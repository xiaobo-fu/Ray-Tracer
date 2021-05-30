from color import Color

# deal with color and Material which tells us how it reacts to light


class Material:
    def __init__(
            self, color=Color.from_hex("#FFFFFF"),
            ambient=0,
            diffuse=0.9,
            specular=0.6,
            reflection=0.5,
            transparency=0.0,
            refraction_index=0.0
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.transparency = transparency
        self.refraction_index = refraction_index

    def color_at(self, position):
        return self.color


class ChequeredMaterial:
    def __init__(
            self,
            color1=Color.from_hex("#FFFFFF"),
            color2=Color.from_hex("#FFFFFF"),
            ambient=0.03,
            diffuse=0.9,
            specular=0.6,
            reflection=0,
            transparency=0.0

    ):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.transparency = transparency

    def color_at(self, position):
        # create a chequer board pattern
        if int((position.x + 2) * 2) % 2 == int(position.z * 2) % 2:
            return self.color1
        else:
            return self.color2