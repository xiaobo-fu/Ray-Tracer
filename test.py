import pygame
import engine
from sphere import Sphere
from ray import Ray
from vector import Vector
from scene import Scene
from material import Material
import random


def draw_ray(ray):
    colour = (random.randrange(0, 256, 1), random.randrange(0, 256, 1), random.randrange(0, 256, 1),)
    ray_start = (x0 + ray.origin.x, y0 - ray.origin.y)
    ray_end = (x0 + ray.origin.x + ray.direction.x * 1000, y0 - (ray.origin.y + ray.direction.y * 1000))
    pygame.draw.line(win, colour, ray_start, ray_end, 2)
    pygame.time.wait(100)
    pygame.display.update()


def ray_trace(ray, scene):
    depth = 0

    # find the nearest object, and return the object and the distance to it
    dist_hit, obj_hit, dist_far = engine.RenderEngine.find_nearest(None, ray, scene)

    # if hits nothing, do nothing
    if obj_hit is None:
        print("3 hit nothing")
        print()
        return

    # get the hit position on the object and its normal
    hit_pos = ray.origin + ray.direction * dist_hit
    hit_normal = obj_hit.normal(hit_pos)

    # refraction
    # check if the hit object is transparent
    if obj_hit.material.transparency != 0:
        if dist_hit < 0.00001 and dist_hit > -0.00001:
            dist_hit = 0
        hit_pos_far = ray.origin + ray.direction * dist_far
        hit_normal_far = obj_hit.normal(hit_pos_far)
        refraction(ray, obj_hit, hit_pos, dist_hit, hit_normal, hit_pos_far, dist_far,
                                 hit_normal_far, scene, depth)

    return


def refraction(ray, obj_hit, hit_pos, dist_hit, hit_normal, hit_pos_far, dist_far,
                                    hit_normal_far, scene, depth):
    cos_theta = ray.direction.dot_product(hit_normal) * -1
    # if air/glass
    if dist_hit > 0:
        print("1 air/glass")
        print(dist_hit, dist_far)
        refraction_index = 1 / obj_hit.material.refraction_index
    # if glass/air
    elif dist_hit == 0:
        print("2 glass/air")
        print(dist_hit, dist_far)
        hit_pos = hit_pos_far
        refraction_index = obj_hit.material.refraction_index
    else:
        print("3 out")
        print(dist_hit, dist_far)
        print()
        draw_ray(ray)
        return

    k = 1.0 - refraction_index ** 2 * (1.0 - cos_theta ** 2)

    if k < 0:
        print("internal")
        print(dist_hit, dist_far)
        print()
        draw_ray(ray)
        return
    else:
        refraction_origin = hit_pos
        refraction_ray_perp = refraction_index * (ray.direction + cos_theta * hit_normal)
        refraction_ray_para = -1 * hit_normal * k
        refraction_direction = refraction_ray_perp + refraction_ray_para
        refraction_ray = Ray(refraction_origin, refraction_direction)
        draw_ray(refraction_ray)
        dist_hit, obj_hit, dist_far = engine.RenderEngine.find_nearest(None, refraction_ray, scene)
        print("refracted")
        print(dist_hit, dist_far)
        print()
        return ray_trace(refraction_ray, scene)


if __name__ == "__main__":
    # visualize using pygame
    # general setup
    pygame.init()
    clock = pygame.time.Clock()

    width = 800
    height = 600
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Self Organizing Map')

    x0 = width / 2
    y0 = height / 2

    win.fill((255, 255, 255))
    pygame.display.update()

    sphere = Sphere(Vector(0, 0, 0), 100, Material(transparency=1.0
                                                   , specular=0.5
                                                   , diffuse=0.1
                                                   , reflection=0.2
                                                   , refraction_index=2.0))

    objects = [sphere]

    scene = Scene(camera=None, lights=None, width=None, height=None, objects=objects)

    pygame.draw.circle(win, (0, 0, 0), (x0 + sphere.center.x, y0 - sphere.center.y), sphere.radius, 1)


    run = True
    while run:
        # quit if end
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for i in range(-110, 110):
            print(i)
            win.fill((255, 255, 255))
            ray = Ray(Vector(-400, 0), Vector(400, i))
            pygame.draw.circle(win, (0, 0, 0), (x0 + sphere.center.x, y0 - sphere.center.y), sphere.radius, 1)
            draw_ray(ray)
            ray_trace(ray, scene)








