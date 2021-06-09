from vector import Vector


# a class to define the camera in redering process
class Camera:
    def __init__(self, position=Vector(0, 0, 0), look_at=Vector(0, 0, 0), angle=100):
        self.position = position
        self.look_at = look_at
        self.magnitude = (look_at - position).magnitude()
        self.direction = (look_at - position).normalize()
        self.angle = angle
