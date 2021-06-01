from math import sqrt


# sphere object
class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    # check if ray intersects the sphere. Returns distance to intersection or None
    def intersects(self, ray):
        sphere_to_ray = ray.origin - self.center
        # a = 1
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        discriminant = b * b - 4 * c

        # if intersects, get the nearest distance
        if discriminant >= 0:
            dist = (-b - sqrt(discriminant)) / 2
            dist_far = (-b + sqrt(discriminant)) / 2
            if dist >= 0:
                return dist, dist_far
        return None, None

    # returns surface normal to the point on sphere's surface
    def normal(self, surface_point):
        return (surface_point - self.center).normalize()
