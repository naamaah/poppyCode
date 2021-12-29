import sys

from numpy.core._multiarray_umath import ndarray
#from pypot.creatures import PoppyHumanoid
from pypot.creatures import PoppyTorso
import Settings as s
import time
import threading
import random
from GUI2 import StartPage, weightPage, TryAgainPage, BlankPage, GoodbyePage, ExercisePage, lastquestion, shutdown_win, begin_page, \
    StartPage_Relax, Relax_Page_ber, lastquestion_relax, relax_thl, relax_thr, relax_thd, facemovement_Relax, teeth, \
    eyes, eyebrows, smile
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

class Poppy(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name=name
        #self.poppy = PoppyTorso()  # for real robot
        #self.poppy = PoppyHumanoid(simulator='vrep')  # for simulator
        self.poppy = PoppyTorso(simulator='vrep')  # for simulator
        print("init robot - (Poppy class)")
        for m in self.poppy.motors:  # motors need to be initialized, False=stiff, True=loose
            m.compliant = False #change to false
        self.init_robot()

    def run_rep(self):
        s.relax = None
        time.sleep(0.5)
        s.str_to_say = 'Start_page'
        #s.screen.switch_frame(begin_page)
        mylist = ["Another" "workout"]
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
        while (s.relax == None):
            continue
        if (s.relax == False):
            self.exercise_run()
        else:
            self.relaxrun()

    def run(self):
        print("hello wave, introduction - (Poppy class)")
        self.run_exercise(self.hello_waving, "hello")
        time.sleep(3)
        s.screen.switch_frame(begin_page)
        s.str_to_say = 'Start_page'
        while (s.relax==None):
            continue
        if(s.relax==False):
            self.exercise_run()
        else:
            self.relaxrun()

    def relaxrun(self):
        s.screen.switch_frame(StartPage_Relax)
        s.str_to_say = 'intro_relax'
        while (not s.clickrelax):  # wait for participant to wave
            continue
        time.sleep(1)
        s.screen.switch_frame(BlankPage)
        print("Let's start! - (Poppy class)")
        chosenrelax=[self.bend_elbows_relax,self.turn_head_down,self.turn_head_right,self.turn_head_left]
        for e in chosenrelax:
            self.run_exercise_and_repeat(e,getattr(e, "instructions"))
            print (e)
        self.face_movement()
        print ("finised with face")
        s.relax = None
        time.sleep(8)
        s.str_to_say = "repeat workout"
        print("stay on finished")
        s.screen.switch_frame(lastquestion_relax)
        while (s.relax == None):
            continue
        if(s.relax==True):
            self.exercise_run()
        elif(s.relax==False):
            self.finish_workout()

    def face_movement(self):
        s.screen.switch_frame(facemovement_Relax)
        s.str_to_say='moving_from_face'
        while (not s.facemove):  # wait for participant to wave
            continue
        s.screen.switch_frame(BlankPage)
        chosenrelax = [self.teeth,self.eyes,self.eyebrows,self.smile]
        for e in chosenrelax:
            self.run_exercise_and_repeat(e, getattr(e, "instructions"))

    def exercise_run(self):
        s.pickWeights = False
        s.waved = False
        s.str_to_say ="adding weights"
        s.screen.switch_frame(weightPage)
        while not s.pickWeights:
            continue
        s.str_to_say = 'ready wave'
        s.screen.switch_frame(StartPage)
        s.relax=False
        while (not s.waved): # wait for participant to wave or to clicked on the screen
           continue
        time.sleep(1)
        s.screen.switch_frame(BlankPage)
        print("Let's start! - (Poppy class)")
        s.str_to_say='lets start'
        time.sleep(2)
        self.countexc=np.zeros([s.exercies_amount+1,1])
        #all existing exercises
        exercise_names = [self.raise_arms_forward,
                          self.raise_arms_horizontally, self.bend_elbows,
                          self.raise_arms_forward_turn, self.raise_arms_bend_elbows, self.raise_arms_horizontally_turn,
                          self.open_and_close_arms_90, self.raise_arms_horizontally_separate , self.raise_arms_forward_separate] #, self.open_hands_and_raise_up, self.raise_hands_and_fold_backward, self.raise_arms_and_lean, ]

        #choose randomly the exercise for this practice
        chosen_exercises = []

        while len(chosen_exercises) <= s.exercies_amount:
            ex = random.choice(exercise_names)
            if ex not in chosen_exercises:
                chosen_exercises.append(ex)
        print (chosen_exercises)

        #### RUN WORKOUT
        count = 0
        cog_mis_aft_exc = random.randint(2,5)
        print("Exercises - (Poppy class)")
        for e in chosen_exercises:
            count = count + 1
            now=datetime.now()
            if e.amount == 2:
             if(getattr(e, "instructions")!= "raise arms horizontally separate" or getattr(e, "instructions")!="raise arms forward separate"):
                dt_t = str(date.today())
                td_t=str(now.strftime("%H:%M:%S"))
                ct = str(0)
                mylist = [dt_t,td_t,e, ct]
                with open(s.general_path+"data_shik.csv", "ab") as f:
                    f.write(b"\t")
                    savetxt(f, mylist, fmt='%s')
             self.run_exercise(e, "")

            else:
                if (e != self.raise_arms_forward_separate or e != self.raise_arms_horizontally_separate):
                    dt_t = str(date.today())
                    ct = str(0)
                    td_t = str(now.strftime("%H:%M:%S"))
                    mylist = [dt_t,td_t, e, ct]

                    with open(s.general_path+"data_shik.csv", "ab") as f:
                        f.write(b"\t")
                        savetxt(f, mylist, fmt='%s')
                print (getattr(e, "instructions") +" - (Poppy class)")
                self.run_exercise_and_repeat(e, getattr(e, "instructions"))
            if (count == cog_mis_aft_exc):
                dt_t = str(date.today())
                td_t = str(now.strftime("%H:%M:%S"))
                mylist=[dt_t,td_t,'cognitive mission']
                with open(s.general_path+"data_shik.csv", "ab") as f:
                    f.write(b"\t")
                    savetxt(f, mylist, fmt='%s')
                s.str_to_say="come to the screen"
                time.sleep(2)
                s.cogGame = True
                #s.cogGameCount = 0
                chose_cog = random.randint(1, 5)
                #chose_cog = 3
                print(chose_cog)
                if chose_cog==1:
                    s.screen.switch_frame(GameOneStart)
                elif chose_cog==2:
                    s.screen.switch_frame(GameTwoStart)
                elif chose_cog == 3:
                    s.screen.switch_frame(GameFourStart)
                elif chose_cog == 4:
                    s.screen.switch_frame(GameFiveStart)
                else:
                    s.screen.switch_frame(introduction)
                while (s.cogGame):
                    continue
                print("POPPY: after cog finished")
                time.sleep(4)
        self.repeatorfinish()

    def repeatorfinish(self):
        s.str_to_say="repeat workout"
        if (s.repeat_again==None):
            s.screen.switch_frame(lastquestion)
        else:
            self.finish_workout()
        print('reached here  - (Poppy class)')
        print(s.repeat_again)
        starttime=time.time()
        a=0
        while s.repeat_again is None:
            continue
        if(s.repeat_again==True):
            print('start  - (Poppy class)')
            s.repeat_again=False
            Excel.wf_exercise("")
            Excel.close_workbook()
            Excel.create_workbook()
            self.run_rep()
        else:
            self.finish_workout()
            s.repeat_again = False

    def init_robot(self):
        for m in self.poppy.motors:
            if not m.name == 'r_elbow_y' and not m.name == 'l_elbow_y' and not m.name == 'head_y':
                m.goto_position(0, 1, wait=True)
        self.poppy.head_y.goto_position(-20,1,wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    # run exercise
    def run_exercise(self, exercise, exercise_name):
        mylist = []
        s.success_exercise = False
        if(exercise_name=="raise arms horizontally" or exercise_name=="raise left arm horizontally"):
            print("instruction for exercise  - (Poppy class)")
            s.str_to_say = exercise_name
            time.sleep(4.5)
            s.req_exercise = exercise.__name__
        elif(exercise_name=="open and close arms 90"):
            print("instruction for exercise - (Poppy class)")
            s.str_to_say = exercise_name
            time.sleep(5)
            s.req_exercise = exercise.__name__
        elif(exercise_name=="raise right arm horizontally"):
            print("instruction for exercise  - (Poppy class)")
            s.str_to_say = exercise_name
            time.sleep(4.5)
            s.req_exercise = exercise.__name__
        elif(exercise_name=="raise arms bend elbows"):
            s.req_exercise = exercise.__name__
            time.sleep(1)
            print("instruction for exercise  - (Poppy class)")
            s.str_to_say = exercise_name
            time.sleep(4)
        elif(exercise_name=="raise arms forward separate" or exercise_name=="raise arms horizontally separate"):
            print("instruction for exercise - (Poppy class)")
            s.str_to_say = exercise_name
            time.sleep(3)
        elif(exercise_name=="raise arms forward"or exercise_name=="raise right arm forward"):
            print("instruction for exercise - (Poppy class)")
            s.str_to_say = exercise_name
            time.sleep(4.5)
            s.req_exercise = exercise.__name__
            #time.sleep(2)
            print (s.req_exercise)
        elif(exercise_name=="bend_elbows_relax"):
            print("instruction for exercise - (Poppy class)")
            print(exercise_name)
            s.str_to_say = exercise_name
            time.sleep(2)
            s.req_exercise = exercise.__name__
            print (s.req_exercise)
        else:
            print("instruction for exercise - (Poppy class)")
            print(exercise_name +" - (Poppy class)")
            s.str_to_say = exercise_name
            time.sleep(4)
            s.req_exercise = exercise.__name__
            print (s.req_exercise+" - (Poppy class)")
        if(exercise_name=="raise arms bend elbows" or exercise_name=="raise arms horizontally"):
            time.sleep(1)
        else:
            time.sleep(2)
        exercise()
        if (exercise_name!="hello"):
            s.req_exercise = ""
            time.sleep(3)

    def repeat_exercise(self):
        print("You need to do the exercise 8 times. if you want to try again please raise your right hand  - (Poppy class)")
        # s.tts.say='feedback 8 times'
        s.str_to_say='try again'
        s.waved = False
        self.time1 = time.time()
        self.time2 = 0
        s.req_exercise = "hello_waving"
        time.sleep(1)
        s.screen.switch_frame(TryAgainPage)
        time.sleep(5)
        while not s.waved and (self.time2 - self.time1 < 30) and not s.clickedTryAgain:
            self.time2 = time.time()
            continue
        s.req_exercise = ""
        s.clickedTryAgain = False
        time.sleep(1)
        if s.waved:
            s.screen.switch_frame(ExercisePage)
            return True
        else:
            return False

    def run_exercise_and_repeat(self, exercise, exercise_name):
        time.sleep(1)
        now=datetime.now()
        if (exercise_name == "raise right arm horizontally" or exercise_name == "raise left arm horizontally" or exercise_name=='raise right arm forward'or exercise_name=="raise left arm forward"):
            dt_t = str(date.today())
            ct = str(0)
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t,td_t ,exercise_name, ct]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
        if(exercise_name=="bend_elbows_relax"):
            s.screen.switch_frame(Relax_Page_ber)
            self.run_exercise(exercise, exercise_name)
        elif(exercise_name=="turn_head_left"):
            s.screen.switch_frame(relax_thl)
            self.run_exercise(exercise, exercise_name)
        elif(exercise_name=="turn_head_right"):
            s.screen.switch_frame(relax_thr)
            self.run_exercise(exercise, exercise_name)
        elif(exercise_name=="turn_head_down"):
            s.screen.switch_frame(relax_thd)
            self.run_exercise(exercise, exercise_name)
        elif(exercise_name=="teeth"):
            s.screen.switch_frame(teeth)
            self.run_exercise(exercise, exercise_name)
        elif (exercise_name == "eyes"):
            s.screen.switch_frame(eyes)
            self.run_exercise(exercise, exercise_name)
        elif (exercise_name == "eyebrows"):
            s.screen.switch_frame(eyebrows)
            self.run_exercise(exercise, exercise_name)
        elif (exercise_name == "smile"):
            s.screen.switch_frame(smile)
            self.run_exercise(exercise, exercise_name)
        else:
            print("ExercisePage")
            s.screen.switch_frame(ExercisePage)
            self.run_exercise(exercise, exercise_name)

    #TODO def finish_exercise(self)

    def finish_workout(self):
        s.numberOfWorkout=s.numberOfWorkout+1
        time.sleep(1)
        s.screen.switch_frame(GoodbyePage)
        s.str_to_say = 'goodbye'
        time.sleep(5)
        Excel.wf_exercise("success"+str(s.numberOfWorkout))
        Excel.close_workbook()
        mylist=["good","bye"]
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\t")
            savetxt(f, mylist, fmt='%s')
        s.screen.switch_frame(shutdown_win)
        s.str_to_say='turn off electricity'
        time.sleep(5)
        for m in self.poppy.motors:  # need to be initialized for the real robot. False=stiff, True=loose
            m.compliant = True
        print("finished robot - ")
        s.finish_workout = True
        simulator.closeSim()

        s.screen.quit()
        #os.system('TASKKILL /F /IM coppeliaSim.exe')
        #os.system('shutdown -s -t 0') #delete for sumulation

    # define attributes for a function
    def func_attributes(**attrs):
        def attributes(f):
            for k, v in attrs.items():
                setattr(f, k, v)
            return f
        return attributes

    #-----------------------Exercises---------------------------#
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
        self.run_exercise_and_repeat(self.raise_right_arm_horiz, "raise right arm horizontally")
        self.run_exercise_and_repeat(self.raise_left_arm_horiz, "raise left arm horizontally")

    @func_attributes(instructions="raise left arm horizontally")
    def raise_left_arm_horiz(self):
        for i in range(s.rep):
            right_hand_up = [self.poppy.r_shoulder_x.goto_position(-90, 1.7, wait=False),
                             self.poppy.r_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            right_hand_down = [self.poppy.r_shoulder_x.goto_position(0, 1.7, wait=False),
                               self.poppy.r_elbow_y.goto_position(90, 1.7, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break

    @func_attributes(instructions="raise right arm horizontally")
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
                        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(2)
            hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                          self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                          self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
            time.sleep(2)
            if (s.success_exercise):
                break

    # EX3 - Bend Elbows
    @func_attributes(number=3, amount=1, instructions="bend elbows")
    def bend_elbows(self):
        for i in range(s.rep):
            self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
            self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
            time.sleep(0.5)
            self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
            self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)
            time.sleep(0.5)
            if (s.success_exercise):
                break

    @func_attributes(number=16,amount=1,instructions="bend_elbows_relax")
    def bend_elbows_relax(self):
        time.sleep(5)
        self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
        time.sleep(8)
        self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)

    # EX4 - Static hands forward
    @func_attributes(number=4, amount=1, instructions="raise arms forward static")
    def raise_arms_forward_static(self):
        self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
        time.sleep(12)
        time.sleep(0.5)
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)

    # EX5 - Raise Arms Bend Elbows
    @func_attributes(number=5, amount=1, instructions="raise arms bend elbows")
    def raise_arms_bend_elbows(self):
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
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # EX6 - Raise Arms Horizontally Turn_Hands
    @func_attributes(number=6, amount=1, instructions="raise arms horizontally turn hands")
    def raise_arms_horizontally_turn(self):
        self.open_hands_aside_move()
        for i in range(4):
            twisting_aside = [self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False),
                              self.poppy.r_arm_z.goto_position(90, 1.5, wait=True),
                              self.poppy.l_arm_z.goto_position(90, 1.5, wait=False),
                              self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)]
        time.sleep(1)
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    def open_hands_aside_move(self):
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)

    # EX7 - Raise arms forward
    @func_attributes(number=7, amount=1, instructions="raise arms forward")
    def raise_arms_forward(self):
        for i in range(s.rep):
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            time.sleep(1.8)
            if (s.success_exercise):
                break

    # EX8 - Raise arms forward speratally
    @func_attributes(number=8, amount=2, instructions="raise arms forward separate")
    def raise_arms_forward_separate(self):
        self.run_exercise_and_repeat(self.raise_right_arm_forward, "raise right arm forward")
        self.run_exercise_and_repeat(self.raise_left_arm_forward, "raise left arm forward")

    def raise_left_arm_forward(self):
        for i in range(s.rep):
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            time.sleep(1.6)
            if (s.success_exercise):
                break

    def raise_right_arm_forward(self):
        for i in range(s.rep):
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=True)
            time.sleep(1.6)
            if (s.success_exercise):
                break

    # EX9 - Raise arms 90 and up
    @func_attributes(number=9, amount=1, instructions="raise arms 90 and up")
    def raise_arms_90_and_up(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
        for i in range(s.rep):
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
            time.sleep(2)
            self.poppy.r_shoulder_x.goto_position(-150, 1, wait=False)
            self.poppy.l_shoulder_x.goto_position(150, 1, wait=False)
            self.poppy.r_elbow_y.goto_position(60, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(60, 1.5, wait=False)
            time.sleep(2)
            if (s.success_exercise):
                break

    # EX10 raise arms and lean
    @func_attributes(number=10, amount=2, instructions="raise arms and lean")
    def raise_arms_and_lean(self):
        self.run_exercise_and_repeat(self.raise_right_arm_and_lean,"")
        self.run_exercise_and_repeat(self.raise_left_arm_and_lean, "")

    @func_attributes(instructions="raise right arm and lean")
    def raise_right_arm_and_lean(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(150, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(30, 1.5, wait=False)
        self.poppy.bust_x.goto_position(20, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=True)
        self.poppy.r_shoulder_x.goto_position(-30, 1.5, wait=False)
        time.sleep(s.rep)
        self.poppy.bust_x.goto_position(0, 1.5, wait=True)
        self.poppy.bust_y.goto_position(0, 1, wait=True)

    @func_attributes(instructions="raise left arm and lean")
    def raise_left_arm_and_lean(self):
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(-150, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(30, 1.5, wait=False)
        self.poppy.bust_x.goto_position(-20, 1.5, wait=False)
        self.poppy.bust_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(30, 1.5, wait=False)
        time.sleep(s.rep)
        self.poppy.bust_x.goto_position(0, 1.5, wait=True)
        self.poppy.bust_y.goto_position(0, 1, wait=True)

    # EX11 Raise hands, open horizontally and move forward
    @func_attributes(number=11, amount=1, instructions="open arms and move forward")
    def open_arms_and_forward(self):
        for i in range(s.rep):
            self.open_hands_aside_move()
            time.sleep(0.5)
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)
            time.sleep(2)
            if (s.success_exercise):
                break
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # EX12 Raise hands and fold backward
    @func_attributes(number=12, amount=1, instructions="raise hands and fold backward")
    def raise_hands_and_fold_backward(self):
        self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-180, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)
        for i in range(s.rep):
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
            time.sleep(1.5)
            self.poppy.l_elbow_y.goto_position(-20, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
            time.sleep(1.5)
            if (s.success_exercise):
                break

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
            time.sleep(1.5)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.l_shoulder_x.goto_position(10, 1, wait=False)
            self.poppy.r_shoulder_x.goto_position(-10, 1, wait=False)
            self.poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-180, 1.5, wait=True)
            time.sleep(1.5)
            if (s.success_exercise):
                break

    # EX14 open and close arms 90
    @func_attributes(number=14, amount=1, instructions="open and close arms 90")
    def open_and_close_arms_90(self):
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
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
            time.sleep(1.7)
            if (s.success_exercise):
                break
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # EX15 raise_arms_forward_turn_hands
    @func_attributes(number=15, amount=1, instructions="raise arms forward turn hands")
    def raise_arms_forward_turn(self):
        self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False)
        self.poppy.r_shoulder_y.goto_position(-90, 2, wait=True)
        self.poppy.l_arm_z.goto_position(-90, 2, wait=False)
        self.poppy.r_arm_z.goto_position(90, 2, wait=False)
        for i in range(4):
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=True)
            #time.sleep(0.5)
            self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        time.sleep(0.3)
        #init
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 2, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 2, wait=True)

    #Ex17 Turn head left and right for five second
    @func_attributes(number=17, amount=1, instructions="turn_head_left")
    def turn_head_left(self):
        time.sleep(1.5)
        self.poppy.head_z.goto_position(-45, 1, wait=True)
        time.sleep(7.4)
        self.poppy.head_z.goto_position(0,1,wait=True)
        time.sleep(2)

    @func_attributes(number=18, amount=1, instructions="turn_head_right")
    def turn_head_right(self):
        time.sleep(1.5)
        self.poppy.head_z.goto_position(45, 1, wait=True)
        time.sleep(7.4)
        self.poppy.head_z.goto_position(0, 1, wait=True)
        time.sleep(2)

    @func_attributes(number=19, amount=1, instructions="turn_head_down")
    def turn_head_down(self):
        time.sleep(2.5)
        self.poppy.head_y.goto_position(20, 1.7, wait=True)
        time.sleep(7.8)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        time.sleep(2)
    @func_attributes(number=20,amount=1,instructions="teeth")
    def teeth(self):
        time.sleep(8)

    @func_attributes(number=21, amount=1, instructions="eyes")
    def eyes(self):
        time.sleep(8)

    @func_attributes(number=22, amount=1, instructions="eyebrows")
    def eyebrows(self):
        time.sleep(8)

    @func_attributes(number=23, amount=1, instructions="smile")
    def smile(self):
        time.sleep(8)

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






