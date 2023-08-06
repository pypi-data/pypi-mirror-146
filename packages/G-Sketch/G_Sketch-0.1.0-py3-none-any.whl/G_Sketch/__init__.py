import math
import sys
from PIL import Image
from G_Sketch.classes import *


def distance(coord1, coord2):

    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[0] - coord2[0]) ** 2)


class Sketch:
    coords = []

    def __init__(self, img_name):

        self.coords = []

        try:
            self.img = Image.open(img_name)

        except FileNotFoundError:
            raise Exception(img_name + " is not a valid file name.")

        self.pixels = list(self.img.getdata())
        self.width, self.height = self.img.size
        self.populate_coords()
        self.bodies = []
        self.counter = 0

        for row in self.coords:
            for coord in row:
                if self.is_edge(coord):

                    check = True

                    for body in self.bodies:
                        if coord in body.outline_pixels:
                            check = False
                    if check:
                        body = Body([])
                        self.get_outline(coord, body)
                        self.bodies.append(body)

    # Copying image data over to 2D array

    def set_min_distance(self, min_dist):

        for i in range(len(self.bodies)):

            new_pixels = [self.bodies[i].outline_pixels[0]]

            for pixel in self.bodies[i].outline_pixels:

                if distance(new_pixels[-1].get_coords(), pixel.get_coords()) > min_dist:

                    new_pixel = Pixel(pixel.get_coords()[0], pixel.get_coords()[1], False)
                    new_pixels.append(new_pixel)

            self.bodies[i].outline_pixels = new_pixels


    def populate_coords(self):
        x = 0
        y = 0
        counter = 1
        cur_row = []

        for pixel in self.pixels:

            if not self.is_white(pixel):
                cur_row.append(Pixel(x, y, False))

            else:
                cur_row.append(Pixel(x, y, True))

            if counter % self.width == 0:
                y += 1
                x = -1
                self.coords.append(cur_row)
                cur_row = []

            x += 1

            counter += 1

    # Checking if pixel is white

    def is_white(self, pixel):
        return pixel[0] > 250 and pixel[1] > 250 and pixel[2] > 250

    # Checking if pixel is located on the edge

    def is_edge(self, pixel):
        poses = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        for pos in poses:

            try:

                if pixel.get_color() == "B" and self.coords[pixel.get_coords()[1] + pos[0]][
                    pixel.get_coords()[0] + pos[1]].get_color() == "W":
                    return True

            except IndexError:
                return True

        return False

    def get_outline(self, pixel, body):
        poses = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        body.outline_pixels.append(pixel)

        for pos in poses:

            try:

                if self.coords[pixel.get_coords()[1] + pos[0]][pixel.get_coords()[0] + pos[1]].get_color() == "B":

                    if not self.coords[pixel.get_coords()[1] + pos[0]][
                               pixel.get_coords()[0] + pos[1]] in body.outline_pixels:

                        if self.is_edge(self.coords[pixel.get_coords()[1] + pos[0]][pixel.get_coords()[0] + pos[1]]):
                            self.get_outline(
                                self.coords[pixel.get_coords()[1] + pos[0]][pixel.get_coords()[0] + pos[1]], body)
            except:
                pass

    # Maxing out recursion (simple recursions occurring so it should be safe)

    sys.setrecursionlimit(100000000)

    # Returns all coordinates of all bodies glued together

    def get_raw_coords(self):

        # Bodies holds each separate piece found in the image. Each body has a collection of pixels representing its outline

        pixels = []

        for body in self.bodies:

            for pixel in body.outline_pixels:
                pixels.append(pixel.get_coords())

        return pixels

    # Returns coords with breaks between bodies

    def get_coords(self):

        # Bodies holds each separate piece found in the image. Each body has a collection of pixels representing its
        # outline

        pixels = []

        for body in self.bodies:

            for pixel in body.outline_pixels:
                pixels.append(pixel.get_coords())

            pixels.append("BREAK")

        return pixels
