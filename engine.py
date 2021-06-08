from image import Image
from ray import Ray
from point import Point
from color import Color
from math import sqrt


# renders 3D objects into 2D objects using ray tracing
class RenderEngine:

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001

    # basic setups
    def render(self, scene):
        # width, height, aspect ratio
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height

        # set up the ray steps according to pixels
        # most left as -1 and most right as +1, same for y axis
        x0 = -1.0
        x1 = +1.0
        # there are (width - 1) steps, same for  y axis
        xstep = (x1 - x0) / (width - 1)
        y0 = -1.0 / aspect_ratio
        y1 = +1.0 / aspect_ratio
        ystep = (y1 - y0) / (height - 1)

        camera = scene.camera

        # initialize pixels array
        pixels = Image(width, height)

        # shoot rays pixel by pixel
        for j in range(height):
            y = y0 + j * ystep
            for i in range(width):
                x = x0 + i * xstep
                # shoot rays from the camera to each pixel
                ray = Ray(camera, Point(x, y) - camera)
                # set color to each pixel using ray trace
                pixels.set_pixel(i, j, self.ray_trace(ray, scene))
            # print the progress
            print(f"{int(j/height * 100)} %")
        return pixels

    # get color using ray trace
    def ray_trace(self, ray, scene, depth=0):
        # set initial color
        color = Color(0, 0, 0)

        # find the nearest object, and return the object and the distance to it
        dist_hit, obj_hit, dist_far = self.find_nearest(ray, scene)
        # if hits nothing, do nothing
        if obj_hit is None:
            return color
        # get the hit position on the object and its normal
        hit_pos = ray.origin + ray.direction * dist_hit
        hit_normal = obj_hit.normal(hit_pos)

        # calculate the hit position diffusion and specular using color at function
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene)

        # calculating the reflection
        if depth < self.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = ray.direction - 2 * ray.direction.dot_product(hit_normal) * hit_normal
            new_ray = Ray(new_ray_pos, new_ray_dir)
            # dim the new ray by the reflection coefficient
            color += self.ray_trace(new_ray, scene, depth+1) * obj_hit.material.reflection

        # # calculating refraction if the hit object is transparent
        # if obj_hit.material.transparency != 0:
        #     if self.MIN_DISPLACE > dist_hit > -self.MIN_DISPLACE:
        #         dist_hit = 0
        #     hit_pos_far = ray.origin + ray.direction * dist_far
        #     hit_normal_far = obj_hit.normal(hit_pos_far)
        #     color += self.refraction(ray, obj_hit, hit_pos, dist_hit, hit_normal, hit_pos_far, dist_far,
        #                             hit_normal_far, scene, depth)
        #
        #     return color

        return color

    def refraction(self, ray, obj_hit, hit_pos, dist_hit, hit_normal, hit_pos_far, dist_far,
                                    hit_normal_far, scene, depth):
        color = Color(0, 0, 0)
        cos_theta = -ray.direction.dot_product(hit_normal)

        # if air/glass
        if dist_hit > 0:
            refraction_index = 1 / obj_hit.material.refraction_index
            hit_pos = hit_pos - (self.MIN_DISPLACE / 2) * ray.direction
        # if glass/air
        elif dist_hit == 0:
            hit_pos = hit_pos_far + self.MIN_DISPLACE * ray.direction
            refraction_index = obj_hit.material.refraction_index
            hit_normal = -hit_normal
        else:
            print('should not be here')
            return color

        k = 1.0 - refraction_index ** 2 * (1.0 - cos_theta ** 2)

        if k < 0:
            print("internal")
            return color
        else:
            refraction_origin = hit_pos
            refraction_ray_perp = refraction_index * (ray.direction + cos_theta * hit_normal)
            refraction_ray_para = -hit_normal * sqrt(k)
            refraction_direction = refraction_ray_perp + refraction_ray_para
            refraction_ray = Ray(refraction_origin, refraction_direction)

            # todo delete after finish
            import test
            test.draw_ray(refraction_ray)

            return self.ray_trace(refraction_ray, scene, depth)

    # find the nearest object, and return the object and the distance to it
    def find_nearest(self, ray, scene,):
        dist_min = None
        dist_far_min = None
        dist_refraction_min = None
        dist_far_refrection_min = None
        obj_hit = None

        # check objects in the scene
        for obj in scene.objects:
            # check the distance using the object's intersects function
            dist, dist_far = obj.intersects(ray)

            # find nearest for non_refraction intersection
            # if dist is not None then we hit something; and we restore the smallest dist
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                dist_far_min = dist_far
                obj_hit = obj

        return dist_min, obj_hit, dist_far_min

    # calculate the hit position color
    def color_at(self, obj_hit, hit_pos, normal, scene):
        # get the object's color at the hit point
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)

        # a vector to camera
        to_cam = scene.camera - hit_pos

        # a variable decides the size of specular
        specular_k = 1000

        # a very basic ambient light
        color = material.ambient * Color.from_hex("#CCCCFF")

        # light calculations
        for light in scene.lights:
            # a ray from hit position to light position
            to_light = Ray(hit_pos, light.position - hit_pos)

            # to check if any object between the hit point and the light
            isBlockd, hit_obj, _ = self.find_nearest(to_light, scene)

            shadow_index = 1.0
            if isBlockd:
                shadow_index = 0.0
                if hit_obj.material.transparency != 0:
                    shadow_index = 0.7

            # lambert diffuse shading
            color += obj_color * material.diffuse * max(normal.dot_product(to_light.direction), 0) * shadow_index
            # Blinn–Phong specular shading
            half_vector = (to_light.direction + to_cam).normalize()
            color += light.color * material.specular * max(normal.dot_product(half_vector), 0) ** specular_k * shadow_index

        return color
