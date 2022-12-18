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
from GUI import Screen, FullScreenApp
import Excel as excel
import pandas as pd
import threading

if __name__ == '__main__':
    # Settings for exercises - to change every run of the code!!!!
    s.robotNumber = "1"
    language = 'Hebrew'
    gender = 'Female'
    #gender = 'Male'
    if (gender == 'Female'):
        s.female = True
    else:
        s.female=False
    s.isCamera=True #False - No camera, True- there is camera
    s.isRobot=True #False - simulator, True- real robot
    # TBA
    s.subjectNum = random.randint(0, 1200)
    s.sessionNumber = 1
    s.TBALevel=2 #1-Low, 2-highNew, 3-HighOriginal
    s.exercies_amount=6

    #permenent - no need to change!
    s.realsense_path = R'C:\git\poppyCode\Naama\nuitrack\Examples\nuitrack_console_sample\out\build\x64-Debug\nuitrack_console_sample.exe'
    s.excel_path = R'C:/Git/poppyCode/Naama/excel_folder/'
    s.general_path = R'C:/Git/poppyCode/Naama/'
    s.pic_path = s.general_path + 'Pictures/'
    s.audio_path = s.general_path + 'audioFiles/' +language + '/' + gender + '/'


    s.clickrelax=False
    s.waved = False
    s.finish_workout = False
    s.rep=6 # Number of repetitions for exercises - the robot doing and the user need to do - update in the code
    s.req_exercise = ""
    s.str_to_say = ""
    # s.exercises_session1=[]
    # s.exercises_session2=[]
    s.chance=False
    s.current_count=0 #save the last repetition of the user.
    s.demo=True #in the beggining is demonstration TBA3
    s.finish_exercise=False
    s.Q1_answer = None
    s.Q2_answer = None
    s.Q3_answer = None
    s.whichExercise_Q2 = None
    s.whichExercise_Q3 = None
    s.weight=""
    s.Q_rep=None

    if (s.isCamera==True):
        s.camera = Camera()
        s.camera.start()
        # forMediaPipe
        # s.current_joint_list = pd.DataFrame()
        # s.current_frame = 0
        # s.prev_frame = 0
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



