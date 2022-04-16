import sys
import time
import keyboard
import cv2 as cv
import numpy as np
from mss import mss
import pydirectinput
from os import system
import pygetwindow as gw
from modules.native_controller import MouseMoveTo
from modules.native_controller import MouseClick

aimlab_title = "aimlab_tb"

window_width, window_height = (640, 480)

timeIncrement = 0

toggle_button = "delete"

active_state = False

last_toggle_state = False

sct = mss()

scan_block = {"top": 0, "left": 0, "width": window_width, "height": window_height}

lower_bound = np.array([86, 138, 88])
upper_bound = np.array([97, 244, 255])

pos_range = {"x": [-1, 0, 1], "y": [9, 10, 11]}


def configure_aimlab():
    aimlab_window = gw.getWindowsWithTitle(aimlab_title)[0]

    if aimlab_window.size != (window_width, window_height):
        aimlab_window.resizeTo(window_width, window_height)
        aimlab_window.moveTo(0, 0)


def coord_diff(center_coord, axis_coord):
    diff = 0

    if axis_coord > center_coord:
        diff = axis_coord - center_coord

    if axis_coord < center_coord:
        diff = -(center_coord - axis_coord)

    return diff


def calc_pos(window_width, window_height, x_coord, y_coord):
    center_x = int(window_width / 2)
    center_y = int(window_height / 2)

    offset_x = coord_diff(center_x, int(x_coord))
    offset_y = coord_diff(center_y, int(y_coord))

    if center_x == offset_x:
        offset_x = 0

    if center_y == offset_y:
        offset_y = 0

    return (offset_x, offset_y)


try:
    while True:
        off_x = 0
        off_y = 0
        contour_x = 0
        contour_y = 0
        dx_x, dx_y = pydirectinput.position()
        key_state = keyboard.is_pressed(toggle_button)

        # TOGGLE: Enable/Disable Recoil-Control
        if key_state != last_toggle_state:
            last_toggle_state = key_state
            if last_toggle_state:
                active_state = not active_state

        try:
            active_window = gw.getActiveWindowTitle()
        except AttributeError:
            continue

        if active_window == aimlab_title:
            configure_aimlab()

        frame = np.array(sct.grab(scan_block))
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_frame, lower_bound, upper_bound)

        contours, hierarchy = cv.findContours(
            mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )

        contour_positions = []

        for contour in contours:
            all_moments = cv.moments(contour)

            contour_x = int(all_moments["m10"] / (all_moments["m00"] + 1e-5))
            contour_y = int(all_moments["m01"] / (all_moments["m00"] + 1e-5))

            cv.circle(mask, (contour_x, contour_y), 5, (255, 255, 255), -1)
            cv.putText(
                mask,
                f"X - {contour_x} | Y - {contour_y}",
                (contour_x - 25, contour_y - 25),
                cv.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )

            off_x, off_y = calc_pos(window_width, window_height, contour_x, contour_y)

            if active_window == aimlab_title and active_state:
                MouseMoveTo(off_x, (off_y - 10))

                if off_x in pos_range["x"] and off_y in pos_range["y"]:
                    MouseClick()

        print(
            f"RUN-TIME: {timeIncrement} | WINDOW: {active_window} | DX-X: {dx_x} DX-Y: {dx_y} | O-X: {off_x} O-Y: {off_y} | ACTIVE: {active_state}"
        )

        cv.imshow("Aimlab Feed", frame)
        cv.imshow("Aimlab Masked Feed", mask)

        if (cv.waitKey(33) & 0xFF) == ord("q"):
            cv.destroyAllWindows()
            break

        timeIncrement += 1

        system("cls")
        time.sleep(0.001)
except KeyboardInterrupt:
    cv.destroyAllWindows()
    sys.exit(0)
