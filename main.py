import cv2
import numpy as np
import os
from typing import cast
from recognizer import Recognizer
from utils import Utils

# recog = Recognizer(src, center_latitude, center_longitude, 16, 5)

# for a,b,c in os.walk("./process"):
#     print(a, b, c)

zoom_level = 16
mod = 5

for i, day in enumerate(os.listdir("./process")):
    if day == ".DS_Store":
        continue

    day_id = Utils.get_or_create_day(day)
    for j, time in enumerate(os.listdir("./process/"+day)):
        if time == ".DS_Store":
            continue

        time_id = Utils.get_or_create_time(time)
        for k, file in enumerate(os.listdir("./process/"+day+"/"+time)):
            if file.endswith(".png"):
                filename = file.replace(".png", "")
                src = cv2.imread("./process/"+day+"/"+time+"/"+file)

                with open(f"./process/{day}/{time}/{filename}.txt") as f:
                    center_lat, center_lon = tuple(float(i) for i in f.readline().split(","))
                    f.close()

                recog = Recognizer(src, center_lat, center_lon, zoom_level, mod)

                for i in range(len(recog.colors)):
                    hsv, mask, result = recog.segregate_traffic(src, i)
                    recog.process_traffic(mask, "test", i, day_id, time_id)

# for i in range(2):
#     src = cv2.imread("./process/Wednesday/6_0/6_0_0.png")
#     center_lat: float = None
#     center_lon: float = None
#
#     with open(f"./process/Wednesday/6_0/6_0_0.txt") as f:
#         center_lat, center_lon = tuple(float(i) for i in f.readline().split(","))
#         f.close()
#
#     recog = Recognizer(src, center_lat, center_lon, zoom_level, mod)
#
#     for j in range(len(recog.colors)):
#         hsv, mask, result = recog.segregate_traffic(src, j)
#         recog.process_traffic(mask, "test", j)
