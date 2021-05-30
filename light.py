from color import Color


# a point light source of a certain color
class Light:
    def __init__(self, position, intensity=1, color=Color.from_hex("#FFFFFF")):
        self.position = position
        self.intensity = intensity
        self.color = color