import cv2

class GUI():
    frame = None
    h_min = 0
    s_min = 0
    v_min = 0
    h_max = 179;
    s_max = 255;
    v_max = 255;

    def __init__(self, frame):
        self.frame = frame

    def on_change(self, x):
        pass

    def on_change_hmin(self, x):
        self.h_min = x

    def color(self):
        cv2.namedWindow("Options")

        cv2.createTrackbar("HMin", "Options", 0, 179, self.on_change)
        # cv2.createTrackbar("SMin", "Options", 0, 255, self.on_change)
        # cv2.createTrackbar("VMin", "Options", 0, 255, self.on_change)
        #
        # cv2.createTrackbar("HMax", "Options", 179, 179, self.on_change)
        # cv2.createTrackbar("SMax", "Options", 255, 255, self.on_change)
        # cv2.createTrackbar("VMax", "Options", 255, 255, self.on_change)

        while True:
            key = cv2.waitKey(1)
            if key == 113:
                break

        cv2.waitKey(0)
        cv2.destroyAllWindows()
