import pygame
import engine
from sphere import Sphere
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
    pygame.time.wait(100)
    pygame.display.update()


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

    WIDTH = 400
    HEIGHT = int(WIDTH / 2)
    camera = Vector(0, 0, -2.0)

    lights = [
        Light(Point(10, -10, -2), Color.from_hex("#FFFFFF")),
        Light(Point(-1, -10, -2), Color.from_hex("#FFFFFF")),
    ]

    scene = Scene(camera, objects, lights, WIDTH, HEIGHT)

    pygame.draw.circle(win, (0, 0, 0), (x0 + sphere.center.x, y0 - sphere.center.y), sphere.radius, 1)

    e = engine.RenderEngine()


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
            e.ray_trace(ray, scene)








