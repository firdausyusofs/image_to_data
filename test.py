import cv2
from recognizer import Recognizer

zoom_level = 16
mod = 5

for i in range(2):
    src = cv2.imread("./process/Wednesday/6_0/6_0_0.png")
    center_lat: float = None
    center_lon: float = None

    with open(f"./process/Wednesday/6_0/6_0_0.txt") as f:
        center_lat, center_lon = tuple(float(i) for i in f.readline().split(","))
        f.close()

    recog = Recognizer(src, center_lat, center_lon, zoom_level, mod)

    for j in range(len(recog.colors)):
        hsv, mask, result = recog.segregate_traffic(src, j)
        recog.process_traffic(mask, "test", j)
