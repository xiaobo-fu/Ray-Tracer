import pygame
import engine
from sphere import Sphere, Sphere_Reverse
from ray import Ray
from vector import Vector
from scene import Scene
from material import Material
import random
from light import Light
from point import Point
from color import Color


def draw_ray(ray):

    width = 800
    height = 600
    x0 = width / 2
    y0 = height / 2
    win = pygame.display.set_mode((width, height))

    colour = (random.randrange(0, 256, 1), random.randrange(0, 256, 1), random.randrange(0, 256, 1),)
    ray_start = (x0 + ray.origin.x, y0 - ray.origin.y)
    ray_end = (x0 + ray.origin.x + ray.direction.x * 1000, y0 - (ray.origin.y + ray.direction.y * 1000))
    pygame.draw.line(win, colour, ray_start, ray_end, 2)
    # pygame.time.wait(200)
    # pygame.display.update()


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

    sphere1 = Sphere_Reverse(Vector(0, 0, 0), 200, Material(transparency=0.0
                                                   , specular=0.5
                                                   , diffuse=0.1
                                                   , reflection=0.2
                                                   , refraction_index=1.5))

    sphere2 = Sphere(Vector(200, 200, 0), 100, Material(transparency=1.0
                                                   , specular=0.5
                                                   , diffuse=0.1
                                                   , reflection=0.2
                                                   , refraction_index=1.5))

    objects = [sphere1, sphere2]

    WIDTH = 400
    HEIGHT = int(WIDTH / 2)
    camera = Vector(0, 0, -2.0)

    lights = [
        Light(Point(10, -10, -2), Color.from_hex("#FFFFFF")),
        Light(Point(-1, -10, -2), Color.from_hex("#FFFFFF")),
    ]

    scene = Scene(camera, objects, lights, WIDTH, HEIGHT)

    for sphere in objects:
        pygame.draw.circle(win, (0, 0, 0), (x0 + sphere.center.x, y0 - sphere.center.y), sphere.radius, 1)

    pygame.display.update()

    e = engine.RenderEngine()

    run = True
    while run:
        # quit if end
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if event.type == pygame.MOUSEBUTTONUP:
            win.fill((255, 255, 255))

            for sphere in objects:
                pygame.draw.circle(win, (0, 0, 0), (x0 + sphere.center.x, y0 - sphere.center.y), sphere.radius, 1)

            pos = pygame.mouse.get_pos()
            xstart = -100
            ystart = 0
            xend = pos[0] - x0 - xstart
            yend = -pos[1] + y0 - ystart

            ray = Ray(Vector(xstart, ystart), Vector(xend, yend))
            draw_ray(ray)
            print(e.find_nearest(ray, scene))
            e.ray_trace(ray, scene)
            pygame.display.update()








