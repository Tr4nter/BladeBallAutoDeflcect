import keyboard # Library that relates to reading and writing keyboard inputs
import math
import time
import PIL.ImageGrab # Reads screenshot in the right format (mss takes the screenshot)
import PIL.Image
import os
import mss # Takes screenshot
import configparser
import cv2 # Reads through screenshot
import numpy as np # Works with CV2
import win32api # Windows API that I just use for mouse button keybinds and mouse movement to an enemy
import win32con
from colorama import Fore, Style, init # Makes the colorful text in the console
from ctypes.wintypes import HWND, DWORD, RECT
import ctypes # Also Windows API to move the mouse
import time # Allows for specific time delays and such
#importing all the modules we need to run the code.
def GetWindowRectFromName(name:str)-> tuple:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    return (rect.left, rect.top, rect.right, rect.bottom)

upper = np.array([173,190,255],dtype="uint8")
lower = np.array([166,0,169],dtype="uint8")
found = False
ori = 30
val = ori

minRadMinus = 1
sct = mss.mss()
screenshot = sct.monitors[1] #this is the settings for the screen capture, the program screenshots your first monitor and continues to look for enemies.
while True:
    if keyboard.is_pressed('x'):
        val = ori
    if keyboard.is_pressed("c"):
        val += 1
    if keyboard.is_pressed("v"):
        val -= 1
    roblox = GetWindowRectFromName("Roblox")
    screenshot["left"] = roblox[0]
    screenshot["top"] = roblox[1]
    screenshot["width"] = int(roblox[2]-roblox[0])
    screenshot["height"] = int((roblox[3]-roblox[1]))
    img = np.array(sct.grab(screenshot))
    cv2.putText(img, str(val), (roblox[0]+5, roblox[1]+20),cv2.FONT_HERSHEY_COMPLEX ,1,  (0,255,0), 2, cv2.LINE_AA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    kernal = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(mask, kernal, iterations=1)
    circel = cv2.HoughCircles(dilated, cv2.HOUGH_GRADIENT, 1, 100, param1=30, param2=20, minRadius=10, maxRadius=100)
    circleCount = 0
    if circel is not None:
        circel = np.uint16(np.around(circel))
        for i in circel[0,:]:
            circleCount += 1
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    else:
        found = False
    if circleCount == 1:
        ball = circel[0]
        radius = ball[0][2]
        if radius > val and keyboard.is_pressed('z') and not found:
            keyboard.press_and_release("f")
            cv2.putText(img, str(radius), (ball[0][0], ball[0][1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
            found = True
    cv2.imshow("meh", img)
    cv2.waitKey(1)
    # (contours, hierachy) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # print(len(contours))
    # cv2.drawContours(, contours,0, (36,255,12),2)
    # if len(contours) > 0:

    #     contour = max(contours,key=cv2.contourArea)
    #     topmost = tuple(contour[contour[:, :, 1].argmin()][0]) 
    #     bottommost = tuple(contour[contour[:, :, 1].argmax()][0]) 
    #     x = int((topmost[0]+bottommost[0])/2)
    #     y = int((topmost[1]+bottommost[1])/2)
    #     img = cv2.circle(img, (x,y), 5, (0,255,0), 1)
    #     distance = np.sqrt(x**2 + y**2)
    #     print(distance)
        # if distance > maxDistance: maxDistance = distance
    #         val-=3.5
    #     x,y,w,h = cv2.boundingRect(contour)
    #     speed = max(min((w-lastWidth),50),0)
    #     if speed > 0:
    #         step+=speed
    #         stepTick = time.time()
    #     lastWidth = w
    #     if step+speed > val and  keyboard.is_pressed('z') and not found:
    #         print(val)
    