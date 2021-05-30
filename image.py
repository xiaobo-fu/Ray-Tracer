# a class creates ppm file by each pixel
class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # create a WxH array filled with Nones
        self.pixels = [[None for _ in range(width)] for _ in range(height)]

    # set pixel color at a speci
    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def write_ppm(self, img_file):
        def to_byte(c):
            # to make sure color is between 0 - 255 and rounded
            return round(max(min(c * 255, 255), 0))

        # write the head of the ppm file
        img_file.write("P3 {} {}\n255\n".format(self.width, self.height))

        # write the pixels
        for row in self.pixels:
            for color in row:
                img_file.write(
                    "{} {} {} ".format(
                        to_byte(color.x), to_byte(color.y), to_byte(color.z)
                        )
                    )
            img_file.write("\n")