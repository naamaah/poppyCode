import time
from pypot.creatures import PoppyTorso

import Poppy
import simulator

#simulator.createSim()
#time.sleep(10)
poppy = PoppyTorso(simulator='vrep')
print("Poppy class - init_robot function")
for m in poppy.motors:
    if not m.name == 'r_elbow_y' and not m.name == 'l_elbow_y' and not m.name == 'head_y':
        m.goto_position(0, 1, wait=True)
poppy.r_elbow_y.goto_position(90, 1, wait=True)
poppy.l_elbow_y.goto_position(90, 1, wait=True)
poppy.head_y.goto_position(-20,1,wait=True)
time.sleep(1)

#open hands aside - function exist
poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
poppy.l_shoulder_x.goto_position(90, 1, wait=False)
poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
poppy.l_elbow_y.goto_position(90, 1.5, wait=True)

for i in range(4):
    #first move
    l_hand_band = [poppy.l_shoulder_y.goto_position(-90, 2, wait=False),
              poppy.l_arm_z.goto_position(-90, 2, wait=False),
              poppy.l_shoulder_x.goto_position(50, 2, wait=False),
              poppy.l_elbow_y.goto_position(-50, 2, wait=True)]
    time.sleep(3)
    poppy.l_elbow_y.goto_position(0, 2, wait=True)
    time.sleep(3)
    poppy.l_elbow_y.goto_position(90, 2, wait=True)
    time.sleep(3)
    poppy.l_shoulder_x.goto_position(90, 1, wait=False)
    poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
    time.sleep(8)

    # r_hand = [poppy.r_shoulder_y.goto_position(-90, 2, wait=False),
    #           poppy.r_arm_z.goto_position(90, 2, wait=False),
    #           poppy.r_shoulder_x.goto_position(-50, 2, wait=False),
    #           poppy.r_elbow_y.goto_position(-50, 2, wait=True)]


#init
poppy.l_arm_z.goto_position(0, 1.5, wait=False)
poppy.r_arm_z.goto_position(0, 1.5, wait=False)
poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_x.goto_position(0, 1.5, wait=True)

"""
#head - clock direction WORKSSSSSS
headZ_degree=[-100,-50,0,50,100]
for num in range(4):
    # down
    poppy.head_y.goto_position(8, 1, wait=False)
    for i in range(len(headZ_degree)):
        poppy.head_z.goto_position(headZ_degree[i], 1, wait=True)
    # up
    poppy.head_y.goto_position(-40, 1, wait=False)
    for i in range(len(headZ_degree)):
        poppy.head_z.goto_position(headZ_degree[len(headZ_degree) - 1 - i], 1, wait=True)

poppy.head_y.goto_position(-20, 1, wait=False)
poppy.head_z.goto_position(0, 1, wait=True)
"""




"""

r_elbowY_degree=[0,100,150,100]
r_armZ_degree=[90,0,0,-90]
for num in range(4):
    print("start"+str(num))
    for i in range(len(r_elbowY_degree)):
        poppy.r_arm_z.goto_position(r_armZ_degree[i], 1, wait=True)
        poppy.r_elbow_y.goto_position(r_elbowY_degree[i], 1, wait=True)
        time.sleep(2)
    print("finished" +str(num))
    #for i in range(len(r_elbowY_degree)):
     #   poppy.r_elbow_y.goto_position(len(r_elbowY_degree)-1-i, 1, wait=True)
      #  poppy.r_arm_z.goto_position(len(r_armZ_degree) - 1 - i, 1, wait=True)


poppy.r_elbow_y.goto_position(90, 1, wait=False)
poppy.r_shoulder_x.goto_position(0, 1, wait=False)
poppy.l_shoulder_x.goto_position(0, 1, wait=False)
poppy.r_arm_z.goto_position(0, 1, wait=True)






for m in poppy.motors:
    print(m.name+" "+str(m.present_position))



#function number9
print("try the exercise")
poppy.l_arm_z.goto_position(90, 1.5, wait=False)
poppy.r_arm_z.goto_position(-90, 1.5, wait=False)

print("start the movment")
for i in range(4):
    poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
    poppy.l_shoulder_x.goto_position(90, 1, wait=False)
    poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
    poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
    time.sleep(1)
    poppy.r_shoulder_x.goto_position(-150, 1, wait=False)
    poppy.l_shoulder_x.goto_position(150, 1, wait=False)
    poppy.r_elbow_y.goto_position(60, 1.5, wait=False)
    poppy.l_elbow_y.goto_position(60, 1.5, wait=False)
    time.sleep(1)
    print("finished"+str(i))

#init
poppy.l_arm_z.goto_position(0, 1, wait=False)
poppy.r_arm_z.goto_position(0, 1., wait=False)
poppy.r_shoulder_x.goto_position(0, 1, wait=False)
poppy.l_shoulder_x.goto_position(0, 1, wait=False)
poppy.r_elbow_y.goto_position(90, 1, wait=True)
poppy.l_elbow_y.goto_position(90, 1, wait=True)
print("finished init")


#number=2
for i in range(4):
    hands_up = [poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
    time.sleep(2)
    hands_down = [poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                  poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                  poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                  poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
    time.sleep(2)
    

#numbe10
poppy.l_arm_z.goto_position(90, 1.5, wait=False)
poppy.l_shoulder_x.goto_position(150, 1.5, wait=False)
poppy.l_elbow_y.goto_position(30, 1.5, wait=False)
poppy.bust_x.goto_position(20, 1.5, wait=False)
poppy.bust_y.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_x.goto_position(-30, 1.5, wait=False)
time.sleep(2)
#init
poppy.l_arm_z.goto_position(0, 1.5, wait=False)
poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
poppy.bust_x.goto_position(0, 1.5, wait=False)
poppy.bust_y.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
time.sleep(2)


#number12
print("before")
poppy.l_shoulder_y.goto_position(-180, 1.5, wait=False)
poppy.r_shoulder_y.goto_position(-180, 1.5, wait=False)
poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)

print("start the ex")
for i in range(4):
        poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        time.sleep(1)
        poppy.l_elbow_y.goto_position(-20, 1.5, wait=False)
        poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
        time.sleep(1)
        print("finiehed "+str(i))



print("start init")
poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
print("done init")


for i in range(4):
    print("open hands "+str(i+1))
    poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
    poppy.l_shoulder_x.goto_position(90, 1, wait=False)
    poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
    poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
    time.sleep(1)
    print("close hands " + str(i + 1))
    poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
    poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
    poppy.l_shoulder_x.goto_position(5, 1.5, wait=False)
    poppy.r_shoulder_x.goto_position(-5, 1.5, wait=True)
    time.sleep(1)


    # init
#poppy.l_arm_z.goto_position(0, 1.5, wait=False)
#poppy.r_arm_z.goto_position(0, 1.5, wait=False)
print("init")
poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
poppy.l_elbow_y.goto_position(90, 1.5, wait=True)


#13

poppy.l_arm_z.goto_position(90, 1.5, wait=False)
poppy.r_arm_z.goto_position(-90, 1.5, wait=False)
for i in range(4):
        poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
        poppy.l_shoulder_x.goto_position(90, 1, wait=False)
        poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
        poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(0.5)
        poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        poppy.l_shoulder_x.goto_position(10, 1.5, wait=False)
        poppy.r_shoulder_x.goto_position(-10, 1.5, wait=False)
        poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
        poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
        time.sleep(1)

# init
poppy.l_arm_z.goto_position(0, 1.5, wait=False)
poppy.r_arm_z.goto_position(0, 1.5, wait=False)
poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)















"""



