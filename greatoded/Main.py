# import sys
import time
import random
import tkinter as tk
from Poppy import Poppy #simulator
from PoppyRobot import PoppyRobot #real robot
from Camera import Camera #nuitrack+realsense
from CameraNew import CameraNew #webcemara and mediaPipe
from mediaPipe import Detection
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
    # Settings for exercises
    language = 'Hebrew'
    gender = 'Female'
    s.female=False
    s.isCamera=False #False - No camera, True- there is camera
    s.isMediaPipe=False #false-Nuitrack(Camera), True-mediaPipe(CameraNew)
    s.isRobot=False #False - simulator, True- real robot
    s.numberOfWorkout=0

    #s.realsense_path="C:\\Users\\owner\\Documents\\nuitrack-sdk-master\\Examples\\nuitrack_console_sample\\out\\build\\x64-Debug\\nuitrack_console_sample.exe"
    s.realsense_path = R'C:\git\poppyCode\greatoded\nuitrack\Examples\nuitrack_console_sample\out\build\x64-Debug\nuitrack_console_sample.exe'
    s.excel_path = R'C:/Git/poppyCode/greatoded/excel_folder/'
    s.general_path = R'C:/Git/poppyCode/greatoded/'
    s.pic_path = s.general_path + 'Pictures/'
    s.audio_path = s.general_path + 'audioFiles/' +language + '/' + gender + '/'

    s.clickrelax=False
    s.exercies_amount=4
    s.relax=False #if i want to use realx exrcise change to None
    s.waved = False
    s.pickWeights = False
    s.finish_workout = False
    s.rep =4# Number of repetitions for exercises - the robot doing
    s.req_exercise = ""
    s.str_to_say = ""
    s.clickedTryAgain = False
    s.cogGame = False

#Level for cognitive game
    s.words_number = 4 #game1
    s.light_tiles_num = 7 #game2
    s.shape_number = 2 #game 4
    s.words_number_color = 4 #game5
    #math game - game3
    s.low_addsub = 10 #level 1:1 level2:10 level3:10
    s.high_addsub = 50 #level 1:50 level2:50 level3:100
    s.low_mul_first = 1 #level 1:1 level2:1 level3:1
    s.high_mul_first = 5 #level 1:5 level2:5 level3:9
    s.low_mul_second = 10 #level 1:2 level2:10 level3:10
    s.high_mul_second = 50 #level 1:6 level2:50 level3:50

    if (s.isCamera==True):
        if(s.isMediaPipe==True): #cameraNew
            s.current_joint_list = pd.DataFrame()
            s.current_frame_from_joint_list = 0
            s.prev_frame_from_joint_list = 0
            detection = Detection()
            detection.start()
            s.camera = CameraNew()
            s.camera.start()
        else: #camera
            s.camera = Camera()
            s.camera.start()

    if (s.isRobot==False):
        simulator.createSim()
        time.sleep(10)
        s.robot = Poppy("poppy")
    else:
        s.robot = PoppyRobot("poppy")

    excel.create_workbook()
    s.repeat_again=None
    #s.facemove=False #not relevant

    s.tts = TTS()
    #s.tts.say_no_wait()
    s.robot.start()
    s.screen = Screen()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()
    print("finished main loop")
    print(threading.enumerate())
