import Settings as s
from tts import TTS
import socket
import select
import threading
from Realsense import Realsense
from Joint import joint
import time
import math
import random
from GUI2 import WellDonePage, ExcellentPage, VeryGoodPage, Winnergreat, robotverygood, feedback_elbow, feedback_head, \
    feedback_relax
import Excel

class Camera(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # Create socket for client-server communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 8888)
        self.sock.bind(self.server_address)
        print ("camera init (Camera class)")

    # Start camera application
    def playRealsense(self):
        rStart = Realsense()
        rStart.start()
        print("Realsense start (Camera class)")

    # Stop camera application
    def stopRealsense(self):
        rStop = Realsense()
        rStop.stop()
        print("Realsense stop (Camera class)")
        # clear received data
        while self.getSkeletonData() is not None:
            continue

    # Client - read messages
    def getSkeletonData(self):
        self.sock.settimeout(5.0) #for check naama change to 10 instad 5
        try:
            #data, address = self.sock.recvfrom(4096)
            data= str(self.sock.recvfrom(4096))
            self.sock.settimeout(None) #to check
            data = data.split('/')
            jointsStr = []
            for i in data:
                joint = i.split(',')
                jointsStr.append(joint)
            # now change to float values
            joints = [] #joints data
            for j in jointsStr:
                joints.append(self.createJoint(j))
            return joints
        except socket.timeout:  # fail after 1 second of no activity
            print("Didn't receive data! [Timeout] - (Camera class)")
            # TODO Maybe add a meesage to the user that the camera don't recieve data?
            return None

    # input - joint data list ; output - joint object
    def createJoint(self, jointList):
        try:
            new_joint = joint (jointList[0], float(jointList[1]) , float(jointList[2]), float(jointList[3]))
            return new_joint
        except:
            print("could not create new joint: list index out of range - (Camera class)")
            return None

    # input - all joints data, required joint number ; output - data of the required joint only
    def findJointData(self, jointsList, jointNumber):
        flag = False #did the joint number exist
        jointData = []
        if jointsList!=None:
            for i in jointsList:
                if  i!=None and i.type == jointNumber:
                    jointData.append(i)
                    flag = True
        if flag:
            return jointData
        else:
            return False

    # input - 2 joints lists; output - T if y(a)>y(b)
    def compareYbetweenJoints(self, jointA, jointB):
        for i in jointA:
            for j in jointB:
                if (i.y>j.y):
                    print("compareYbetweenJoints - True - camera class")
                    return True
        return False

    # Calculate angle between joints
    def calc_angle(self, joint1, joint2, joint3):
        a = self.calc_dist(joint1, joint2)
        b = self.calc_dist(joint1, joint3)
        c = self.calc_dist(joint2, joint3)
        try:
            rad_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            deg_angle = (rad_angle * 180) / math.pi

            return round(deg_angle, 2)
        except:
            print("could not calculate the angle - (Camera class)")

    # Calculate distance between joints
    def calc_dist(self, joint1, joint2):
        distance = math.hypot(joint1.x - joint2.x,
                              joint1.y - joint2.y)
        return distance

    def run_exercise(self):
        self.playRealsense()
        time.sleep(2)
        getattr(self, s.req_exercise)() # running the method of the requested exercise
        self.stopRealsense()
        if(s.success_exercise):
            if (s.relax==False):
                s.str_to_say = self.random_encouragement()
                s.tts.say_wait(s.str_to_say)
            # elif(s.relax==True):
            #     if(s.relaxname=="bend_elbows_relax"):
            #         time.sleep(1)
            #         s.screen.switch_frame(feedback_elbow)
            #         s.str_to_say = self.relax_encouragement()
            #         time.sleep(1)
            #     elif(s.relaxname=="turn_head_left"):
            #         time.sleep(1)
            #         s.screen.switch_frame(feedback_head)
            #         s.str_to_say = self.relax_encouragement()
            #         time.sleep(1)
            #     elif(s.relaxname=="smile"):
            #         time.sleep(1)
            #         s.screen.switch_frame(feedback_relax)
            #         s.str_to_say ="feedback_relax"
            #         time.sleep(1)


    def relax_encouragement(self):
        rand = random.random()
        if rand < 0.2:
            return "well done"
        elif rand < 0.4:
            return "very Good"
        elif rand < 0.6:
            return "excellent"
        elif rand < 0.8:
            return "winnergreat"
        else:
            return "robotverygood"
    def random_encouragement(self):
        #rand = random.random()
        rand=0.1 #only for testing - delete after
        #time.sleep(1)
        print("encouragement")
        if rand < 0.2:
            #s.screen.switch_frame(WellDonePage) #only for testing - remove for note after
            return "well done"
        elif rand < 0.4:
            s.screen.switch_frame(VeryGoodPage)
            return "very Good"
        elif rand<0.6:
            s.screen.switch_frame(ExcellentPage)
            return "excellent"
        elif rand <0.8:
            s.screen.switch_frame(Winnergreat)
            return "winnergreat"
        else:
            s.screen.switch_frame(robotverygood)
            return "robotverygood"

    ####### Exercises #######

    def hello_waving(self): # check if the participant waved
        list_joints = [["12", "15"]]
        while (s.req_exercise == "hello_waving"):
            print ("try hello wave")
            joints = self.getSkeletonData()
            #print(joints)
            JOINT_RIGHT_SHOULDER = self.findJointData(joints, "12")
            JOINT_RIGHT_HAND = self.findJointData(joints, "15")
            if (not JOINT_RIGHT_SHOULDER or not JOINT_RIGHT_HAND):
                continue
            new_entry = [JOINT_RIGHT_SHOULDER, JOINT_RIGHT_HAND]
            if (self.compareYbetweenJoints(JOINT_RIGHT_HAND, JOINT_RIGHT_SHOULDER)):
                s.waved = True
                print ("participant wave - (camera class")
                new_entry.append("wave")
                list_joints.append(new_entry)
                s.req_exercise = ""
                #s.str_to_say = "1"  # for check camera
            list_joints.append(new_entry)
            #Excel.wf_joints("hello_waving",list_joints)
            if(s.waved):
                return True

    def exercise_three_joints(self, exercise_name, joint_num1, joint_num2, joint_num3): #TODO add depth check
        flag = False
        counter = 0
        list_joints = [[joint_num1, joint_num2, joint_num3]]
        while (s.req_exercise == exercise_name):
            joints = self.getSkeletonData()
            joint1 = self.findJointData(joints, joint_num1)
            joint2 = self.findJointData(joints, joint_num2)
            joint3 = self.findJointData(joints, joint_num3)
            if not joint1 or not joint2 or not joint3:
                continue
            for i in range(0, len(joint1)):
                angle = self.calc_angle(joint2[i], joint3[i], joint1[i])
                new_entry = [joint1[i], joint2[i], joint3[i], angle]
                print (str(angle)+"angle")
                if ((100<angle<120) & (not flag)):
                    print("up")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("up")
                if ((angle<55) & (flag)):
                    print("down")
                    flag = False
                    print (counter)
                    new_entry.append("down")
                if (counter == s.rep):
                    s.req_exercise = ""
                    print ("finish with" + str(counter) +"- (Camera class)")
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter)+"- (Camera class)")
        print(list_joints)
        Excel.wf_joints(exercise_name,list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def exercise_six_joints(self, exercise_name, joint_r1, joint_r2, joint_r3, joint_l1, joint_l2, joint_l3, up_lb, up_ub, down_lb, down_ub): #TODO add depth check
        flag = False
        counter = 0
        list_joints = [[joint_r1, joint_r2, joint_r3, joint_l1, joint_l2, joint_l3]]
        while (s.req_exercise == exercise_name):
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, joint_r1)
            jointr2 = self.findJointData(joints, joint_r2)
            jointr3 = self.findJointData(joints, joint_r3)
            jointl1 = self.findJointData(joints, joint_l1)
            jointl2 = self.findJointData(joints, joint_l2)
            jointl3 = self.findJointData(joints, joint_l3)
            if not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                right_angle = self.calc_angle(jointr2[i], jointr3[i], jointr1[i])
                left_angle = self.calc_angle(jointl2[i], jointl3[i], jointl1[i])
                new_entry = [jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i], right_angle,
                             left_angle]
                print (right_angle)
                print (left_angle)
                if ((up_lb<right_angle<up_ub) & (up_lb<left_angle<up_ub) & (not flag)):
                    print("up")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("up")
                if ((down_lb<right_angle<down_ub) & (down_lb<left_angle<down_ub) & (flag)):
                    print("down")
                    flag = False
                    new_entry.append("down")
                    print (counter)
                if (counter == s.rep):
                    s.req_exercise = ""
                    print ("finish with" + str(counter))
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter) + "- (Camera class)")
        Excel.wf_joints(exercise_name,list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def raise_arms_horizontally_separate(self):
        while (s.req_exercise == "raise_arms_horizontally_separate"):
            continue

    def raise_right_arm_horiz(self):
        time.sleep(2.5)
        self.exercise_three_joints("raise_right_arm_horiz", "3", "12", "13")

    def raise_left_arm_horiz(self):
        self.exercise_three_joints("raise_left_arm_horiz", "3", "6", "7")

    def raise_arms_horizontally(self):
        time.sleep(2)
        self.exercise_six_joints("raise_arms_horizontally","3", "12", "13", "3", "6", "7", 90, 130, 0, 70)

    def turn_head_left(self):
        counter=0
        time.sleep(4.2)
        while (s.req_exercise=="turn_head_left"):
            counter=self.counting_flag(counter)
            if(counter>=5):
                s.relaxname = "turn_head_left"
                s.req_exercise = ""
                s.success_exercise = True

    def turn_head_down(self):
        counter = 0
        time.sleep(6.5)
        while (s.req_exercise=="turn_head_down"):
            counter = self.counting_flag(counter)

            if (counter >= 5):
                s.relaxname = "turn_head_down"
                s.req_exercise = ""
                s.success_exercise = True

    def teeth(self):
        counter = 0
        time.sleep(3.5)
        while (s.req_exercise == "teeth"):
            counter = self.counting_flag(counter)
            if (counter >= 5):
                s.relaxname = "teeth"
                s.req_exercise = ""
                s.success_exercise = True

    def eyes(self):
        counter = 0
        time.sleep(3.5)
        while (s.req_exercise == "eyes"):
            counter = self.counting_flag(counter)

            if (counter >= 5):
                s.relaxname = "eyes"
                s.req_exercise = ""
                s.success_exercise = True

    def eyebrows(self):
        counter = 0
        time.sleep(3.5)
        while (s.req_exercise == "eyebrows"):
            counter = self.counting_flag(counter)

            if (counter >= 5):
                s.relaxname = "eyebrows"
                s.req_exercise = ""
                s.success_exercise = True

    def smile(self):
        counter = 0
        time.sleep(3.5)
        while (s.req_exercise == "smile"):
            counter = self.counting_flag(counter)
            if (counter >= 5):
                s.relaxname = "smile"
                s.req_exercise = ""
                s.success_exercise = True

    def turn_head_right(self):
        counter = 0
        time.sleep(4.2)
        while (s.req_exercise=="turn_head_right"):
            counter = self.counting_flag(counter)
            if (counter >= 5):
                s.relaxname = "turn_head_right"
                s.req_exercise = ""
                s.success_exercise = True

    def bend_elbows(self):
        time.sleep(2.6)
        self.exercise_six_joints("bend_elbows", "12", "13", "15", "6", "7", "9", 0, 10, 165, 180)

    def bend_elbows_relax(self):
        counter = 0
        time.sleep(8)
        while (s.req_exercise == "bend_elbows_relax"):
            counter = self.counting_flag(counter)
            if (counter >= 5):
                s.req_exercise = ""
                s.relaxname="bend_elbows_relax"
                s.success_exercise = True

    def raise_arms_forward_static(self):
        up_time_counter = 0
        cntr=-1
        last_time = 0
        exercise_name = s.req_exercise
        list_joints = [[12, 13, 15, 6, 7, 9]]
        while (s.req_exercise == "raise_arms_forward_static") or ( s.req_exercise == "raise_arms_forward_turn" ):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                right_height = abs(jointr1[i].y - jointr3[i].y)
                left_height = abs(jointl1[i].y - jointl3[i].y)
                new_entry = [jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i], right_height,
                             left_height]
                print (right_height)
                print (left_height)
                if (right_height < 100.0) & (left_height < 100.0):
                    up_time_counter = up_time_counter + (time.time() - last_time)
                    if(cntr<7):
                        cntr=cntr+1
                        self.counting_flag(cntr)
                    print (time.time())
                    print (last_time)
                    print (up_time_counter)
                    last_time = time.time()
                    new_entry.append(cntr)
                if (up_time_counter >= s.rep or cntr>=7):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                last_time = time.time()
                list_joints.append(new_entry)
        print ("finish with " + str(up_time_counter)+"- (Camera class)")
        print(list_joints)
        Excel.wf_joints(exercise_name, list_joints)
        s.ex_list.append([exercise_name, cntr])
        if (s.success_exercise):
            return True

    def raise_arms_forward_turn(self):
        self.raise_arms_forward_static()

    def raise_right_arm_forward(self):
        flag = False
        counter = 0
        exercise_name = s.req_exercise
        list_joints = [[12, 13, 15]]
        while (s.req_exercise == "raise_right_arm_forward"):
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            if not jointr1 or not jointr2 or not jointr3:
                continue
            for i in range(0, len(jointr1)):
                right_height = abs(jointr1[i].y - jointr3[i].y)
                right_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                right_depth = abs(jointr1[i].z - jointr3[i].z)
                new_entry = [jointr1[i], jointr2[i], jointr3[i], right_height, right_angle, right_depth]
                print (right_height)
                print (right_angle)
                print (right_depth)
                print (flag)
                if (right_height < 80.0) &  (right_depth>300) & (not flag):
                    print ("up")
                    counter = self.counting_flag(counter)
                    print(counter)
                    flag = True
                    new_entry.append("up")
                if (150 < right_angle <= 200) & (right_depth<100) & flag:
                    print ("down")
                    flag = False
                    new_entry.append("down")
                if (counter == s.rep):
                    s.req_exercise = ""
                    print ("finish with" + str(counter))
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter) +"- (Camera class)")
        print(list_joints)
        Excel.wf_joints(exercise_name,list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def raise_left_arm_forward(self):
        flag = False
        counter = 0
        exercise_name = s.req_exercise
        list_joints = [[6, 7, 9]]
        while (s.req_exercise == "raise_left_arm_forward"):
            joints = self.getSkeletonData()
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointl1)):
                left_height = abs(jointl1[i].y - jointl3[i].y)
                left_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                left_depth = abs(jointl1[i].z - jointl3[i].z)
                new_entry = [jointl1[i], jointl2[i], jointl3[i], left_height, left_angle, left_depth]
                if (left_height < 80.0) & (left_depth>300) & (not flag):
                    print ("up")
                    counter = self.counting_flag(counter)
                    print(counter)
                    flag = True
                    new_entry.append("up")
                if (170 < left_angle < 180) & (left_depth<100) & flag:
                    print ("down")
                    flag = False
                    new_entry.append("down")
                if (counter == s.rep):
                    s.req_exercise = ""
                    print ("finish with" + str(counter))
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter) +"- (Camera class)")
        print(list_joints)
        Excel.wf_joints(exercise_name, list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def raise_arms_forward_separate(self):
        while (s.req_exercise == "raise_arms_forward_separate"):
            continue

    def raise_arms_forward(self):
        flag = False
        counter = 0
        exercise_name = s.req_exercise
        list_joints = [[12, 13, 15, 6, 7, 9]]
        while (s.req_exercise == "raise_arms_forward"):
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_height = abs(jointl1[i].y - jointl3[i].y )
                left_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                left_depth = abs(jointl1[i].z - jointl3[i].z)
                right_height = abs(jointr1[i].y - jointr3[i].y)
                right_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                right_depth = abs(jointr1[i].z - jointr3[i].z)
                new_entry = [jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i], right_angle,
                             left_angle, right_height, left_height,right_depth,left_depth]
                if (left_height < 80.0) & (right_height < 80.0) & (right_depth>300) & (left_depth>300) & (not flag):
                    print ("up")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("up")
                if (160 < left_angle < 190) & (150 < right_angle < 200) & (right_depth<100) & (left_depth<80) & (flag):
                    print ("down")
                    flag = False
                    new_entry.append("down")
                if counter == s.rep:
                    s.req_exercise = ""
                    print ("finish with" + str(counter))
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter) + "- (Camera class)")
        print(list_joints)
        Excel.wf_joints(exercise_name, list_joints)
        s.ex_list.append([exercise_name, counter])
        if s.success_exercise:
            return True

    def raise_arms_bend_elbows(self):
        flag = False
        counter = 0
        exercise_name = s.req_exercise
        list_joints = [[3, 12, 13, 15, 6, 7, 9]]
        while (s.req_exercise == "raise_arms_bend_elbows"):
            joints = self.getSkeletonData()
            joint_torso = self.findJointData(joints, "3")
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not joint_torso or not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_armpit_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                left_elbow_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                right_armpit_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                right_elbow_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                new_entry =[joint_torso[i], jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i],
                            jointl3[i], right_armpit_angle, left_armpit_angle, right_elbow_angle,
                            left_elbow_angle]
                print (left_armpit_angle)
                print (left_elbow_angle)
                print (right_armpit_angle)
                print (right_elbow_angle)
                if ((100<left_armpit_angle<120 and 100<right_armpit_angle<120) and (0<left_elbow_angle<20 and 0<right_elbow_angle<20) and (not flag)):
                    print("close")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("close")
                if ((100<left_armpit_angle<120 and 100<right_armpit_angle<120) and (140<left_elbow_angle<180 and 140<right_elbow_angle<180) and (flag)):
                    print("open")
                    flag = False
                    print (counter)
                    new_entry.append("open")
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter) +"- (Camera class)")
        print(list_joints)
        Excel.wf_joints(exercise_name, list_joints)
        s.ex_list.append([exercise_name, counter])
        if (s.success_exercise):
            return True

    def raise_arms_horizontally_turn(self):
        up_time_counter = 0
        cntr = -1
        list_joints = [[3,12,13,6,7]]
        while (s.req_exercise == "raise_arms_horizontally_turn"):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            joint_torso = self.findJointData(joints, "3")
            if not joint_torso or not jointr1 or not jointr2 or not jointl1 or not jointl2:
                continue
            for i in range(0, len(jointr1)):
                right_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                left_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                new_entry = [joint_torso[i], jointr1[i], jointr2[i], jointl1[i], jointl2[i], right_angle, left_angle]
                print (right_angle)
                print (left_angle)
                if (100 < right_angle < 120) and (100 < left_angle < 120):
                    up_time_counter = up_time_counter + (time.time() - last_time)
                    print (up_time_counter)
                    if (cntr < 7):
                        cntr = cntr + 1
                        self.counting_flag(cntr)
                    last_time = time.time()
                if (up_time_counter >= s.rep or cntr>=7):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print(list_joints)
        Excel.wf_joints("raise_arms_horiz_turn", list_joints)
        s.ex_list.append(["raise_arms_horiz_turn", cntr])
        if (s.success_exercise):
            return True

    def raise_arms_90_and_up (self):
        flag = False
        counter = 0
        while (s.req_exercise == "raise_arms_90_and_up"):
            joints = self.getSkeletonData()
            joint_torso = self.findJointData(joints, "3")
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not joint_torso or not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_armpit_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                left_elbow_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                right_armpit_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                right_elbow_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                print (left_armpit_angle)
                print (left_elbow_angle)
                print (right_armpit_angle)
                print (right_elbow_angle)
                if ((130 < left_armpit_angle < 180 and 130 < right_armpit_angle < 180) and (
                        100 < left_elbow_angle < 145 and 100 < right_elbow_angle < 145) and (not flag)):
                    print("close")
                    counter = self.counting_flag(counter)
                    flag = True
                if ((95 < left_armpit_angle < 125 and 95 < right_armpit_angle < 125) and (
                        70 < left_elbow_angle < 95 and 70 < right_elbow_angle < 95) and (flag)):
                    print("open")
                    flag = False
                    print (counter)
                if (counter == s.rep):
                    s.req_exercise = ""
                    print ("finish with" + str(counter) +"- (Camera class)")
                    s.success_exercise = True
                    return True

    def open_hands_and_raise_up(self):
        self.exercise_six_joints("open_hands_and_raise_up", "3", "12", "13", "3", "6", "7", 160, 180, 100, 120)

    def open_arms_and_forward(self):
        flag = False
        counter = 0
        list_joints = [[3, 12, 13, 15, 6, 7, 9]]
        while (s.req_exercise == "open_arms_and_forward"):
            joints = self.getSkeletonData()
            joint_torso = self.findJointData(joints, "3")
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not joint_torso or not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_height = abs(jointl1[i].y - jointl3[i].y )
                left_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                left_depth = abs(jointl1[i].z-jointl3[i].z)
                right_height = abs(jointr1[i].y - jointr3[i].y)
                right_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                right_depth = abs(jointr1[i].z - jointr3[i].z)
                new_entry = [joint_torso[i], jointr1[i], jointr2[i], jointr3[i], jointl1[i], jointl2[i], jointl3[i],
                             right_height, left_height, right_angle, left_angle, right_depth, left_depth]
                print (left_depth)
                print (right_depth)
                print (left_height)
                print (left_angle)
                print (right_height)
                print (right_angle)
                if (left_height < 70.0) & (right_height < 70.0) & (right_depth>300) & (left_depth>300) & (not flag):
                    print ("close")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("close")
                if (90 < left_angle < 120) & (90 < right_angle < 120) & (right_depth<70) & (left_depth<70) & (flag):
                    print ("open")
                    new_entry.append("open")
                    flag = False
                if (counter == s.rep):
                    s.req_exercise = ""
                    print ("finish with" + str(counter) )
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter) +"- (Camera class)")
        Excel.wf_joints("open_arms_and_forward", list_joints)
        s.ex_list.append(["open_arms_and_forward", counter])
        if (s.success_exercise):
            return True

    def open_and_close_arms_90(self):
        time.sleep(7.1)
        flag = False
        counter = 0
        list_joints = [[3, 12, 13, 15, 6, 7, 9]]
        while (s.req_exercise == "open_and_close_arms_90"):
            joints = self.getSkeletonData()
            joint_torso = self.findJointData(joints, "3")
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not joint_torso or not jointr1 or not jointr2 or not jointr3 or not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointr1)):
                left_armpit_angle = self.calc_angle(jointl1[i], joint_torso[i], jointl2[i])
                left_elbow_angle = self.calc_angle(jointl2[i], jointl1[i], jointl3[i])
                right_armpit_angle = self.calc_angle(jointr1[i], joint_torso[i], jointr2[i])
                right_elbow_angle = self.calc_angle(jointr2[i], jointr1[i], jointr3[i])
                left_height = abs(jointl1[i].y - jointl2[i].y)
                left_depth = abs(jointl1[i].z - jointl2[i].z)
                right_height = abs(jointr1[i].y - jointr2[i].y)
                right_depth = abs(jointr1[i].z - jointr2[i].z)
                new_entry = [joint_torso[i], jointr1[i], jointr2[i], jointr3[i],jointl1[i], jointl2[i], jointl3[i],
                             right_armpit_angle, left_armpit_angle,right_elbow_angle, left_elbow_angle,
                             right_height, left_height, right_depth, left_depth]
                print (left_armpit_angle)
                print (left_elbow_angle)
                print (right_armpit_angle)
                print (right_elbow_angle)
                print (left_height)
                print (left_depth)
                print (right_height)
                print (right_depth)
                if (left_height <70) & (right_height <70)& (right_depth>200) & (left_depth>200) & (not flag):
                    print("close - try to say outside the function")
                    counter = self.counting_flag(counter)
                    flag = True
                    new_entry.append("close")
                if ((90 < left_armpit_angle < 130 and 90 < right_armpit_angle < 130) and (60 < left_elbow_angle < 110 and 60 < right_elbow_angle < 110) and (right_depth<100) and (left_depth<100) and(flag)):
                    print("open")
                    new_entry.append("open")
                    flag = False
                    print (flag)
                if (counter == s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    break
                list_joints.append(new_entry)
        print ("finish with" + str(counter))
        Excel.wf_joints("open_and_close_arms_90", list_joints)
        s.ex_list.append(["open_and_close_arms_90", counter])
        if (s.success_exercise):
            return True

    def raise_arms_and_lean(self): #todo fill
        while (s.req_exercise == "raise_arms_and_lean"):
            continue

    def raise_left_arm_and_lean(self):
        up_time_counter = 0
        print("try - raise_left_arm_and_lean")
        while (s.req_exercise == "raise_left_arm_and_lean"):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointl1 = self.findJointData(joints, "6")
            jointl2 = self.findJointData(joints, "7")
            jointl3 = self.findJointData(joints, "9")
            if not jointl1 or not jointl2 or not jointl3:
                continue
            for i in range(0, len(jointl1)):
                right_height = abs(jointl1[i].y - jointl3[i].y)
                print (right_height)
                if (right_height > 300):
                    #up_time_counter = up_time_counter + (time.time() - last_time)
                    up_time_counter = self.counting_flag(up_time_counter)
                    print("time -> last time-> number ")
                    print (time.time())
                    print (last_time)
                    print (up_time_counter)
                    last_time = time.time()
                if (up_time_counter >= s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    print ("finish with " + str(up_time_counter))
                    return True
                last_time = time.time()

    def raise_right_arm_and_lean(self):
        up_time_counter = 0
        print ("try - raise_right_arm_and_lean")
        while (s.req_exercise == "raise_right_arm_and_lean"):
            last_time = time.time()
            joints = self.getSkeletonData()
            jointr1 = self.findJointData(joints, "12")
            jointr2 = self.findJointData(joints, "13")
            jointr3 = self.findJointData(joints, "15")
            if not jointr1 or not jointr2 or not jointr3:
                continue
            for i in range(0, len(jointr1)):
                right_height = abs(jointr1[i].y - jointr3[i].y)
                print (right_height)
                if (right_height > 300):
                    #up_time_counter = up_time_counter + (time.time() - last_time)
                    up_time_counter = self.counting_flag(up_time_counter)
                    print("time -> last time-> number ")
                    print (time.time())
                    print (last_time)
                    print (up_time_counter)
                    last_time = time.time()
                if (up_time_counter >= s.rep):
                    s.req_exercise = ""
                    s.success_exercise = True
                    print ("finish with raise_right_arm_and_lean" + str(up_time_counter))
                    return True
                last_time = time.time()

    # def raise_hands_and_fold_backward(self): #todo fill

    def counting_flag(self, counter):
        print("try to say in function")
        counter = counter + 1
        s.str_to_say=str(counter)
        s.tts.say_wait(s.str_to_say)
        #time.sleep(1.5)
        # if counter == 1:
        #     numberstr= "OnePage"
        # s.screen.switch_frame(numberstr)
        print ("say " + str(counter))
        return (counter)

    def run(self):
        print ("camera start" + "- (Camera class)")
        while (not s.finish_workout):
            if (s.req_exercise != ""):
                print ("camera starting: " + str(s.req_exercise) + "- (Camera class)")
                self.run_exercise()
                if (s.success_exercise):#only for testing cameraNew separete
                    s.finish_workout=True
                    break
        Excel.close_workbook()  # only for camera check - delete after
        print ("camera done - (Camera class)")


#for tests
if __name__ == '__main__':
    s.rep = 4
    language = 'Hebrew'
    gender = 'Female'
    #for the robot path
    #s.realsense_path = "C:\\Users\\owner\\Documents\\nuitrack-sdk-master\\Examples\\nuitrack_console_sample\\out\\build\\x64-Debug\\nuitrack_console_sample.exe"
    #simulator Path
    #s.realsense_path="C:\\Users\\TEMP.NAAMA\\Documents\\nuitrack-sdk-master\\Examples\\nuitrack_console_sample\\out\\build\\x64-Debug\\nuitrack_console_sample.exe"
    s.realsense_path = R'C:\git\poppyCode\greatoded\nuitrack\Examples\nuitrack_console_sample\out\build\x64-Debug\nuitrack_console_sample.exe'
    s.excel_path = R'C:/Git/poppyCode/greatoded/excel_folder/'
    s.general_path = R'C:/Git/poppyCode/greatoded/'
    s.pic_path = s.general_path + 'Pictures/'
    s.audio_path = s.general_path + 'audioFiles/' + '/' + language + '/' + gender + '/'
    Excel.create_workbook()
    s.str_to_say = ""
    s.tts = TTS()
    s.relax = False
    s.waved = False
    s.finish_workout = False
    s.success_exercise = False
    #testing - works:
    #s.req_exercise = "hello_waving"
    #number 1:
    # s.req_exercise="raise_arms_horizontally_separate"
    # s.req_exercise = "raise_left_arm_horiz"
    # s.req_exercise = "raise_right_arm_horiz"
    #number 2:
    # s.req_exercise="raise_arms_horizontally"
    #number 3:
    # s.req_exercise="bend_elbows"
    #number 4- more checking!
    #s.req_exercise="raise_arms_forward_static"
    #number 5:
    #s.req_exercise="raise_arms_bend_elbows"
    #number 6 - more checking!
    #s.req_exercise="raise_arms_horizontally_turn"
    #number 7 - need more work:
    #s.req_exercise="raise_arms_forward"
    # number 8 - dosent work:
    #s.req_exercise = "raise_arms_forward_separate"
    # number 8 - dosent work:
    #s.req_exercise = "raise_arms_forward_separate"
    #s.req_exercise = "raise_right_arm_forward"
    #s.req_exercise = "raise_left_arm_forward" - works
    # number 9:
    #s.req_exercise = "raise_arms_90_and_up"
    # number 11:
    #s.req_exercise = "open_arms_and_forward"
    # number 13:
    #s.req_exercise = "open_hands_and_raise_up"
    # number 14:
    #s.req_exercise = "open_and_close_arms_90"
    # number 17:
    #s.req_exercise = "raise_arms_forward_turn"
    s.camera = Camera()
    s.camera.start()



"""
self.raise_arms_horizontally_separate
self.raise_arms_horizontally
self.bend_elbows,
self.raise_arms_forward_static,
self.raise_arms_bend_elbows
self.raise_arms_horizontally_turn
self.raise_arms_forward,
self.raise_arms_forward_separate,
self.raise_arms_90_and_up
self.raise_arms_and_lean_dynmic
self.open_arms_and_forward,
self.raise_hands_and_fold_backward,
self.open_hands_and_raise_up
self.open_and_close_arms_90
self.open_and_close_arms_90,
self.open_and_down_arms_90,
self.to_90_and_down_arms
self.raise_arms_forward_turn
"""