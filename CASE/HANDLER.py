#-*- coding: utf-8 -*-
from LEDCONTROLLER import LedController
from LEDCONTROLLER import initializer
import time
import alsaaudio as audio
import signal
import pickle
import os
import skywriter

menu = "led"
some_value = 7000
some_value2 = 4000
i = 5
ledlist = ""
allled = [13, 18, 19, 20, 21, 23, 24, 25, 26]
isplaying = True
dimming = 100
initializer()

def handling(i):
    try:
        global ledlist
        LedController().LedtoTurnOff(allled)
        with open('courses/courses.list', 'r') as coursesfile:
            clist  = pickle.load(coursesfile)
        if type(clist) == list:
            ledlist = LedController().HandleCourses(clist, i)
            print ledlist
            if type(ledlist) == list or type(ledlist) == tuple:
                LedController().LedtoTurnOn(ledlist,dimming)
            else:
                print "LedList not acceptable"
        else:
            print "List not acceptable"
            print clist
    except Exception as e:
        print "Erreur lors du processus" 
        ledlist = ""
        print e
        time.sleep(1)

@skywriter.flick()
def flick(start,finish):
    global i
    global menu
    global allled
    global isplaying

    print('Got a flick!', start, finish)
    if start == "east" and finish == "west":
        if menu == "led":
            i = i-1
            if i == -1:
                i = 0
            handling(i)
            print "handling " + str(i-5)
        elif menu == "music":
            os.system("mpc prev")

    elif start == "west" and finish == "east":
        if menu == "led":
            i = i+1
            if i == 15:
                i = 14
            handling(i)
            print "handling " + str(i-5)
        elif menu == "music":
            os.system("mpc next")

    elif start == "south" and finish == "north":
        if menu == "led":
            i = 5
            handling(i)
            print "handling " + str(i-5)
        elif menu == "music":
            i = 5
            menu = "led"
            handling(i)
            print "handling " + str(i-5)

    elif start == "north" and finish == "south":
        if menu == "led":
            menu = "music"
            LedController().LedtoTurnOff(allled)
            for led in allled:
                LedController().LedtoTurnOn([led], 100)
                time.sleep(0.05)
        elif menu == "music":
            if isplaying == False:
                os.system("mpc toggle")
                isplaying = True
            elif isplaying == True:
                os.system("mpc toggle")
                isplaying = False


mixer = audio.Mixer('PCM', cardindex=0)

@skywriter.airwheel()
def spinny(delta):
    global ledlist
    global some_value
    global some_value2
    global dimming
    if menu == "music":
        some_value += delta
        if some_value < 0:
            some_value = 0
        if some_value > 8000:
            some_value = 8000
        print('New volume: ', some_value/80)
        mixer.setvolume(int(some_value/80))
        LedController().LedtoTurnOn(allled, int(some_value/80))

    elif menu == "led":
        some_value2 += delta
        if some_value2 < 50:
            some_value2 = 50
        if some_value2 > 4000:
            some_value2 = 4000
        print("New duty cycle: ", some_value2/40)
        dimming = int(some_value2/40)
        LedController().LedtoTurnOn(ledlist, dimming)

mixer.setvolume(87)
handling(0)
try:
    signal.pause()
except:
    LedController().exit()
#def spinny(delta):
#    angle += delta
#    print angle
#    if angle < 0:
#        angle = 0
#    if 340 <= angle - oldangle <= 380:
#        handling(i)
#        print "handling" + str(i)
#        angle = 0
#        oldangle = angle
