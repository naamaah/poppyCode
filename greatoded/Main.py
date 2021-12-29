import sys
import time
import random
import tkinter as tk
from Poppy import Poppy
from Camera import Camera
from tts import TTS
import Settings as s #Global settings variables
import simulator
import threading
import os

if __name__ == '__main__':
    # Settings for exercises
    language = 'Hebrew'
    gender = 'Female'
    s.female=False
from GUI2 import Screen, FullScreenApp
import Excel as excel
    s.isCamera=False #False - No camera, True- there is camera
    s.numberOfWorkout=0

    s.realsense_path = "C:\\Users\\TEMP.NAAMA\\Documents\\nuitrack-sdk-master\\Examples\\nuitrack_console_sample\\out\\build\\x64-Debug\\nuitrack_console_sample.exe"
    #s.realsense_path = R'C:/PycharmProjects/greatoded/nuitrack/Examples/nuitrack_console_sample/out/build/x64-Debug/nuitrack_console_sample.exe'
    #s.excel_path = R'C:/PycharmProjects/greatoded/excel_folder/'
    #s.general_path = R'C:/PycharmProjects/greatoded/'
    #audiopath = s.general_path + 'audio files/'
    s.excel_path = R'C:/Git/poppyCode/greatoded/excel_folder/'
    s.general_path = R'C:/Git/poppyCode/greatoded/'
    s.pic_path = s.general_path + 'Pictures/'
    s.audio_path =s.general_path + 'audio files/' + '/' +language + '/' + gender + '/'

    s.clickrelax=False
    s.exercies_amount=1
    s.relax=None
    s.waved = False
    s.pickWeights = False
    s.finish_workout = False
    s.rep = 2# Number of repetitions for exercises - the robot doing
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

    s.cogGameCount=0
    simulator.createSim()
    time.sleep(5)
    excel.create_workbook()

    s.repeat_again=None
    s.robot = Poppy("poppy")
    if (s.isCamera==True):
        s.camera = Camera()
        s.camera.start()
    s.facemove=False
    s.tts = TTS("tts")

    s.tts.start()
    s.robot.start()
    s.screen = Screen()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()

    s.tts.join()
    print(s.tts.is_alive())
    s.robot.join()
    print(s.robot.is_alive())
    print("finished main loop")

    print(threading.enumerate())





    #raise SystemExit
    #sys.exit()
    #exit()
    #quit()
    #os._exit()
