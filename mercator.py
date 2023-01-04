import math

DEFAULT_PROJECTION_WIDTH = 256
DEFAULT_RPOJECTION_HEIGHT = 256

class Point():
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Location():
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Mercator():
    center_latitude = None
    center_longitude = None
    area_width = None
    area_height = None
    area_scale = None
    projection_width = None
    projection_height = None
    pixels_per_lon_degree = None
    pixels_per_lon_radian = None
    projection_center_px = None
    projection_center_py = None

    def __init__(self, center_latitude, center_longitude, area_width, area_height, area_scale):
        self.center_latitude = center_latitude
        self.center_longitude = center_longitude
        self.area_width = area_width
        self.area_height = area_height
        self.area_scale = math.pow(2, area_scale)
        self.projection_width = DEFAULT_PROJECTION_WIDTH
        self.projection_height = DEFAULT_RPOJECTION_HEIGHT

        self.pixels_per_lon_degree = self.projection_width/360
        self.pixels_per_lon_radian = self.projection_width/(2 * math.pi)

        centerPoint = self.project_location(center_latitude, center_longitude)
        self.projection_center_px = centerPoint.x * self.area_scale
        self.projection_center_py = centerPoint.y * self.area_scale

    def project_location(self, latitude, longitude) -> Point:
        px = self.projection_width / 2 + longitude * self.pixels_per_lon_degree
        siny = math.sin(self.deg2rad(latitude))
        py = (self.projection_height / 2) + 0.5 * math.log((1 + siny) / (1 - siny)) * -self.pixels_per_lon_radian

        return Point(px, py)

    def rag2deg(self, rad):
        return (rad * 180) / math.pi

    def deg2rad(self, deg):
        return (deg * math.pi) / 180

    def project_px(self, px, py) -> Location:
        longitude = (px - self.projection_width / 2) / self.pixels_per_lon_degree
        latitudeRadians = (py - self.projection_height / 2) / -self.pixels_per_lon_radian
        latitude = self.rag2deg(2 * math.atan(math.exp(latitudeRadians)) - math.pi / 2)

        return Location(latitude, longitude)

    def get_point(self, latitude, longitude) -> Point:
        px, py = self.project_location(latitude, longitude)

        x = (px * self.area_scale - self.projection_center_px) * self.area_width / 2
        y = (py * self.area_scale - self.projection_center_py) * self.area_height / 2

        return Point(x, y)

    def get_location(self, px, py) -> Location:
        x = self.projection_center_px + (px - self.area_width / 2)
        y = self.projection_center_py + (py - self.area_height / 2)

        return self.project_px(x / self.area_scale, y / self.area_scale)
