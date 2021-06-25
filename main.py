from color import Color
from engine import RenderEngine
from light import Light
from material import Material, ChequeredMaterial
from point import Point
from scene import Scene
from sphere import Sphere
from vector import Vector
from camera import Camera


def main():
    WIDTH = 800
    HEIGHT = int(WIDTH / 2)
    camera = Camera(position=Vector(4, 0, 0.5), look_at=Vector(0, 0, 3), angle=53)
    objects = [
        # Ground Plane with Chequered Material, also a giant ball
        Sphere(Point(-1.8, 1000.5, 1), 1000.0, ChequeredMaterial(color1=Color.from_hex("#FFFFFF"),
                                                                color2=Color.from_hex("#87ceeb"), ambient=0.0,
                                                                diffuse=0.6, specular=0,
                                                                reflection=0.05, ),),
        # background ball
        Sphere(Point(0, 0, 1000010), 1000000, Material(Color.from_hex("#87ceeb"), ambient=0, diffuse=0.6, specular=0,
                                                   reflection=0, transparency=0)),
        # Red ball
        Sphere(Point(0.2, 0.1, 4), 0.4, Material(Color.from_hex("#ddbea9"), ambient=0, diffuse=1, specular=0.5,
                                                 reflection=0.5, transparency=0)),
        # Blue ball
        Sphere(Point(-1, -0.2, 3), 0.7, Material(Color.from_hex("#d75b1d"), ambient=0, diffuse=1.0, specular=0.5,
                                                 reflection=0.8, transparency=0)),
        # Pink ball
        Sphere(Point(0.7, 0.4, 1.6), 0.1, Material(Color.from_hex("#ffb4a2"), ambient=0, diffuse=0.6, specular=0.5,
                                                   reflection=0.2, transparency=0)),
        # transparent ball
        Sphere(Point(0.7, 0.0, 3.1), 0.5, Material(Color.from_hex("#FFFFFF"), transparency=1.0, specular=0.5,
                                                 diffuse=0.0, reflection=0.1, refraction_index=1.5)),
        # transparent ball
        Sphere(Point(-0.5, 0.3, 1), 0.2, Material(Color.from_hex("#FFFFFF"), transparency=1.0, specular=0.5,
                                                  diffuse=0.0, reflection=0.1, refraction_index=1.5)),
    ]

    lights = [
        Light(Point(10, -10, -2), Color.from_hex("#FFFFFF")),
        Light(Point(-1, -10, -2), Color.from_hex("#FFFFFF")),
    ]

    scene = Scene(camera, objects, lights, WIDTH, HEIGHT)
    engine = RenderEngine()
    image = engine.render(scene)

    with open("test.ppm", "w") as img_file:
        image.write_ppm(img_file)


if __name__ == '__main__':
    main()
