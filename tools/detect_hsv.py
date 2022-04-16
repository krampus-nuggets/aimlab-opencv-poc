import sys
import time
import cv2 as cv
import numpy as np
import pygetwindow as gw
from mss import mss


def dummy(x):
    pass


sct = mss()

timeIncrement = 0

target_window = "aimlab_tb"

scan_block = {"top": 0, "left": 0, "width": 640, "height": 400}


def configure_target():
    program_window = gw.getWindowsWithTitle(target_window)[0]

    if program_window.size != (640, 400):
        program_window.resizeTo(640, 400)
        program_window.moveTo(0, 0)


window_properties = {
    "main_window": "HSV Color Detection",
    "hue": {"min": "Hue-Min", "max": "Hue-Max"},
    "saturation": {"min": "Sat-Min", "max": "Sat-Max"},
    "value": {"min": "Val-Min", "max": "Val-Max"},
}

cv.namedWindow(window_properties["main_window"])
cv.resizeWindow(window_properties["main_window"], 640, 400)

# Hue Trackbar
cv.createTrackbar(
    window_properties["hue"]["min"], window_properties["main_window"], 0, 180, dummy
)
cv.createTrackbar(
    window_properties["hue"]["max"], window_properties["main_window"], 180, 180, dummy
)

# Saturation Trackbar
cv.createTrackbar(
    window_properties["saturation"]["min"],
    window_properties["main_window"],
    0,
    255,
    dummy,
)
cv.createTrackbar(
    window_properties["saturation"]["max"],
    window_properties["main_window"],
    255,
    255,
    dummy,
)

# Value Trackbar
cv.createTrackbar(
    window_properties["value"]["min"], window_properties["main_window"], 0, 255, dummy
)
cv.createTrackbar(
    window_properties["value"]["max"], window_properties["main_window"], 255, 255, dummy
)

try:
    while True:
        try:
            active_window = gw.getActiveWindowTitle()
        except AttributeError:
            continue

        if active_window == target_window:
            configure_target()

        hueMin = cv.getTrackbarPos(
            window_properties["hue"]["min"], window_properties["main_window"]
        )
        hueMax = cv.getTrackbarPos(
            window_properties["hue"]["max"], window_properties["main_window"]
        )

        satMin = cv.getTrackbarPos(
            window_properties["saturation"]["min"], window_properties["main_window"]
        )
        satMax = cv.getTrackbarPos(
            window_properties["saturation"]["max"], window_properties["main_window"]
        )

        valMin = cv.getTrackbarPos(
            window_properties["value"]["min"], window_properties["main_window"]
        )
        valMax = cv.getTrackbarPos(
            window_properties["value"]["max"], window_properties["main_window"]
        )

        lower_bound = np.array([hueMin, satMin, valMin])
        upper_bound = np.array([hueMax, satMax, valMax])

        frame = np.array(sct.grab(scan_block))
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_frame, lower_bound, upper_bound)

        cv.imshow("HSV Detection Tool", mask)

        if (cv.waitKey(33) & 0xFF) == ord("q"):
            cv.destroyAllWindows()
            break

        timeIncrement += 1
        print(
            f"RUN-TIME: {timeIncrement} | Hue-Min: {hueMin} Hue-Max: {hueMax} | Sat-Min: {satMin} Sat-Max: {satMax} | Val-Min: {valMin} Val-Max: {valMax}",
            end=" \r",
        )
        time.sleep(0.01)
except KeyboardInterrupt:
    cv.destroyAllWindows()
    sys.exit(0)
