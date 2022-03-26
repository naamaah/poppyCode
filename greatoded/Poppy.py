import sys
from numpy.core._multiarray_umath import ndarray
#from pypot.creatures import PoppyHumanoid
from GUI2 import Screen, FullScreenApp
from pypot.creatures import PoppyTorso
import Settings as s
import time
import threading
import random
from GUI2 import StartPage, weightPage, TryAgainPage, BlankPage, GoodbyePage, ExercisePage, lastquestion, shutdown_win,\
    Q1_page, Q2_page, Q3_page
# \
#  begin_page,   StartPage_Relax, Relax_Page_ber, lastquestion_relax, relax_thl, relax_thr, relax_thd, facemovement_Relax, teeth, \
#     eyes, eyebrows, smile
from CognitiveGame1 import GameOneStart
from CognitiveGame2 import GameTwoStart
from CognitiveGame4 import GameFourStart
from CognitiveGame5 import GameFiveStart
from cognetivemission_math import introduction
from datetime import date,datetime
import numpy as np
from numpy import savetxt
from numpy import loadtxt
import os
import Excel
import simulator
from tts import TTS
from Camera import Camera
# #from playsound import playsound
# import winsound
import simpleaudio as sa
from pygame import mixer


class Poppy(threading.Thread):
    def __init__(self, name):
        print("Poppy class - init function")
        threading.Thread.__init__(self)
        self.name=name
        self.poppy = PoppyTorso(simulator='vrep')  # for simulator
        print("init robot - (Poppy class)")
        for m in self.poppy.motors:  # motors need to be initialized, False=stiff, True=loose
            m.compliant = False
        self.init_robot()
        print("finished init")

    def run(self):
        print("Poppy class - run function")
        print("hello wave, introduction - (Poppy class)")
        #For TBA levels
        if (s.sessionNumber==1):
            self.run_exercise(self.hello_waving, "hello")  # the robot wave
            s.tts.say_wait("Answer to Question")
            s.tts.say_no_wait("Q1")
            s.screen.switch_frame(Q1_page)
            while (s.Q1_answer==None):  # wait for participant to answer Q1
                continue
            s.tts.say_no_wait("Q2")
            s.screen.switch_frame(Q2_page)
            while (s.Q2_answer == None):  # wait for participant to answer Q2
                continue
            s.tts.say_no_wait("Q3")
            s.screen.switch_frame(Q3_page)
            while (s.Q3_answer == None):  # wait for participant to answer Q3
                continue
            s.tts.say_no_wait("Thanks for answer")
        else:
            self.run_exercise(self.hello_waving, "NoAudio")  # the robot wave
        self.exercise_run()
        print("done poppy")

    def exercise_run(self):
        print("Poppy class - exercise_run function")
        s.waved = False
        s.str_to_say = 'ready wave'
        s.tts.say_no_wait(s.str_to_say)
        s.screen.switch_frame(StartPage)
        while (not s.waved): # wait for participant to wave or to clicked on the screen
           continue
        time.sleep(1)
        s.screen.switch_frame(BlankPage)
        print("Let's start! - (Poppy class)")
        s.str_to_say='lets start'
        s.tts.say_wait(s.str_to_say)
        all_exercise_names=[self.raise_arms_horizontally_separate,self.raise_arms_horizontally,self.bend_elbows,self.raise_arms_forward_static,
                        self.raise_arms_bend_elbows,self.raise_arms_horizontally_turn, self.raise_arms_forward, self.raise_arms_forward_separate,
                        self.raise_arms_90_and_up,self.raise_arms_and_lean_dynmic, self.open_arms_and_forward, self.raise_hands_and_fold_backward,
                        self.open_hands_and_raise_up, self.open_and_close_arms_90, self.open_and_close_arms_90, self.open_and_down_arms_90,
                        self.to_90_and_down_arms, self.raise_arms_forward_turn]

        right_exercise_names = [self.raise_right_arm_horiz,self.raise_right_arm_forward,self.raise_right_arm_and_lean_dynmic]

        left_exercise_names = [self.raise_left_arm_horiz,self.raise_left_arm_forward,self.raise_left_arm_and_lean_dynmic]

        # exercise_onlyTwoHandTogether = [self.raise_arms_horizontally, self.bend_elbows,
        #                   self.raise_arms_bend_elbows, self.raise_arms_forward,
        #                   self.raise_arms_90_and_up, self.open_arms_and_forward,
        #                   self.raise_hands_and_fold_backward,
        #                   self.open_hands_and_raise_up, self.open_and_close_arms_90]

        if (s.sessionNumber==1):
            #choose randomly the exercise for this session
            chosen_exercises = []
            while len(chosen_exercises) < s.exercies_amount:
                ex = random.choice(all_exercise_names)
                if ex.amount != 2:  # only two hands
                    if ex not in chosen_exercises:
                        chosen_exercises.append(ex)
            print (chosen_exercises)
            s.rep=random.randint(9,12)
            print("number of repetition"+str(s.rep))
        elif (s.sessionNumber==2):
            #questions!
            #question 3
            if (s.Q3_answer=='a'):
                s.whichExercise_Q3 = 'Weights'
            elif (s.Q3_answer=='c'): #for now withput weights
                #s.pickWeights=random.choice([True, False])
                s.whichExercise_Q3 = 'No Weights'
            # else: # s.Q3_answer=='b'
            #     s.whichExercise='Static'

            # question 2
            if (s.Q2_answer == 'a'): #problem with left
                s.whichExercise_Q2 = 'Right'
            elif (s.Q2_answer == 'b'):
                s.whichExercise_Q2 = 'Left'
            else:
                s.whichExercise_Q2 = 'All'

            # question 1
            if (s.Q1_answer == 'a'):
                if (s.whichExercise_Q3 == 'Weights'):
                    s.rep=random.randint(7,8)
                else:
                    s.rep = 9
            elif (s.Q1_answer == 'b'):
                if (s.whichExercise_Q3 == 'Weights'):
                    s.rep = random.randint(8, 9)
                else:
                    s.rep = 10
            elif (s.Q1_answer == 'c'):
                if (s.whichExercise_Q3 == 'Weights'):
                    s.rep = random.randint(9, 10)
                else:
                    s.rep = 11
            else: # d
                if (s.whichExercise_Q3 == 'Weights'):
                    s.rep = random.randint(10, 11)
                else:
                    s.rep = 12

            #exercise chosen:
            chosen_exercises = []
            while len(chosen_exercises) < s.exercies_amount:
                if(s.whichExercise_Q2 == 'Right'):
                  ex = random.choice(right_exercise_names)
                  if ex not in chosen_exercises:
                    chosen_exercises.append(ex)
                elif(s.whichExercise_Q2 == 'Left'):
                    ex = random.choice(left_exercise_names)
                    if ex not in chosen_exercises:
                        chosen_exercises.append(ex)
                else: #no problem - need to fix that it wpnt be the sem exercise as pervious session
                    ex = random.choice(all_exercise_names)
                    if ex not in chosen_exercises:
                        chosen_exercises.append(ex)
            print(chosen_exercises)
            print("number of repetition" + str(s.rep))
        # else: # session 3

        #### RUN WORKOUT
        count = 0
        print("Exercises - (Poppy class)")
        print("ExercisePage")
        s.screen.switch_frame(ExercisePage)
        for e in chosen_exercises:
            count = count + 1
            print(exercise_name)
            if e.amount == 2: #for exercise with two separate hands
                self.run_exercise(e, "")
            else:
                exercise_name = getattr(e, "instructions")
                self.run_exercise(e, exercise_name)
        self.finish_workout()

    def init_robot(self):
        print("Poppy class - init_robot function")
        for m in self.poppy.motors:
            if not m.name == 'r_elbow_y' and not m.name == 'l_elbow_y' and not m.name == 'head_y':
                m.goto_position(0, 1, wait=True)
        self.poppy.head_y.goto_position(-20,1,wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)
        time.sleep(1)
        print("Poppy class - finished init_robot function")

    #run exercise
    def run_exercise(self, exercise, exercise_name):
        print("Poppy class - run_exercise function "+str(exercise.number))
        s.success_exercise = False
        s.str_to_say = exercise_name
        s.req_exercise = exercise.__name__
        s.tts.say_wait(s.str_to_say)
        exercise()  # the function of the current exercise.
        if (exercise_name != "hello"):
            s.req_exercise = ""
            time.sleep(4)

    def finish_workout(self):
        print("Poppy class - finish_workout function")
        s.numberOfWorkout=s.numberOfWorkout+1
        time.sleep(1)
        s.screen.switch_frame(GoodbyePage)
        s.str_to_say = 'goodbye'
        s.tts.say_wait(s.str_to_say)
        Excel.wf_exercise("success"+str(s.numberOfWorkout))
        Excel.close_workbook()
        mylist=["good","bye"]
        # with open(s.general_path+"data_shik.csv", "ab") as f:
        #     f.write(b"\t")
        #     savetxt(f, mylist, fmt='%s')
        s.screen.switch_frame(shutdown_win)
        s.str_to_say='turn off electricity'
        s.tts.say_wait(s.str_to_say)
        #time.sleep(5)
        for m in self.poppy.motors:  # need to be initialized for the real robot. False=stiff, True=loose
            m.compliant = True
        print("finished robot - ")
        s.finish_workout = True
        simulator.closeSim()
        s.screen.quit()
        # time.sleep(4)
        # os.system('TASKKILL /IM main.py') #only for simulation
        #os.system('shutdown -s -t 0') #only for the real robot.

    # define attributes for a function
    def func_attributes(**attrs):
        def attributes(f):
            for k, v in attrs.items():
                setattr(f, k, v)
            return f
        return attributes

    #-----------------------Exercises---------------------------#
    @func_attributes(number='hello')
    def hello_waving(self):
        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-80, 1.5, wait=False)
        for i in range(3):
            self.poppy.r_arm[3].goto_position(-35, 0.6, wait=True)
            self.poppy.r_arm[3].goto_position(35, 0.6, wait=True)
        self.finish_waving()

    def finish_waving(self):
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)

    # EX1 - Right Arm Horizontally and Left arm Horizontally
    @func_attributes(number=1 ,amount=2, instructions="raise arms horizontally separate")
    def raise_arms_horizontally_separate(self):
        self.run_exercise(self.raise_right_arm_horiz, "raise right arm horizontally")
        self.run_exercise(self.raise_left_arm_horiz, "raise left arm horizontally")

    @func_attributes(number='1L' ,instructions="raise left arm horizontally")
    def raise_left_arm_horiz(self):
        for i in range(s.rep):
            right_hand_up = [self.poppy.r_shoulder_x.goto_position(-90, 1.7, wait=False),
                             self.poppy.r_elbow_y.goto_position(90, 1.7, wait=False)] #1.7
            time.sleep(2)
            right_hand_down = [self.poppy.r_shoulder_x.goto_position(0, 1.7, wait=False),
                               self.poppy.r_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break

    @func_attributes(number='1R',instructions="raise right arm horizontally")
    def raise_right_arm_horiz(self):
        for i in range(s.rep):
            hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.7, wait=False),
                        self.poppy.l_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.7, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break

    # EX2 - Two Arms Horizontally
    @func_attributes(number=2, amount=1, instructions="raise arms horizontally")
    def raise_arms_horizontally(self):
        for i in range(s.rep):
            hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                        self.poppy.r_elbow_y.goto_position(90, 1, wait=False)] #1.5
            time.sleep(1)
            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                          self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(1)
            if (s.success_exercise):
                break

    # EX3 - Bend Elbows
    @func_attributes(number=3, amount=1, instructions="bend elbows")
    def bend_elbows(self):
        #s.str_to_say = exercise_name
        for i in range(s.rep):
            band = [self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False),self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)]
            time.sleep(0.5)
            down = [self.poppy.r_arm[3].goto_position(85, 1.5, wait=False), self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)]
            time.sleep(0.5)
            if (s.success_exercise):
                break


    # EX4 - Static hands forward
    @func_attributes(number=4, amount=1, instructions="raise arms forward static")
    def raise_arms_forward_static(self):
        static=[self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False),
                self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False),
                self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False),
                self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)]
        time.sleep(12)

        #back to position
        initPos=[self.poppy.l_arm_z.goto_position(0, 1.5, wait=False),
                self.poppy.r_arm_z.goto_position(0, 1.5, wait=False),
                self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False),
                self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)]

    # EX5 - Raise Arms Bend Elbows
    @func_attributes(number=5, amount=1, instructions="raise arms bend elbows")
    def raise_arms_bend_elbows(self):
        self.open_hands_aside_move()
        for i in range(s.rep):
            l_hand = [self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.l_arm_z.goto_position(-90, 2, wait=False),
                      self.poppy.l_shoulder_x.goto_position(50, 2, wait=False),
                      self.poppy.l_elbow_y.goto_position(-50, 2, wait=False)]
            r_hand = [self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.r_arm_z.goto_position(90, 2, wait=False),
                      self.poppy.r_shoulder_x.goto_position(-50, 2, wait=False),
                      self.poppy.r_elbow_y.goto_position(-50, 2, wait=False)]
            time.sleep(2)
            self.open_hands_aside_move()
            if (s.success_exercise):
                break
        time.sleep(2)

        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=True)


    # EX6 - Raise Arms Horizontally Turn_Hands
    @func_attributes(number=6, amount=1, instructions="raise arms horizontally turn hands")
    def raise_arms_horizontally_turn(self):
        self.open_hands_aside_move()
        for i in range(4):
            twisFirst = [self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False),
                              self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)]
            twisSecond=[self.poppy.l_arm_z.goto_position(90, 1.5, wait=False),
                              self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)]

        time.sleep(1)
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=True)

    def open_hands_aside_move(self):
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(1)

    # EX7 - Raise arms forward
    @func_attributes(number=7, amount=1, instructions="raise arms forward")
    def raise_arms_forward(self):
        for i in range(s.rep):
            forwaed=[self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False),
                    self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False),
                    self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False),
                    self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)]
            time.sleep(1)
            down=[self.poppy.l_arm_z.goto_position(0, 1.5, wait=False),
                self.poppy.r_arm_z.goto_position(0, 1.5, wait=False),
                self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False),
                self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)]
            time.sleep(1)
            if (s.success_exercise):
                break

    # EX8 - Raise arms forward speratally
    @func_attributes(number=8, amount=2, instructions="raise arms forward separate")
    def raise_arms_forward_separate(self):
        self.run_exercise(self.raise_right_arm_forward, "raise right arm forward")
        self.run_exercise(self.raise_left_arm_forward, "raise left arm forward")

    @func_attributes(number='8L', instructions="raise left and forward")
    def raise_left_arm_forward(self):
        for i in range(s.rep):
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)
            time.sleep(1)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break

    @func_attributes(number='8R', instructions="raise right and forward")
    def raise_right_arm_forward(self):
        for i in range(s.rep):
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=True)
            time.sleep(1)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break

    # EX9 - Raise arms 90 and up
    @func_attributes(number=9, amount=1, instructions="raise arms 90 and up")
    def raise_arms_90_and_up(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        for i in range(s.rep):
            nine=[self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False),
                self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)]
            time.sleep(1)
            up=[self.poppy.r_shoulder_x.goto_position(-150, 1.5, wait=False),
                self.poppy.l_shoulder_x.goto_position(150, 1.5, wait=False),
                self.poppy.r_elbow_y.goto_position(60, 1.5, wait=False),
                self.poppy.l_elbow_y.goto_position(60, 1.5, wait=True)]
            time.sleep(1)
            if (s.success_exercise):
                break
        #init
        time.sleep(1)
        self.poppy.l_arm_z.goto_position(0, 1, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1., wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    # # EX10 raise arms and lean
    # @func_attributes(number=10, amount=2, instructions="raise arms and lean")
    # def raise_arms_and_lean(self):
    #     #mirror
    #     self.run_exercise(self.raise_right_arm_and_lean, "raise left arm and lean")
    #     self.run_exercise(self.raise_left_arm_and_lean, "raise right arm and lean")
    #
    # @func_attributes(number='10L', instructions="raise left arm and lean")
    # def raise_left_arm_and_lean(self):
    #     self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
    #     self.poppy.l_shoulder_x.goto_position(150, 1.5, wait=False)
    #     self.poppy.l_elbow_y.goto_position(30, 1.5, wait=True)#left hands in the position
    #     self.poppy.bust_x.goto_position(20, 1.5, wait=False)
    #     self.poppy.bust_y.goto_position(0, 1.5, wait=False)
    #     self.poppy.r_shoulder_x.goto_position(-30, 1.5, wait=True)
    #     time.sleep(10)
    #     #init
    #     self.poppy.l_arm_z.goto_position(00, 1.5, wait=False)
    #     self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
    #     self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
    #     self.poppy.bust_x.goto_position(0, 1.5, wait=False)
    #     self.poppy.bust_y.goto_position(0, 1.5, wait=False)
    #     self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
    #     self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
    #     time.sleep(1)
    #
    # @func_attributes(number='10R', instructions="raise right arm and lean")
    # def raise_right_arm_and_lean(self):
    #     self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
    #     self.poppy.r_shoulder_x.goto_position(-150, 1.5, wait=False)
    #     self.poppy.r_elbow_y.goto_position(30, 1.5, wait=True)
    #     self.poppy.bust_x.goto_position(-20, 1.5, wait=False)
    #     self.poppy.bust_y.goto_position(0, 1.5, wait=False)
    #     self.poppy.l_shoulder_x.goto_position(30, 1.5, wait=True)
    #     time.sleep(10)
    #     self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
    #     self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
    #     self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
    #     self.poppy.bust_x.goto_position(0, 1.5, wait=False)
    #     self.poppy.bust_y.goto_position(0, 1.5, wait=False)
    #     self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
    #     self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
    #     time.sleep(1)

    # EX33 raise arms and lean and repeat
    @func_attributes(number=10, amount=2, instructions="raise arms and lean")
    def raise_arms_and_lean_dynmic(self):
        # mirror
        self.run_exercise(self.raise_right_arm_and_lean_dynmic, "raise right arm and lean")
        self.run_exercise(self.raise_left_arm_and_lean_dynmic, "raise left arm and lean")

    @func_attributes(number='10L', instructions="raise left arm and lean")
    def raise_left_arm_and_lean_dynmic(self):
        for num in range(s.rep):
            self.poppy.r_arm_z.goto_position(-120, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-120, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(-35, 1.5, wait=True)
            self.poppy.bust_x.goto_position(-20, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(30, 1.5, wait=True)
            # next move
            time.sleep(1)
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.bust_x.goto_position(0, 1.5, wait=True)
            if (s.success_exercise):
                break

        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.bust_x.goto_position(0, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        time.sleep(1)

    @func_attributes(number='10R', instructions="raise right arm and lean")
    def raise_right_arm_and_lean_dynmic(self):
        for num in range(s.rep):
            self.poppy.l_arm_z.goto_position(140, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(120, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(-48, 1.5, wait=True)  # left hands in the position
            self.poppy.bust_x.goto_position(20, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-30, 1.5, wait=True)
            time.sleep(1)
            # next move
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.bust_x.goto_position(0, 1.5, wait=True)

            if (s.success_exercise):
                break

        # init
        self.poppy.l_arm_z.goto_position(00, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.bust_x.goto_position(0, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(1)

    # EX11 Raise hands, open horizontally and move forward
    @func_attributes(number=11, amount=1, instructions="open arms and move forward")
    def open_arms_and_forward(self):
        self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-90, 1.5, wait=True)
        for i in range(s.rep):
            self.open_hands_aside_move()
            time.sleep(0.5)
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break
        #init
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)

    # EX12 Raise hands and fold backward
    @func_attributes(number=12, amount=1, instructions="raise hands and fold backward")
    def raise_hands_and_fold_backward(self):
        self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=True)
        for i in range(s.rep):
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
            time.sleep(1)
            self.poppy.l_elbow_y.goto_position(-20, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break

        #         self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        #         self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        # up = [self.poppy.r_shoulder_x.goto_position(-150, 1.5, wait=False),
        #       self.poppy.l_shoulder_x.goto_position(150, 1.5, wait=False),
        #       self.poppy.r_elbow_y.goto_position(60, 1.5, wait=False),
        #       self.poppy.l_elbow_y.goto_position(60, 1.5, wait=True)]

        #init
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)

    # EX13 open hands and raise up
    @func_attributes(number=13, amount=1, instructions="open hands and raise up")
    def open_hands_and_raise_up(self):
        for i in range(s.rep):
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
            time.sleep(1)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(8, 1, wait=False)
            self.poppy.r_shoulder_x.goto_position(-8, 1, wait=False)
            self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-180, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)

    # EX14 open and close arms 90
    @func_attributes(number=14, amount=1, instructions="open and close arms 90")
    def open_and_close_arms_90(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        for i in range(s.rep):
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)

    @func_attributes(number=15, amount=1, instructions="NoAudio")
    def open_and_down_arms_90(self):
        for i in range(s.rep):
            self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break
        # init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)

    @func_attributes(number=16, amount=1, instructions="open and down arms 90")
    def to_90_and_down_arms(self):
        for i in range(s.rep):
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.r_shoulder_x.goto_position(0, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(0, 1, wait=True)

            time.sleep(1)
            if (s.success_exercise):
                break
        # init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)

    # EX17 raise_arms_forward_turn_hands
    @func_attributes(number=17, amount=1, instructions="raise arms forward turn hands")
    def raise_arms_forward_turn(self):
        self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False)
        self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False)
        self.poppy.l_arm_z.goto_position(-90, 2, wait=False)
        self.poppy.r_arm_z.goto_position(90, 2, wait=True)
        for i in range(s.rep):
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)

        time.sleep(0.3)
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 2, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 2, wait=True)

    #warmUp exercise
    @func_attributes(number=31, amount=2, instructions="")
    def head_circle(self):
        # mirror
        self.run_exercise(self.head_clockWise, "")
        self.run_exercise(self.head_anticlockwise, "")

    @func_attributes(number='31L', amount=1, instructions="")
    def head_anticlockwise(self):
        headZ_degree = [-100, -50, 0, 50, 100]
        for num in range(4):
            # down
            self.poppy.head_y.goto_position(8, 1, wait=False)
            for i in range(len(headZ_degree)):
                self.poppy.head_z.goto_position(headZ_degree[i], 1.3, wait=True)
            # up
            self.poppy.head_y.goto_position(-40, 1, wait=False)
            for i in range(len(headZ_degree)):
                self.poppy.head_z.goto_position(headZ_degree[len(headZ_degree) - 1 - i], 1.3, wait=True)

        #init
        self.poppy.head_y.goto_position(-20, 1, wait=False)
        self.poppy.head_z.goto_position(0, 1, wait=True)

    @func_attributes(number='31R', amount=1, instructions="")
    def head_clockWise(self):
        headZ_degree = [-100, -50, 0, 50, 100]
        for num in range(4):
            # down
            self.poppy.head_y.goto_position(8, 1, wait=False)
            for i in range(len(headZ_degree)):
                self.poppy.head_z.goto_position(headZ_degree[len(headZ_degree) - 1 - i], 1.3, wait=True)
            # up
            self.poppy.head_y.goto_position(-40, 1, wait=False)
            for i in range(len(headZ_degree)):
                self.poppy.head_z.goto_position(headZ_degree[i], 1.3, wait=True)

        # init
        self.poppy.head_y.goto_position(-20, 1, wait=False)
        self.poppy.head_z.goto_position(0, 1, wait=True)

    @func_attributes(number=32, amount=1, istruction="")
    def elbow_clockWise(self):
        # elboys -clockwise direction
        l_shoulderY = [-90, -90, -90, 30, 30]
        l_armZ = [-90, -90, -90, -5, -5]
        l_shoulderX = [50, 50, 50, 90, 90]
        l_elbowY = [-50, 0, 90, -10, -50]

        r_shoulderY = [-90, -90, -90, 30, 30]
        r_armZ = [90, 90, 90, 5, 5]
        r_shoulderX = [-50, -50, -50, -90, -90]
        r_elbowY = [-50, 0, 90, -10, -50]

        for num in range(10):
            for i in range(len(l_elbowY)):
                self.poppy.l_shoulder_y.goto_position(l_shoulderY[i], 1, wait=False)
                self.poppy.r_shoulder_y.goto_position(r_shoulderY[i], 1, wait=False)
                self.poppy.l_arm_z.goto_position(l_armZ[i], 1, wait=False)
                self.poppy.r_arm_z.goto_position(r_armZ[i], 1, wait=False)
                self.poppy.l_shoulder_x.goto_position(l_shoulderX[i], 1, wait=False)
                self.poppy.r_shoulder_x.goto_position(r_shoulderX[i], 1, wait=False)
                self.poppy.l_elbow_y.goto_position(l_elbowY[i], 1, wait=False)
                self.poppy.r_elbow_y.goto_position(r_elbowY[i], 1, wait=True)

        # init
        self.poppy.l_shoulder_y.goto_position(0, 1, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(0, 1, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)

    # EX33 raise arms and lean and repeat
    @func_attributes(number=33, amount=2, instructions="raise arms and lean")
    def raise_arms_and_lean_repeat(self):
        # mirror
        self.run_exercise(self.raise_right_arm_and_lean_repeat, "raise right arm and lean")
        self.run_exercise(self.raise_left_arm_and_lean_repeat, "raise left arm and lean")

    @func_attributes(number='33L', instructions="raise left arm and lean")
    def raise_left_arm_and_lean_repeat(self):
        for num in range(7):
            self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-150, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(30, 1.5, wait=True)
            self.poppy.bust_x.goto_position(-20, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(30, 1.5, wait=True)
            # next move
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.bust_x.goto_position(0, 1.5, wait=True)

        time.sleep(10)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.bust_x.goto_position(0, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        time.sleep(1)

    @func_attributes(number='33R', instructions="raise right arm and lean")
    def raise_right_arm_and_lean_repeat(self):
        for num in range(7):
            self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(150, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(30, 1.5, wait=True)  # left hands in the position
            self.poppy.bust_x.goto_position(20, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-30, 1.5, wait=True)
            #next move
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.bust_x.goto_position(0, 1.5, wait=True)

        # init
        self.poppy.l_arm_z.goto_position(00, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.bust_x.goto_position(0, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(1)

    @func_attributes(number=34, amount=1, instructions="")
    def back_strech_Dynmic(self):
        #open hand and 90
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(1)
        for i in range(5):
            self.poppy.abs_z.goto_position(70,2, wait=True)
            self.poppy.abs_z.goto_position(-70, 2, wait=True)

        #init
        self.poppy.abs_z.goto_position(0, 1, wait=True)
        self.poppy.r_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(0.5)

    # EX14 open and close arms 90
    @func_attributes(number=35, amount=1, instructions="open and close arms 90")
    def open_and_close_arms_90_dynamic(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        for i in range(5):
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
            time.sleep(1)
            # if (s.success_exercise):
            #     break
        # init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)



    @func_attributes(number=36, amount=1, instructions="open and close arms 90")
    def open_and_down_arms_90_dynamic(self):
        for i in range(s.rep):
            self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break
        # init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)

    # wormUp
    @func_attributes(number=30, amount=1, instructions="")
    def warmUp(self):
        self.head_circle()
        #self.elbow_clockWise() #not dood enough
        self.open_and_close_arms_90_dynamic()
        self.open_and_down_arms_90_dynamic()
        self.back_strech_Dynmic()
        self.raise_arms_and_lean_repeat()



    @func_attributes(number=41, amount=1, instructions="turn_head_left")
    def turn_head_left(self):
        #time.sleep(1.5)
        self.poppy.head_y.goto_position(0, 1, wait=False)
        self.poppy.head_z.goto_position(-45, 1, wait=True)
        time.sleep(7.4)
        self.poppy.head_z.goto_position(0,1,wait=True)
        time.sleep(1)

    @func_attributes(number=42, amount=1, instructions="turn_head_right")
    def turn_head_right(self):
        #time.sleep(1.5)
        self.poppy.head_y.goto_position(0, 1, wait=False)
        self.poppy.head_z.goto_position(45, 1, wait=True)
        time.sleep(6)
        self.poppy.head_z.goto_position(0, 1, wait=True)
        time.sleep(1)

    @func_attributes(number=43, amount=1, instructions="turn_head_down")
    def turn_head_down(self):
        #time.sleep(2.5)
        self.poppy.head_y.goto_position(20, 1.7, wait=True)
        time.sleep(6)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        time.sleep(2)

    def hands_up(self):
        self.poppy.l_shoulder_y.goto_position(-200, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-200, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(-10, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(10, 1.5, wait=False)
        self.poppy.head_y.goto_position(50,1.5,wait=True)
        time.sleep(1)

    @func_attributes(number=44, amount=1, instructions="")
    def left_band(self):
        self.hands_up()
        self.poppy.l_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-40, 1.5, wait=True)
        self.poppy.r_arm_z.goto_position(80, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(7)

        #init
        #init hands up
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        #init exe
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        self.init_robot()
        time.sleep(2)

    @func_attributes(number=45, amount=1, instructions="")
    def right_band(self):
        self.hands_up()
        self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(40, 1.5, wait=True)
        self.poppy.l_arm_z.goto_position(-70, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(7)

        # init
        #init hand up
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        #init exercise
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        self.init_robot()
        time.sleep(2)

    @func_attributes(number=46, amount=1, instructions="")
    def left_strech(self):
        #open to 90
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(1)

        self.poppy.abs_z.goto_position(-15, 1.5, wait=False)
        self.poppy.head_z.goto_position(50,1.5,wait=False)
        #left
        self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(-120, 1.5, wait=True)
        #right
        self.poppy.r_shoulder_y.goto_position(-50, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(30,1.5,wait=False)
        self.poppy.r_shoulder_x.goto_position(20, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(30, 1.5, wait=True)
        time.sleep(7)

        #init
        self.poppy.abs_z.goto_position(0, 1.5, wait=False)
        self.poppy.head_z.goto_position(0,1.5,wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0,1.5,wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        self.init_robot()
        time.sleep(1)

    @func_attributes(number=47, amount=1, instructions="")
    def right_strech(self):
        self.open_hands_aside_move()
        #right strech
        self.poppy.abs_z.goto_position(30, 1, wait=False)
        self.poppy.head_z.goto_position(-50,1,wait=False)
        #right
        self.poppy.r_shoulder_y.goto_position(-90, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(120, 1, wait=True)
        #left
        self.poppy.l_shoulder_y.goto_position(-50, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-30,1.5,wait=False)
        self.poppy.l_shoulder_x.goto_position(-20, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(30, 1.5, wait=True)
        time.sleep(7)

        #init
        self.poppy.abs_z.goto_position(0, 1, wait=False)
        self.poppy.head_z.goto_position(0, 1, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1, wait=True)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        self.init_robot()
        time.sleep(2)

    @func_attributes(number=48, amount=1, instructions="")
    def back_strech_static(self):
        #open hand and 90
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(2)

        self.poppy.abs_z.goto_position(70,1, wait=True)
        time.sleep(6)
        self.poppy.abs_z.goto_position(0, 1, wait=True)
        time.sleep(1)
        self.poppy.abs_z.goto_position(-70, 1, wait=True)
        time.sleep(6)

        #init
        self.poppy.abs_z.goto_position(0, 1.5, wait=True)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(1)


    @func_attributes(number=40, amount=1, instructions="")
    def coolDown(self):
        #head
        # self.turn_head_left() #my left
        # self.turn_head_right() #my right
        # self.turn_head_down()
        #
        #back
        self.back_strech_static()
        #backhands+shoulder
        self.left_band() #my right
        self.right_band() #my left
        #
        #
        self.left_strech()
        self.right_strech()
        # #self.init_robot()



    # #relax
    # @func_attributes(number=16, amount=1, instructions="bend_elbows_relax")
    # def bend_elbows_relax(self):
    #     time.sleep(5)
    #     self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
    #     self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
    #     time.sleep(8)
    #     self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
    #     self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)
    #
    #
    # #Ex17 Turn head left and right for five second
    # @func_attributes(number=17, amount=1, instructions="turn_head_left")
    # def turn_head_left(self):
    #     #time.sleep(1.5)
    #     #poppy.head_y.goto_position(0, 1, wait=False)
    #     self.poppy.head_z.goto_position(-45, 1, wait=True)
    #     time.sleep(7.4)
    #     self.poppy.head_z.goto_position(0,1,wait=True)
    #     time.sleep(1)
    #
    # @func_attributes(number=18, amount=1, instructions="turn_head_right")
    # def turn_head_right(self):
    #     #time.sleep(1.5)
    #     self.poppy.head_z.goto_position(45, 1, wait=True)
    #     time.sleep(7.4)
    #     self.poppy.head_z.goto_position(0, 1, wait=True)
    #     time.sleep(1)
    #
    # @func_attributes(number=19, amount=1, instructions="turn_head_down")
    # def turn_head_down(self):
    #     #time.sleep(2.5)
    #     self.poppy.head_y.goto_position(20, 1.7, wait=True)
    #     time.sleep(7.8)
    #     self.poppy.head_y.goto_position(-20, 1, wait=True)
    #     time.sleep(1)

    # @func_attributes(number=20,amount=1,instructions="teeth")
    # def teeth(self):
    #     time.sleep(8)
    #
    # @func_attributes(number=21, amount=1, instructions="eyes")
    # def eyes(self):
    #     time.sleep(8)
    #
    # @func_attributes(number=22, amount=1, instructions="eyebrows")
    # def eyebrows(self):
    #     time.sleep(8)
    #
    # @func_attributes(number=23, amount=1, instructions="smile")
    # def smile(self):
    #     time.sleep(8)

    # def strech(self):
    #     self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
    #     self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)
    #     time.sleep(2)
    #     self.poppy.r_shoulder_x.goto_position(80, 1.5, wait=True)
    #     self.poppy.r_elbow_y.goto_position(-15, 1.5, wait=True)
    #     self.poppy.r_shoulder_y.goto_position(-110, 1.5, wait=True)
    #
    # def trying(self): #hands in x?
    #         self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
    #         self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
    #         self.poppy.l_shoulder_x.goto_position(45, 1.5, wait=False)
    #         self.poppy.r_shoulder_x.goto_position(-45, 1.5, wait=True)
    #         time.sleep(2)
    #         self.poppy.l_shoulder_y.goto_position(-20, 1.5, wait=False)
    #         self.poppy.l_shoulder_x.goto_position(-25, 1.5, wait=False)
    #         self.poppy.l_elbow_y.goto_position(-40, 1.5, wait=False)
    #         self.poppy.l_arm_z.goto_position(-90, 1.5, wait=True)
    #         time.sleep(1)
    #         self.poppy.r_shoulder_y.goto_position(-60, 1.5, wait=True)
    #         self.poppy.r_shoulder_x.goto_position(15, 1.5, wait=True)
    #         self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=True)
    #         self.poppy.r_arm_z.goto_position(75, 1.5, wait=True)


if __name__ == '__main__':
    #simulator.createSim()
    #time.sleep(10)
    language = 'Hebrew'
    gender = 'Female'
    s.rep=4
    s.finish_workout=False
    s.isRobot = False
    #s.str_to_say=""
    s.req_exercise = "open arms and move forward"
    s.excel_path = R'C:/Git/poppyCode/greatoded/excel_folder/'
    s.general_path = R'C:/Git/poppyCode/greatoded/'
    s.pic_path = s.general_path + 'Pictures/'
    s.audio_path = s.general_path + 'audioFiles/' + '/' + language + '/' + gender + '/'
    s.robot = Poppy("poppy")
    s.tts = TTS()
    s.robot.start()
    #s.camera = Camera()
    #s.camera.start()
    #s.tts.start()

    #s.screen = Screen()
    time.sleep(10)
    Poppy.to_90_and_down_arms(s.robot)
    #Poppy.coolDown(s.robot)
    #Poppy.warmUp(s.robot)

    #poppy.run_exercise(Poppy.raise_arms_horizontally, "raise arms horizontally")
    # Poppy.raise_arms_horizontally_separate(s.robot)
    # Poppy.raise_arms_horizontally(s.robot)
    # Poppy.bend_elbows(s.robot)
    # Poppy.raise_arms_forward_static(s.robot)
    # Poppy.raise_arms_bend_elbows(s.robot)
    # Poppy.raise_arms_horizontally_turn(s.robot)
    # Poppy.raise_arms_forward(s.robot)
    # Poppy.raise_arms_forward_separate(s.robot)
    # Poppy.raise_arms_90_and_up(s.robot)
    # Poppy.raise_arms_and_lean(s.robot)
    # Poppy.open_arms_and_forward(s.robot)
    # Poppy.raise_hands_and_fold_backward(s.robot)
    # Poppy.open_hands_and_raise_up(s.robot)
    # Poppy.open_and_close_arms_90(s.robot)
    # Poppy.raise_arms_forward_turn(s.robot)
"""

        # self.run_exercise(self.raise_arms_horizontally, "raise arms horizontally")
        # self.run_exercise(self.bend_elbows, "bend elbows")
        # 
        # # self.run_exercise(self.raise_arms_forward_separate, "")
        # 
        # self.run_exercise(self.raise_arms_forward, "raise arms forward")
        # self.run_exercise(self.raise_arms_forward_static, "raise arms forward")
        # # self.run_exercise(self.raise_arms_horizontally_separate, "")
        # self.run_exercise(self.raise_arms_forward_turn_hands, "raise arms forward")
        # self.run_exercise(self.raise_arms_bend_elbows, "raise arms bend elbows")
        # self.run_exercise(self.raise_arms_horizontally_turn_hands, "raise arms horizontally turn hands")
        # self.run_exercise(self.raise_arms_90_and_up, "raise arms forward")
        # # self.run_exercise(self.open_hands_and_raise_up, "raise arms forward")
        # self.run_exercise(self.open_arms_and_move_forward, "raise arms forward")
        # self.run_exercise(self.open_and_close_arms_90, "")
        # 
        # self.run_exercise(self.raise_arms_and_lean, "")
        # self.run_exercise_and_repeat(self.raise_hands_and_fold_backward, "")
"""



