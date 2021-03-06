# test_model.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey,ReleaseKey,ReleaseAll,keydict
from alexnet import alexnet
from getkeys import key_check
from keydefs import press_keys

import random

WIDTH = 400
HEIGHT = 300
LR = 1e-3
EPOCHS = 6
# !!!!! You know what to do with this by now.
training_id = 'BarnabusX002'
MODEL_NAME = 'pythonplay-{}-{}-epochs.model'.format(training_id,EPOCHS)

t_time = 0.09

'''
def straight():
##    if random.randrange(4) == 2:
##        ReleaseKey(W)
##    else:
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    #ReleaseKey(W)
    ReleaseKey(D)
    #ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(A)

def right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    #ReleaseKey(W)
    #ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(D)
'''


model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    last_keys = []
    while(True):
        
        if not paused:
            # 800x600 windowed mode
            #screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
            screen = grab_screen(region=(0,40,800,640))
            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            screen = cv2.resize(screen, (400,300))

            prediction = model.predict([screen.reshape(400,300,3)])[0]
            #print(prediction)

            threshold = 0.1

            keystage = []
            for i in range(len(prediction)):
            	if prediction[i] > threshold:
            		keystage.append(i)

            '''
            if len(keystage) > 2:
                largest = max(keystage)
                largest2 = max(item for item in keystage if item < largest)
                keystage = []
                keystage.append(largest)
                keystage.append(largest2)
            '''
            press_keys(keystage, last_keys)
            last_keys = keystage

            '''
            turn_thresh = .75
            fwd_thresh = 0.70

            if prediction[1] > fwd_thresh:
                straight()
            elif prediction[0] > turn_thresh:
                left()
            elif prediction[2] > turn_thresh:
                right()
            else:
                straight()
            '''

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseAll()
                time.sleep(1)

main()       