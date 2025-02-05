#LICENSED UNDER THE Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License (CC BY-NC-SA 3.0)
#Freenove 2016 - 2025
#Thank you Freenove for the base of this code (https://freenove.com/)
# (Some of the code) By Kiamehr Eskandari
import cv2
import time
from picamera2 import Picamera2
from ultralytics import YOLO
from Motor import *
from random import randint
import Ultrasonic

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (2560, 1440)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

model = YOLO("yolo11n.pt")
PWM = Motor()
ultra = Ultrasonic.Ultrasonic()

count = 0
position = None

while True:
    PWM.setMotorModel(2000, 2000, 2000, 2000)  
    frame = picam2.capture_array()

    results = model(frame)


    for box in results[0].boxes.xyxy:
        x_min, y_min, x_max, y_max = box
        center_x = (x_min + x_max) / 2

        if center_x < frame.shape[1] / 3:
            position = 0  # Left
        elif center_x > 2 * frame.shape[1] / 3:
            position = 1  # Right
        else:
            position = 2  # Middle

    if position is not None:
        if position == 0:  # Left
            if ultra.get_distance() <= 100:
                PWM.setMotorModel(2000,2000,-500,-500)       #Right    
                time.sleep(2)
                PWM.setMotorModel(-500,-500,2000,2000)       #Left 
                time.sleep(2)
            else:
                print('Object detected too far')
        elif position == 1:  # Right
            if ultra.get_distance() <= 100:
                PWM.setMotorModel(-500,-500,2000,2000)       #Left 
                time.sleep(2)
                PWM.setMotorModel(2000,2000,-500,-500)       #Right    
                time.sleep(2)
            else:
                print('Object detected too far')
        else:  # Middle
            if ultra.get_distance() <= 100:
                choice = randint(1, 2)
                if choice == 1:
                    PWM.setMotorModel(-500,-500,2000,2000)       #Left 
                    time.sleep(2)
                    PWM.setMotorModel(2000,2000,-500,-500)       #Right    
                    time.sleep(2)
                else:
                    PWM.setMotorModel(2000,2000,-500,-500)       #Right    
                    time.sleep(2)
                    PWM.setMotorModel(-500,-500,2000,2000)       #Left 
                    time.sleep(2)
            else:
                print('Object detected too far')
    else:
        print('No objects detected')

    annotated_frame = results[0].plot()

    cv2.imshow("Camera", annotated_frame)

    count += 1

    if count == 10:
        print('End of program')
        PWM.setMotorModel(0, 0, 0, 0)
        break


cv2.destroyAllWindows()
picam2.stop()
