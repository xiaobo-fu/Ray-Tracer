from image import Image
from ray import Ray
from point import Point
from color import Color
from math import sqrt, pi, cos, sin
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


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

        camera = scene.camera
        camera_angle_half = camera.angle / 180 * pi / 2

        # set up the ray steps according to pixels
        # most left as -1 and most right as +1, same for y axis
        x0 = cos(-camera_angle_half) * (camera.look_at.x - camera.position.x) + sin(-camera_angle_half) * (
                camera.look_at.z - camera.position.z) + camera.position.x
        x1 = cos(+camera_angle_half) * (camera.look_at.x - camera.position.x) + sin(+camera_angle_half) * (
                camera.look_at.z - camera.position.z) + camera.position.x

        # there are (width - 1) steps, same for  y axis
        xstep = (x1 - x0) / (width - 1)

        z0 = -sin(-camera_angle_half) * (camera.look_at.x - camera.position.x) + cos(-camera_angle_half) * (
                camera.look_at.z - camera.position.z) + camera.position.z
        z1 = -sin(camera_angle_half) * (camera.look_at.x - camera.position.x) + cos(camera_angle_half) * (
                camera.look_at.z - camera.position.z) + camera.position.z

        zstep = (z1 - z0) / (width - 1)

        y0 = -Point(x1 - x0, 0, z1 - z0).magnitude() / 2 / aspect_ratio
        y1 = Point(x1 - x0, 0, z1 - z0).magnitude() / 2 / aspect_ratio
        ystep = (y1 - y0) / (height - 1)


        # # todo visualize the camera
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # ax.set_xlim(-3, 3)
        # ax.set_ylim(-3, 3)
        # ax.set_zlim(-3, 3)
        #
        # ax.scatter(camera.position.x, camera.position.y, camera.position.z, c='g')
        # ax.scatter(camera.look_at.x, camera.look_at.y, camera.look_at.z, c='r')
        # ax.scatter(x0, y0, z0, c='c')
        # ax.scatter(x1, y0, z1, c='b')
        # ax.scatter(x0, y1, z0, c='c', marker='^')
        # ax.scatter(x1, y1, z1, c='b', marker='^')
        # for i in scene.objects[2:]:
        #     ax.scatter(i.center.x, i.center.y, i.center.z, c='y', s=i.radius*100)
        #
        # plt.show()

        # initialize pixels array
        pixels = Image(width, height)

        # shoot rays pixel by pixel
        for j in range(height):
            y = y0 + j * ystep
            for i in range(width):
                x = x0 + i * xstep
                z = z0 + i * zstep
                # shoot rays from the camera to each pixel
                ray = Ray(camera.position, Point(x, y, z) - camera.position)
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

        # calculating refraction if the hit object is transparent
        if obj_hit.material.transparency != 0:
            if self.MIN_DISPLACE > dist_hit > -self.MIN_DISPLACE:
                dist_hit = 0
            hit_pos_far = ray.origin + ray.direction * dist_far
            hit_normal_far = obj_hit.normal(hit_pos_far)
            color += self.refraction(ray, obj_hit, hit_pos, dist_hit, hit_normal, hit_pos_far, dist_far,
                                    hit_normal_far, scene, depth)

            return color

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

            return self.ray_trace(refraction_ray, scene, depth)

    # find the nearest object, and return the object and the distance to it
    def find_nearest(self, ray, scene,):
        dist_min = None
        dist_far_min = None
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
        to_cam = scene.camera.position - hit_pos

        # a variable decides the size of specular
        specular_k = 1000

        # a very basic ambient light
        color = material.ambient * Color.from_hex("#CCCCFF")

        # light calculations
        for light in scene.lights:
            # a ray from hit position to light position
            to_light = Ray(hit_pos, light.position - hit_pos)

            # distance between hit position and light
            dist_to_light = (hit_pos - light.position).magnitude()

            # to check if any object between the hit point and the light
            dist, hit_obj, _ = self.find_nearest(to_light, scene)

            shadow_index = 1.0
            if dist < dist_to_light:
                shadow_index = 0.0
                if hit_obj.material.transparency != 0:
                    shadow_index = 0.7

            # lambert diffuse shading
            color += obj_color * material.diffuse * max(normal.dot_product(to_light.direction), 0) * light.intensity * shadow_index
            # Blinn–Phong specular shading
            half_vector = (to_light.direction + to_cam).normalize()
            color += light.color * material.specular * max(normal.dot_product(half_vector), 0) ** specular_k * light.intensity * shadow_index

        return color
