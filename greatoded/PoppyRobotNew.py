import sys
from numpy.core._multiarray_umath import ndarray
from GUI2 import Screen, FullScreenApp
from pypot.creatures import PoppyTorso
import Settings as s
import time
import threading
import random
from GUI2 import StartPage, weightExPage, TryAgainPage, BlankPage, GoodbyePage, ExercisePage, lastquestion, shutdown_win,\
    questionsDuringExplainPage, questionBeginPage, Q1_page, Q2_page, Q3_page,ThankForAnswerBeginPage, questionDuringPage, Q1_New_page,Q2_New_page, ThanksDuringPage, \
    ExamplePage,FinishDemoPage,exerciseExplainPage,  WellDonePage, ExcellentPage, VeryGoodPage, Winnergreat, robotverygood, ExercisePage,\
    nextTime, OneMoreToGO, TwoMoreToGO, ThreeMoreToGO, FourMoreToGO
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


class PoppyRobot(threading.Thread):
    def __init__(self, name):
        print("Poppy class - init function")
        threading.Thread.__init__(self)
        print("THread")
        self.name=name
        self.robotType()
        print("finised robot")

    def robotType(self):
        self.poppy = PoppyTorso(camera='dummy')  # for real robot

    def run(self):
        print("Poppy class - run function")
        for m in self.poppy.motors:  # motors need to be initialized, False=stiff, True=loose
            m.compliant = False #change to false
        self.init_robot()
        print("finished init")
        print("hello wave, introduction - (Poppy class)")
        self.run_exercise(self.hello_waving, "hello"+s.robotNumber) # the robot wave+the name of the hello according to the robot number
        self.all_exercise_run()
        print("done poppy")

    # talk after say hello and before begin the exercises
    def say_before_exercises(self, chosen_exercises):
        print("say_before_exercises")
        s.screen.switch_frame(exerciseExplainPage)
        s.tts.say_wait("exerciseExplain")
        if (s.TBALevel == 3):# TBALevel 3
            self.QuestionBegin()
            self.demo_high(chosen_exercises)
        elif(s.TBALevel == 2):
            s.screen.switch_frame(questionsDuringExplainPage)
            s.tts.say_wait("QuestionsDuringExplainHigh")
            self.demo_high(chosen_exercises)


    def QuestionBegin(self):
        # QA part
        s.screen.switch_frame(questionBeginPage)
        s.tts.say_wait("Answer to Question")
        s.tts.say_no_wait("Q1")
        s.screen.switch_frame(Q1_page)
        while (s.Q1_answer == None):  # wait for participant to answer Q1
            continue
        s.tts.say_no_wait("Q2New")
        s.screen.switch_frame(Q3_page)
        while (s.Q3_answer == None):  # wait for participant to answer Q3
            continue
        s.screen.switch_frame(ThankForAnswerBeginPage)
        s.tts.say_wait("AnswerExplainHigh")
        # QA information data
        if (s.Q1_answer == 'a'):
            if (s.weight == 'withWeights'):
                s.rep = random.randint(6, 8)
            else:
                s.rep = 8
        elif (s.Q1_answer == 'b'):
            if (s.weight == 'withWeights'):
                s.rep = random.randint(8, 10)
            else:
                s.rep = 10
        elif (s.Q1_answer == 'c'):
            if (s.weight == 'withWeights'):
                s.rep = random.randint(10, 12)
            else:
                s.rep = 12
        else:  # d
            if (s.weight == 'withWeights'):
                s.rep = random.randint(12, 14)
            else:
                s.rep = 14
        s.Q_answer.append([s.Q1_answer, s.Q3_answer])
        s.Q_answer.append([s.rep, s.weight])
        Excel.wf_QA()

    def demo_high(self,chosen_exercises):
        print("make an exmaple of each exercise")
        s.screen.switch_frame(ExamplePage)
        s.tts.say_wait('DemoTBAHigh')
        tempRep = s.rep
        s.rep = 1
        count = 1
        for e in chosen_exercises:
            s.tts.say_wait(str(count) + 'EX')
            s.rep = 1
            s.screen.switch_frame(ExamplePage)
            if e.amount == 2:  # for exercise with two separate hands
                self.run_exercise(e, "")
            else:
                exercise_name = getattr(e, "instructions")
                self.run_exercise(e, exercise_name)
            count = count + 1
        s.screen.switch_frame(FinishDemoPage)
        s.tts.say_wait('FinishDemo')
        s.rep = tempRep
        s.demo = False


    def all_exercise_run(self):
        print("Poppy class - all_exercise_run function")
        # s.Two_hands_exercise_names = [self.raise_arms_horizontally, self.bend_elbows,
        #                         self.raise_arms_forward_static,
        #                         self.open_arms_bend_elbows, self.raise_arms_forward,
        #                         self.open_arms_and_forward,
        #                         self.open_hands_and_raise_up, self.open_and_close_arms_90, self.raise_arms_forward_turn]
        s.Two_hands_exercise_names = [self.raise_arms_horizontally, self.bend_elbows,
                                      self.open_arms_bend_elbows, self.raise_arms_forward,
                                      self.open_arms_and_forward,
                                    self.open_and_close_arms_90]
        chosen_exercises = self.fun_chosen_exercises()
        # say and demo for TBA 3
        self.say_before_exercises(chosen_exercises)
        s.req_exercise="hello_waving" #for the camera
        s.waved = False
        s.str_to_say = 'ready wave'
        s.tts.say_no_wait(s.str_to_say)
        s.screen.switch_frame(StartPage)
        while (not s.waved):  # wait for participant to wave or to clicked on the screen
            continue
        time.sleep(1)
        s.screen.switch_frame(BlankPage)
        print("Let's start! - (Poppy class)")
        s.str_to_say = 'lets start'
        s.tts.say_wait(s.str_to_say)

        #### RUN WORKOUT - New
        print("Exercises - (Poppy class)")
        print("ExercisePage")
        #s.screen.switch_frame(ExercisePage)
        countEx=0
        for e in chosen_exercises:
            exercise_name = getattr(e, "instructions")
            if (exercise_name != "hello" and exercise_name != "helloShort"):
                if (s.TBALevel == 1 or s.weight == ''):
                    s.screen.switch_frame(ExercisePage)
                else:
                    s.screen.switch_frame(weightExPage)
            exercise_name = getattr(e, "instructions") #only exercise with both hands
            self.run_exercise(e, exercise_name)
            countEx=countEx+1
            print("exercise number", countEx)
            if countEx==s.exercies_amount:
                print("finished exercises")
                continue
            else:
                if (s.TBALevel==3):
                    self.changeRepTBA3Original()
                elif (s.TBALevel==2):
                    if (countEx<=3):
                        self.changeRepTBA3Original() #the begging is the same only according to the preformance
                    else:
                        if s.Q1_answer != 'c':
                            self.changeRepAfterAnswerTBA2()
                    if countEx == 3: #after finished ex 3
                        self.QuestionDuring()
        self.finish_workout()

    def QuestionDuring(self):
        s.screen.switch_frame(questionDuringPage)
        s.tts.say_wait("QuestionsDuringEx")
        print("QuestionsDuringEx")
        s.screen.switch_frame(Q1_New_page)
        print("Q1_New_page")
        s.tts.say_wait('QuestionsRep')  # Q1_New
        s.tts.say_wait('currentex_'+str(s.rep))
        while (s.Q1_answer == None):  # wait for participant to answer Q1
            continue
        s.screen.switch_frame(Q2_New_page)
        print("Q2_New_page")
        s.tts.say_wait('QuestionsWeight')  # Q2_New
        while (s.Q2_answer == None):  # wait for participant to answer Q2
            continue
        s.screen.switch_frame(ThanksDuringPage)
        s.tts.say_wait("ThanksDuring")
        if s.Q1_answer == 'c':
            s.tts.say_wait("HIghTheSame")
        elif s.Q1_answer == 'a':
            s.rep=s.rep+1
        else:
            s.rep = s.rep - 1
        s.Q_answer.append([s.Q1_answer, s.Q2_answer])
        s.Q_answer.append([s.rep, s.weight])
        Excel.wf_QA()

    def changeRepAfterAnswerTBA2(self):
        if s.Q1_answer == 'a': #add
            if (s.success_exercise or s.current_count>=s.rep):
                s.tts.say_wait("HighSuccessAdd")
                s.rep = s.rep + 2
            elif s.current_count / s.rep >= 0.7:
                s.tts.say_wait("HighalmostSuccessAdd")
                s.rep = s.rep + 1
            else:
                s.tts.say_wait("HighNoSuccessAdd")
        else: #red
            if (s.success_exercise or s.current_count>=s.rep):
                s.tts.say_wait("HighSuccessRed")
                s.rep = s.rep -1
            elif s.current_count / s.rep >= 0.7:
                s.tts.say_wait("HighalmostSuccessRed")
                s.rep = s.rep - 2
            else:
                s.tts.say_wait("HighNoSuccessRed")
                s.rep = s.rep - 2
        print("New rep", s.rep)
        s.rep = min(14, s.rep)
        s.rep = max(6, s.rep)
        print("rep between 6-14", s.rep)

    def changeRepTBA3Original(self):
        if (s.success_exercise or s.current_count>=s.rep):
            s.rep = s.rep + 2
            s.rep = min(14, s.rep)
            print(str(s.rep) + "HighSuccss-.rep+2")
            s.tts.say_wait("HighSuccess")
        elif (s.current_count == s.rep - 1 and s.chance == False):
            s.chance = True  # dont change the rep, give the user one more try
            print(str(s.rep) + "HighSecondChance")
            s.tts.say_wait("HighSecondChance")
        else:
            s.rep = s.rep - int(math.ceil(s.rep - s.current_count) / 2)
            print(str(s.rep) + "round - HighFailure")
            s.tts.say_wait("HighFailure")
        if (s.rep < 6):
            s.rep = 6

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

    def fun_chosen_exercises(self):
        # choose randomly the exercise for this session
        chosen_exercises = []
        while len(chosen_exercises) < s.exercies_amount:
            ex = random.choice(s.Two_hands_exercise_names)
            if ex not in chosen_exercises:
                chosen_exercises.append(ex)
        print(chosen_exercises)
        #s.rep = random.randint(9, 12)
        print("number of repetition" + str(s.rep))
        return chosen_exercises


    #run exercise
    def run_exercise(self, exercise, exercise_name):
        print("_______________")
        print(s.rep)
        s.success_exercise = False
        s.finish_exercise = False
        s.current_count=0
        if (s.rep != 1):
            s.req_exercise = exercise.__name__
        print(s.rep)
        print("Poppy class - run_exercise function " + str(exercise.number) + str(exercise_name))
        if (exercise.number != "hello" and exercise_name!="" and s.rep!=1):
            print("inside")
            s.tts.say_wait(exercise.why)
            s.tts.say_wait(exercise_name)
            print("after purpose")
            if (exercise.count == 'rep'):
                begin = 'beginExRep'
            else:
                begin = 'beginExFor'
            s.tts.say_wait(begin)
            s.tts.say_wait(str(s.rep) + exercise.count)
            s.tts.say_wait(s.weight)
            print("after process")
        else:
            s.tts.say_wait(exercise_name)
        exercise()  # the function of the current exercise.
        s.finish_exercise = True
        print("-----finish_exercise------"+str(s.current_count)+"The number of rep of the user")
        if (exercise.number!='hello'):
            s.req_exercise = ""
            if (s.rep == 1):
                time.sleep(0.5)
            else:
                if (s.success_exercise or s.current_count>=s.rep):
                    s.str_to_say = self.random_encouragement()
                    s.tts.say_wait(s.str_to_say)
                else:
                    if (s.TBALevel == 3 or s.TBALevel==2):
                        print("next")
                        s.screen.switch_frame(nextTime)
                        if (s.Q1_answer == 'c' and s.TBALevel==2):
                            s.tts.say_wait('nextTimeSucc')


    def random_encouragement(self):
        rand = random.random()
        #rand=0.1 #only for testing - delete after
        #time.sleep(1)
        print("encouragement")
        if rand < 0.2:
            s.screen.switch_frame(WellDonePage) #only for testing - remove for note after
            return "well done"
        elif rand < 0.4:
            s.screen.switch_frame(VeryGoodPage)
            return "very Good"
        elif rand<0.6:
            s.screen.switch_frame(ExcellentPage)
            return "excellent"
        elif rand <0.8:
            s.screen.switch_frame(Winnergreat)
            return "winnergreate"
        else:
            s.screen.switch_frame(robotverygood)
            return "robotverygood"

    def finish_workout(self):
        print("Poppy class - finish_workout function")
        # s.numberOfWorkout=s.numberOfWorkout+1
        #time.sleep(6)
        s.screen.switch_frame(GoodbyePage)
        s.str_to_say = 'goodbye'+s.robotNumber
        s.tts.say_wait(s.str_to_say)
        # if (s.sessionNumber == 3):
        #     s.str_to_say = 'goodbye'
        #     s.tts.say_wait(s.str_to_say)
        # else:
        #     s.str_to_say = 'byeShort'
        #     s.tts.say_wait(s.str_to_say)
        Excel.wf_exercise()
        Excel.close_workbook()
        # s.screen.switch_frame(shutdown_win)
        # s.str_to_say='turn off electricity'
        # s.tts.say_wait(s.str_to_say)
        # time.sleep(5)
        # for m in self.poppy.motors:  # need to be initialized for the real robot. False=stiff, True=loose
        #     m.compliant = True
        print("finished robot-")
        s.finish_workout = True
        self.closeRobot()
        s.screen.quit()
        # time.sleep(4)
        # os.system('TASKKILL /IM main.py') #only for simulation
        # os.system('shutdown -s -t 0') #only for the real robot.
    def closeRobot(self):
        print("real robot finished")

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
        self.poppy.r_arm_z.goto_position(-80, 1.5, wait=True)
        for i in range(3):
            self.poppy.r_arm[3].goto_position(-35, 1, wait=True)
            self.poppy.r_arm[3].goto_position(35, 1, wait=True)
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

    @func_attributes(number='1L',amount=1 ,instructions="raise left arm horizontally", why='ForShoulder', count='rep')
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

    @func_attributes(number='1R',amount=1,instructions="raise right arm horizontally", why='ForShoulder', count='rep')
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
    @func_attributes(number=2, amount=1, instructions="raise arms horizontally",why='ForShoulder', count='rep')
    def raise_arms_horizontally(self):
        for i in range(s.rep):
            hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.7, wait=False),
                        self.poppy.l_elbow_y.goto_position(90, 1.7, wait=False),
                        self.poppy.r_shoulder_x.goto_position(-90, 1.7, wait=False),
                        self.poppy.r_elbow_y.goto_position(90, 1.7, wait=True)] #1.5
            time.sleep(1)
            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.7, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.7, wait=False),
                          self.poppy.r_shoulder_x.goto_position(0, 1.7, wait=False),
                          self.poppy.r_elbow_y.goto_position(90, 1.7, wait=True)]
            time.sleep(1)
            if (s.success_exercise):
                break

    # EX3 - Bend Elbows
    @func_attributes(number=3, amount=1, instructions="bend elbows", why='ForBicep', count='rep')
    def bend_elbows(self):
        for i in range(s.rep):
            band = [self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False),self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)]
            time.sleep(0.5)
            down = [self.poppy.r_arm[3].goto_position(85, 1.5, wait=False), self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)]
            time.sleep(0.5)
            if (s.success_exercise):
                break

    # EX4 - Static hands forward
    @func_attributes(number=4, amount=1, instructions="raise arms forward static", why='ForShoulder', count='sec')
    def raise_arms_forward_static(self):
        for i in range(s.rep):
            static=[self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False),
                self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False),
                self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False),
                self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)]
            time.sleep(1)
            if (s.success_exercise):
                break
        #back to position
        initPos=[self.poppy.l_arm_z.goto_position(0, 1.5, wait=False),
                self.poppy.r_arm_z.goto_position(0, 1.5, wait=False),
                self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False),
                self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)]

    # EX5 - Raise Arms Bend Elbows
    @func_attributes(number=5, amount=1, instructions="open arms bend elbows", why='ForShoulder', count='rep')
    def open_arms_bend_elbows(self):
        self.open_hands_aside_move()
        for i in range(s.rep):
            l_hand = [self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.l_arm_z.goto_position(-90, 2, wait=False),
                      self.poppy.l_shoulder_x.goto_position(50, 2, wait=False),
                      self.poppy.l_elbow_y.goto_position(-50, 2, wait=False)]
            r_hand = [self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.r_arm_z.goto_position(90, 2, wait=False),
                      self.poppy.r_shoulder_x.goto_position(-50, 2, wait=False),
                      self.poppy.r_elbow_y.goto_position(-50, 2, wait=True)]
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
    @func_attributes(number=6, amount=1, instructions="raise arms horizontally turn hands", why='ForShoulder', count='sec')
    def raise_arms_horizontally_turn(self):
        self.open_hands_aside_move()
        for i in range(s.rep):
            twisFirst = [self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False),
                              self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)]
            twisSecond=[self.poppy.l_arm_z.goto_position(90, 1.5, wait=False),
                              self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)]
            if(s.success_exercise):
                break

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


    # EX7 - Raise arms forward
    @func_attributes(number=7, amount=1, instructions="raise arms forward", why='ForShoulder', count='rep')
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
                self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)]
            time.sleep(1)
            if (s.success_exercise):
                break

    # EX8 - Raise arms forward speratally
    @func_attributes(number=8, amount=2, instructions="raise arms forward separate")
    def raise_arms_forward_separate(self):
        self.run_exercise(self.raise_right_arm_forward, "raise right and forward")
        self.run_exercise(self.raise_left_arm_forward, "raise left and forward")


    @func_attributes(number='8L', amount=1,instructions="raise left and forward", why='ForShoulder', count='rep')
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

    @func_attributes(number='8R',amount=1, instructions="raise right and forward", why='ForShoulder', count='rep')
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
    @func_attributes(number=9, amount=1, instructions="raise arms 90 and up", why='ForShoulder', count='rep')
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

    # EX10 raise arms and lean and repeat
    @func_attributes(number=10, amount=2, instructions="raise arms and lean")
    def raise_arms_and_lean_dynmic(self):
        # mirror
        self.run_exercise(self.raise_right_arm_and_lean_dynmic, "raise right arm and lean dynmic")
        self.run_exercise(self.raise_left_arm_and_lean_dynmic, "raise left arm and lean dynmic")

    @func_attributes(number='10L',amount=1, instructions="raise left arm and lean dynmic", why='ForSide', count='rep')
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


    @func_attributes(number='10R',amount=1, instructions="raise right arm and lean dynmic", why='ForSide', count='rep')
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
    @func_attributes(number=11, amount=1, instructions="open arms and move forward", why='ForShoulder', count='rep')
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
    @func_attributes(number=12, amount=1, instructions="raise hands and fold backward", why='ForTricep', count='rep')
    def raise_hands_and_fold_backward(self):
        #hainds up
        self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-179, 1.5, wait=True)
        for i in range(s.rep):
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
            time.sleep(1)
            self.poppy.l_elbow_y.goto_position(-30, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(-30, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break
        #init
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)

    # EX13 open hands and raise up
    @func_attributes(number=13, amount=1, instructions="open hands and raise up", why='ForShoulder', count='rep')
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
            self.poppy.l_shoulder_x.goto_position(15, 1, wait=False)
            self.poppy.r_shoulder_x.goto_position(-15, 1, wait=False)
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
    @func_attributes(number=14, amount=1, instructions="open and close arms 90", why='ForShoulder', count='rep')
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


    @func_attributes(number=15, amount=1, instructions="open and down arms 90", why='ForShoulder', count='rep')
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

    @func_attributes(number=16, amount=1, instructions="to 90 and down arms", why='ForShoulder', count='rep')
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
    @func_attributes(number=17, amount=1, instructions="raise arms forward turn hands", why='ForShoulder',count='sec')
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
            if (s.success_exercise):
                break
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 2, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 2, wait=True)


    @func_attributes(number=18, amount=2, instructions="raise hands and fold backward separate")
    def raise_hands_and_fold_backward_separate(self):
        self.run_exercise(self.raise_right_and_fold_backward, "raise right and fold backward")
        self.run_exercise(self.raise_left_and_fold_backward, "raise left and fold backward")


    @func_attributes(number='18R', amount=1, instructions="raise right and fold backward", why='ForTricep', count='rep')
    def raise_right_and_fold_backward(self):
        # left robot
        self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=True)

        for i in range(s.rep):
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
            time.sleep(1)
            self.poppy.l_elbow_y.goto_position(-20, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break
        # init
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)


    @func_attributes(number='18L', amount=1, instructions="raise left and fold backward", why='ForTricep', count='rep')
    def raise_left_and_fold_backward(self):
        self.poppy.r_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=True)
        for i in range(s.rep):
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
            time.sleep(1)
            self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=True)
            time.sleep(1)
            if (s.success_exercise):
                break

        # init
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)

        # EX19 - Bend Elbows separate
    @func_attributes(number=19, amount=2, instructions="bend elbows separate")
    def bend_elbows_separate(self):
        self.run_exercise(self.bend_right_elbow, "bend right elbow")
        self.run_exercise(self.bend_left_elbow, "bend left elbow")

    @func_attributes(number='19R', amount=1, instructions="bend right elbow", why='ForBicep', count='rep')
    def bend_right_elbow(self):
        for i in range(s.rep):
            self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
            time.sleep(1)
            self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)
            time.sleep(0.5)
            if (s.success_exercise):
                break

    @func_attributes(number='19L', amount=1, instructions="bend left elbow", why='ForBicep', count='rep')
    def bend_left_elbow(self):
        for i in range(s.rep):
            self.poppy.r_arm[3].goto_position(-60, 1.5, wait=True)
            time.sleep(1)
            self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
            time.sleep(0.5)
            if (s.success_exercise):
                break

    # EX20 - Bend Elbows separate
    @func_attributes(number=20, amount=2, instructions="raise arms 90 and up separate")
    def raise_arms_90_and_up_separate(self):
        self.run_exercise(self.raise_right_90_and_up, "raise right 90 and up")
        self.run_exercise(self.raise_left_90_and_up, "raise left 90 and up")


    @func_attributes(number='20R', amount=1, instructions="raise right 90 and up", why='ForShoulder', count='rep')
    def raise_right_90_and_up(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=True)
        for i in range(s.rep):
            nine = [self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)]
            time.sleep(1)
            up = [self.poppy.l_shoulder_x.goto_position(150, 1.5, wait=False),
              self.poppy.l_elbow_y.goto_position(60, 1.5, wait=True)]
            time.sleep(1)
            if (s.success_exercise):
                break
        # init
        time.sleep(1)
        self.poppy.l_arm_z.goto_position(0, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    @func_attributes(number='20L', amount=1, instructions="raise left 90 and up", why='ForShoulder', count='rep')
    def raise_left_90_and_up(self):
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        for i in range(s.rep):
            nine = [self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                self.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)]
            time.sleep(1)
            up = [self.poppy.r_shoulder_x.goto_position(-150, 1.5, wait=False),
              self.poppy.r_elbow_y.goto_position(60, 1.5, wait=True)]
            time.sleep(1)
            if (s.success_exercise):
                break
        # init
        time.sleep(1)
        self.poppy.r_arm_z.goto_position(0, 1., wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)


    # warmUp exercise
    @func_attributes(number=31, amount=2, instructions="")
    def head_circle(self):
        # mirror
        self.run_exercise(self.head_clockWise, "")
        self.run_exercise(self.head_anticlockwise, "")

    @func_attributes(number='31L', amount=1, instructions="")
    def head_anticlockwise(self):
        headZ_degree = [-100, -50, 0, 50, 100]
        for num in range(2):
            # down
            self.poppy.head_y.goto_position(8, 1, wait=False)
            for i in range(len(headZ_degree)):
                self.poppy.head_z.goto_position(headZ_degree[i], 1.3, wait=True)
            # up
            self.poppy.head_y.goto_position(-40, 1, wait=False)
            for i in range(len(headZ_degree)):
                self.poppy.head_z.goto_position(headZ_degree[len(headZ_degree) - 1 - i], 1.3, wait=True)

        # init
        self.poppy.head_y.goto_position(-20, 1, wait=False)
        self.poppy.head_z.goto_position(0, 1, wait=True)

    @func_attributes(number='31R', amount=1, instructions="")
    def head_clockWise(self):
        headZ_degree = [-100, -50, 0, 50, 100]
        for num in range(2):
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
            # next move
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
        # open hand and 90
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(1)
        for i in range(5):
            self.poppy.abs_z.goto_position(70, 2, wait=True)
            self.poppy.abs_z.goto_position(-70, 2, wait=True)

        # init
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
            self.poppy.l_shoulder_x.goto_position(-20, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(20, 1.5, wait=False)
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
        for i in range(5):
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

    # wormUp
    @func_attributes(number=30, amount=1, instructions="")
    def warmUp(self):
        self.head_circle()
        # self.elbow_clockWise() #not dood enough
        self.open_and_close_arms_90_dynamic()
        self.open_and_down_arms_90_dynamic()
        self.back_strech_Dynmic()
        self.raise_arms_and_lean_repeat()

    # Ex17 Turn head left and right for five second
    @func_attributes(number=41, amount=1, instructions="turn_head_left")
    def turn_head_left(self):
        # time.sleep(1.5)
        self.poppy.head_y.goto_position(0, 1, wait=False)
        self.poppy.head_z.goto_position(-45, 1, wait=True)
        time.sleep(7.4)
        self.poppy.head_z.goto_position(0, 1, wait=True)
        time.sleep(1)

    @func_attributes(number=42, amount=1, instructions="turn_head_right")
    def turn_head_right(self):
        # time.sleep(1.5)
        self.poppy.head_y.goto_position(0, 1, wait=False)
        self.poppy.head_z.goto_position(45, 1, wait=True)
        time.sleep(6)
        self.poppy.head_z.goto_position(0, 1, wait=True)
        time.sleep(1)

    @func_attributes(number=43, amount=1, instructions="turn_head_down")
    def turn_head_down(self):
        # time.sleep(2.5)
        self.poppy.head_y.goto_position(20, 1.7, wait=True)
        time.sleep(6)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        time.sleep(2)

    def hands_up(self):
        self.poppy.l_shoulder_y.goto_position(-200, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-200, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(-10, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(10, 1.5, wait=False)
        self.poppy.head_y.goto_position(50, 1.5, wait=True)
        time.sleep(1)

    @func_attributes(number=44, amount=1, instructions="")
    def left_band(self):
        self.hands_up()
        self.poppy.l_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-40, 1.5, wait=True)
        self.poppy.r_arm_z.goto_position(80, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(7)

        # init
        # init hands up
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        # init exe
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
        # init hand up
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        # init exercise
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        self.init_robot()
        time.sleep(2)

    @func_attributes(number=46, amount=1, instructions="")
    def left_strech(self):
        # open to 90
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(1)

        self.poppy.abs_z.goto_position(-15, 1.5, wait=False)
        self.poppy.head_z.goto_position(50, 1.5, wait=False)
        # left
        self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(-120, 1.5, wait=True)
        # right
        self.poppy.r_shoulder_y.goto_position(-50, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(30, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(20, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(30, 1.5, wait=True)
        time.sleep(7)

        # init
        self.poppy.abs_z.goto_position(0, 1.5, wait=False)
        self.poppy.head_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        self.init_robot()
        time.sleep(1)

    @func_attributes(number=47, amount=1, instructions="")
    def right_strech(self):
        self.open_hands_aside_move()
        # right strech
        self.poppy.abs_z.goto_position(30, 1, wait=False)
        self.poppy.head_z.goto_position(-50, 1, wait=False)
        # right
        self.poppy.r_shoulder_y.goto_position(-90, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(120, 1, wait=True)
        # left
        self.poppy.l_shoulder_y.goto_position(-50, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-30, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(-20, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(30, 1.5, wait=True)
        time.sleep(7)

        # init
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
        # open hand and 90
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(2)

        self.poppy.abs_z.goto_position(70, 1, wait=True)
        time.sleep(6)
        self.poppy.abs_z.goto_position(0, 1, wait=True)
        time.sleep(1)
        self.poppy.abs_z.goto_position(-70, 1, wait=True)
        time.sleep(6)

        # init
        self.poppy.abs_z.goto_position(0, 1.5, wait=True)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(1)

    @func_attributes(number=40, amount=1, instructions="")
    def coolDown(self):
        # head
        # self.turn_head_left() #my left
        # self.turn_head_right() #my right
        # self.turn_head_down()
        #
        # back
        self.back_strech_static()
        # backhands+shoulder
        self.left_band()  # my right
        self.right_band()  # my left
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
    language = 'Hebrew'
    gender = 'Female'
    s.rep=4
    s.success_exercise=False
    s.sessionNumber=3
    s.subjectNum=12
    s.TBALevel=1
    s.finish_workout=False
    s.isRobot = False
    s.str_to_say=""
    s.req_exercise = ""
    s.excel_path = R'C:/Git/poppyCode/greatoded/excel_folder/'
    s.general_path = R'C:/Git/poppyCode/greatoded/'
    s.pic_path = s.general_path + 'Pictures/'
    s.audio_path = s.general_path + 'audioFiles/' + '/' + language + '/' + gender + '/'
    s.robot = PoppyRobot("poppy")
    s.tts = TTS()
    #s.camera = Camera()
    #s.camera.start()
    #s.tts.start()
    s.robot.start()
    #s.screen = Screen()
    PoppyRobot.raise_hands_and_fold_backward(s.robot)

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