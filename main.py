import cv2
import numpy as np
import os
from typing import cast
from recognizer import Recognizer
from utils import Utils

zoom_level = 16
mod = 5
cur_reverse = True

days = ["Wednesday", "Friday"]

for i, day in enumerate(days):
    day_id = Utils.get_or_create_day(day)
    for j, time in enumerate(Utils.get_sorted_times("./process/"+day)):
        time_id = Utils.get_or_create_time(time)

        reverse = Utils.check_reverse(cur_reverse, j)

        cur_reverse = reverse

        files = Utils.get_sorted_files("./process/"+day+"/"+time)
        for k, file in enumerate(files):
            if file.endswith(".png"):
                filename = file.replace(".png", "")
                _, _, index = tuple(int(i) for i in filename.split("_"))

                if reverse:
                    index = (len(files)-1)-index

                print(day, filename, index, reverse)

                # src = cv2.imread("./process/"+day+"/"+time+"/"+file)
                #
                # with open(f"./process/{day}/{time}/{filename}.txt") as f:
                #     center_lat, center_lon = tuple(float(i) for i in f.readline().split(","))
                #     f.close()
                #
                # recog = Recognizer(src, center_lat, center_lon, zoom_level, mod, index)
                #
                # for idx in range(len(recog.colors)):
                #     hsv, mask, result = recog.segregate_traffic(src, idx)
                #     recog.process_traffic(mask, idx, day_id, time_id)
