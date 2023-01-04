import cv2
from coordinate import Coordinate
from mercator import Location, Mercator
import colorsys
import math

# 129, 212, 116 - green
# 241, 156, 92 - orange
# 223, 77, 62 - red
# 117, 40, 35 - maroon



class Recognizer():
    mercator = None
    mod = None
    frame = None
    colors = []

    def __init__(
            self,
            frame,
            center_latitude,
            center_longitude,
            zoom_level,
            mod):

        self.frame = frame
        height, width, _ = frame.shape

        self.mercator = Mercator(
            center_latitude,
            center_longitude,
            width,
            height,
            zoom_level
        )

        self.mod = mod

        self.colors = []
        self.init_colors()

    def init_colors(self):
        # Initialize green traffic hsv
        r, g, b = (130, 211, 117)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        h, s, v = (math.floor(h*179), math.floor(s*255), math.floor(v*255))
        self.colors.append({"lB": (h, s, v), "uB": (h+1, s+1, v+1)})

        # Initialize orange traffic hsv
        r, g, b = (241, 156, 92)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        h, s, v = (math.floor(h*179), math.floor(s*255), math.floor(v*255))
        self.colors.append({"lB": (h, s, v), "uB": (h+1, s+1, v+1)})

        # Initialize red traffic hsv
        r, g, b = (223, 77, 62)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        h, s, v = (math.floor(h*179), math.floor(s*255), math.floor(v*255))
        self.colors.append({"lB": (h, s, v), "uB": (h+1, s+1, v+1)})

        # Initialize maroon traffic hsv
        r, g, b = (119, 39, 35)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        h, s, v = (math.floor(h*179), math.floor(s*255), math.floor(v*255))
        self.colors.append({"lB": (h, s, v), "uB": (h+1, s+1, v+1)})

    def segregate_traffic(self, src, key):
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.colors[key]["lB"], self.colors[key]["uB"])

        result = cv2.bitwise_and(src, src, mask=mask)

        return (hsv, mask, result)

    def process_traffic(self, src, name, key, day_id, time_id):
        height, width, _ = self.frame.shape
        top_left = self.mercator.get_location(0, 0)
        bottom_right = self.mercator.get_location(width, height)

        coord = Coordinate(top_left, bottom_right, key)

        locations = cv2.findNonZero(src)

        coordinates: list[Location] = []

        if locations is not None:
            locations = [v[0] for i, v in enumerate(locations)]
            for i, v in enumerate(locations):
                if i % self.mod == 0:
                    x, y = v
                    coordinate = self.mercator.get_location(x, y)
                    coordinates.append(coordinate)

            coord.insert_to_db(coordinates, key, day_id, time_id)
