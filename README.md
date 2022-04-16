<p align="center">
<img src="https://res.cloudinary.com/wemakeart/image/upload/v1650072158/github-projects/aimlab-poc/aimlab-poc-bot_dietko.png" width=150px height="150px"  alt="docs-icon"/>
</p>

# Aimlab - OpenCV POC

This repository serves as a Proof-of-Concept for myself on working with OpenCV in Python. Playing with color-spaces, masking, identifying, tracking, etc.

### What was accomplished in this POC:

1. A tool was created for fine tuning HSV lower & upper bound values
2. Objects in the screen-capture scan-box were successfully identified
3. A c-types controller was built for MnK events because DirectInput is slow and win32api does not work
4. Basic logic was implemented for finding the center of each identified object and the clicking it

### Technology used:

1. mss - Very fast screenshot package
2. c-types - Building MnK controller
3. keyboard - Used for handling basic keyboard events
4. pydirectinput - Finding cursor position values in a 3D scene of Aimlab
5. opencv-python - Open Source Computer Vision handles the bulk of the project workload
6. pygetwindow - Logic based on whether Aimlab window is active | Identify Aimlab window

### Interesting Reads:

1. OpenCV Find Contours - [Link](https://docs.opencv.org/4.x/df/d0d/tutorial_find_contours.html)
2. OpenCV inRange Thresholding - [Link](https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html)
3. Aimbot Math - [Link](https://www.unknowncheats.me/forum/counterstrike-global-offensive/137492-math-behind-hack-1-coding-better-aimbot-stop-using-calcangle.html)

### Example

https://res.cloudinary.com/wemakeart/video/upload/v1650071232/github-projects/aimlab-poc/Aimlab-Gridshot-FINAL-720p_gm4aj1.mp4
