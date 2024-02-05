import time
from time import sleep
import RPi.GPIO as GPIO

import speech_recognition as sr
import pyttsx3
import pyaudio

pwm_sol = 0

A0 = 0
A1 = 0
A2 = 0
A3 = 0

segments = 0

digit_pins = 0

binary_dict = 0

stepper = 0
CCW = 0
CW = 0

in2 = 0
in1 = 0
in3 = 0
in4 = 0
en1 = 0
en2 = 0
solenoid_pin = 0
temp1 = 0

p1 = 0
p2 = 0


def setupV():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    global pwm_sol
    pwm_sol = GPIO.PWM(4, 500)
    global A0
    A0 = 5
    global A1
    A1 = 6
    global A2
    A2 = 11
    global A3
    A3 = 9
    global segments
    segments = [A3, A2, A1, A0]
    GPIO.setup(segments, GPIO.OUT, initial=0)
    global digit_pins
    digit_pins = [2, 3]
    GPIO.setup(digit_pins, GPIO.OUT, initial=1)
    global binary_dict
    binary_dict = {' ': [1, 1, 1, 1],
                   '0': [0, 0, 0, 0],
                   '1': [0, 0, 0, 1],
                   '2': [0, 0, 1, 0],
                   '3': [0, 0, 1, 1],
                   '4': [0, 1, 0, 0],
                   '5': [0, 1, 0, 1],
                   '6': [0, 1, 1, 0],
                   '7': [0, 1, 1, 1],
                   '8': [1, 0, 0, 0],
                   '9': [1, 0, 0, 1], }
    global stepper
    stepper = Stepper()
    global CCW
    CCW = True
    global CW
    CW = False
    global in2
    in2 = 24  # left wheel
    global in1
    in1 = 23  # left wheel
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    global in3
    in3 = 17  # right wheel
    global in4
    in4 = 27  # right wheel
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    global en1
    en1 = 25  # left wheel
    global en2
    en2 = 22  # right wheel
    global solenoid_pin
    solenoid_pin = 4
    global temp1
    temp1 = 1
    GPIO.setup(en1, GPIO.OUT)
    GPIO.setup(en2, GPIO.OUT)
    global p1
    p1 = GPIO.PWM(en1, 1000)
    global p2
    p2 = GPIO.PWM(en2, 1000)
    p1.start(100)
    p2.start(100)
    pwm_sol.start(0)


def light_number(number: int):
    if number > 99 or number < 0:
        pass
    else:

        digit1 = int(number / 10)
        digit2 = number - digit1 * 10

        while True:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(digit_pins, GPIO.OUT)
            GPIO.output(digit_pins, [1, 0])
            GPIO.output(segments, binary_dict[str(digit1)])
            time.sleep(0.01)

            GPIO.output(digit_pins, [0, 1])
            GPIO.output(segments, binary_dict[str(digit2)])
            time.sleep(0.01)
            break


class Stepper():
    def __init__(self):
        self.DIR = 20
        self.STEP = 21
        self.MODE1 = 26
        self.MODE2 = 19
        self.MODE0 = 13
        self.CW = 1
        self.CCW = 0
        self.SPR = 6400  # 360/1.8 => steps per revolution
        self.step_angle = 0.05625  # Stepper motor step angle (From spec sheet)
        self.rotation_time = 0.5  # time it takes to complete a revolution in seconds

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.MODE1, GPIO.OUT)
        GPIO.setup(self.MODE2, GPIO.OUT)
        GPIO.setup(self.MODE0, GPIO.OUT)
        GPIO.output(self.DIR, self.CW)
        GPIO.output(self.MODE1, GPIO.HIGH)
        GPIO.output(self.MODE2, GPIO.HIGH)
        GPIO.output(self.MODE0, GPIO.LOW)

    def Rotate(self, angle, direction):
        step_count = int(angle / self.step_angle)
        delay = 0.0001  # delay time between each step
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.output(self.DIR, direction)

        for x in range(step_count):
            GPIO.setup(self.STEP, GPIO.OUT)
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(delay)

        sleep(0.5)

        GPIO.output(self.DIR, False)
        GPIO.output(self.STEP, False)


def position():
    recognizer = sr.Recognizer()

    while True:

        try:

            with sr.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio)
                text = text.lower()

                if text == "left":
                    stepper.Rotate(50, CCW)
                    print("left")
                    break
                elif text == "right":
                    stepper.Rotate(50, CW)
                    print("right")
                    break
                else:
                    # stepper.Rotate(0, CW)
                    print("centre")
                    break

        except sr.UnknownValueError():

            recognizer = sr.Recognizer()
            continue


def speed():
    recognizer2 = sr.Recognizer()

    while True:
        try:

            with sr.Microphone() as mic:

                recognizer2.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer2.listen(mic)

                text2 = recognizer2.recognize_google(audio)
                text2 = text2.lower()

                if text2 == "slow":
                    p1.ChangeDutyCycle(25)
                    p2.ChangeDutyCycle(25)
                    print("slow")
                    break
                elif text2 == "average":
                    p1.ChangeDutyCycle(50)
                    p2.ChangeDutyCycle(50)
                    print("average")
                    break
                elif text2 == "fast":
                    p1.ChangeDutyCycle(100)
                    p2.ChangeDutyCycle(100)
                    print("fast")
                    break

        except sr.UnknownValueError():

            recognizer2 = sr.Recognizer()
            continue


def voice():
    ball_num = 5
    position()
    speed()

    if (temp1 == 1):
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)

        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    while (ball_num > 0):
        print("Running")
        light_number(ball_num)
        pwm_sol.ChangeDutyCycle(100)
        time.sleep(0.5)
        pwm_sol.ChangeDutyCycle(0)
        time.sleep(0.5)
        ball_num = ball_num - 1

    if (ball_num == 0):
        GPIO.setmode(GPIO.BCM)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)


GPIO.cleanup()


