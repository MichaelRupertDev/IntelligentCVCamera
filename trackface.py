import numpy as np
import RPi.GPIO as GPIO
import time
import cv2

class CVRunner():
    position = 3

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    pwm=GPIO.PWM(12, 50)
    pwm.start(position)t

    def moveLeft(self, amt):
        if self.position > 2:
            self.position -= amt
        self.pwm.ChangeDutyCycle(self.position)
        print "moving left.."

    def moveRight(self, amt):
        if self.position < 8:
            self.position += amt
        self.pwm.ChangeDutyCycle(self.position)
        print "moving right.."
        
    def run(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.putText(img, "{} -> {}".format(x, x+w), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                if x > 250:
                    self.moveRight(.5)
                if x < 250:
                    self.moveLeft(.5)
                    
            cv2.imshow('img',img)
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
            
        cv2.destroyAllWindows()

cr = CVRunner()

cr.run()
