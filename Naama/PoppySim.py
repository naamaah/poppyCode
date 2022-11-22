import sys
from PoppyRobotNew import PoppyRobot #real robot
from numpy.core._multiarray_umath import ndarray
from GUI2 import Screen, FullScreenApp
from pypot.creatures import PoppyTorso
import Settings as s
import time
import threading
import random
from GUI2 import StartPage, weightPage, TryAgainPage, BlankPage, GoodbyePage, ExercisePage, lastquestion, shutdown_win,\
    Q1_page, Q2_page, Q3_page,Q1_New_page, ExamplePage
from datetime import date,datetime
import numpy as np
from numpy import savetxt
from numpy import loadtxt
import os
import Excel
import simulator
from tts import TTS
from Camera import Camera
import math

class PoppySim(PoppyRobot):
    def __init__(self, name):
        PoppyRobot.__init__(self, name)
        print("finised init robot - Sim class")

    def robotType(self):
        self.poppy = PoppyTorso(simulator='vrep')  # for simulator

    def closeRobot(self):
        print("sim robot finished")
        simulator.closeSim()