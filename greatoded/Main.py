# import sys
import time
import random
import tkinter as tk
#from PoppySim import Poppy #simulator
from PoppyRobotNew import PoppyRobot #real robot
from PoppySim import PoppySim #simulator
from Camera import Camera #nuitrack+realsense
#from CameraNew import CameraNew #webcemara and mediaPipe
#from mediaPipe import Detection
from tts import TTS
import Settings as s #Global settings variables
import simulator
# import threading
# import os
from GUI2 import Screen, FullScreenApp
import Excel as excel
import pandas as pd
import threading

if __name__ == '__main__':
    # Settings for exercises - to change every run of the code!!!!
    s.robotNumber = "3"
    language = 'Hebrew'
    gender = 'Female'
    # gender = 'Male'
    if (gender == 'Female'):
        s.female = True
    else:
        s.female=False
    s.isCamera=False #False - No camera, True- there is camera
    s.isRobot=False #False - simulator, True- real robot
    # TBA
    s.subjectNum = random.randint(0, 1200)
    s.sessionNumber = 1
    s.TBALevel=3 #1-Low, 2-Medium, 3-HighOriginal
    s.exercies_amount=3

    #permenent - no need to change!
    s.realsense_path = R'C:\git\poppyCode\greatoded\nuitrack\Examples\nuitrack_console_sample\out\build\x64-Debug\nuitrack_console_sample.exe'
    s.excel_path = R'C:/Git/poppyCode/greatoded/excel_folder/'
    s.general_path = R'C:/Git/poppyCode/greatoded/'
    s.pic_path = s.general_path + 'Pictures/'
    s.audio_path = s.general_path + 'audioFiles/' +language + '/' + gender + '/'


    s.clickrelax=False
    s.waved = False
    s.finish_workout = False
    s.rep=6 # Number of repetitions for exercises - the robot doing and the user need to do - update in the code
    s.req_exercise = ""
    s.str_to_say = ""
    s.exercises_session1=[]
    s.exercises_session2=[]
    s.chance=False
    s.current_count=0 #save the last repetition of the user.
    s.demo=True #in the beggining is demonstration TBA3
    s.Q1_answer = None
    s.Q2_answer = None
    s.Q3_answer = None
    s.whichExercise_Q2 = None
    s.whichExercise_Q3 = None
    s.weight=""

    if (s.isCamera==True):
        s.camera = Camera()
        s.camera.start()

    if (s.isRobot==False):
        simulator.createSim()
        time.sleep(10)
        s.robot = PoppySim('poppy')
    else:
        s.robot = PoppyRobot('poppy')

    excel.create_workbook()
    s.repeat_again=None

    s.tts = TTS()
    s.robot.start()
    s.screen = Screen()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()
    print("finished main loop")
    print(threading.enumerate())

    # #Level for cognitive game
    #     s.words_number = 4 #game1
    #     s.light_tiles_num = 7 #game2
    #     s.shape_number = 2 #game 4
    #     s.words_number_color = 4 #game5
    #     #math game - game3
    #     s.low_addsub = 10 #level 1:1 level2:10 level3:10
    #     s.high_addsub = 50 #level 1:50 level2:50 level3:100
    #     s.low_mul_first = 1 #level 1:1 level2:1 level3:1
    #     s.high_mul_first = 5 #level 1:5 level2:5 level3:9
    #     s.low_mul_second = 10 #level 1:2 level2:10 level3:10
    #     s.high_mul_second = 50 #level 1:6 level2:50 level3:50

    # boolean not relevant
    # s.relax=False #if i want to use realx exrcise change to None
    # s.pickWeights = False
    # s.clickedTryAgain = False
    # s.cogGame = False
    # s.numberOfWorkout=0

