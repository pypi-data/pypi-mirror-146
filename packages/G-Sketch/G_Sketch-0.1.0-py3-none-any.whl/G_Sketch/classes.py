class Pixel:

    def __init__(self, x, y, white):
        self.x = x
        self.y = y
        self.white = white

    def get_color(self):
        return "W" if self.white else "B"

    def get_coords(self):
        return self.x, self.y


class Body:

    def __init__(self, outline_pixels):
        self.outline_pixels = outline_pixels

