import time
from pypot.creatures import PoppyTorso

import Poppy
import simulator

#simulator.createSim()
#time.sleep(10)
poppy = PoppyTorso(simulator='vrep')
print("Poppy class - init_robot function")
for m in poppy.motors:
    m.goto_position(0, 1, wait=True)
    m.speed=350
poppy.r_elbow_y.goto_position(90, 1, wait=True)
poppy.l_elbow_y.goto_position(90, 1, wait=True)
time.sleep(1)

#up to 90
poppy.l_arm_z.goto_position(90, 1.5, wait=False)
poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)
poppy.l_shoulder_x.goto_position(90, 1.5, wait=False)
poppy.r_elbow_y.goto_position(0, 1.5, wait=False)
poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
time.sleep(1)

poppy.l_arm_z.goto_position(0, 1.5, wait=False)
poppy.r_arm_z.goto_position(0, 1.5, wait=True)


# #elboys -clock direction -  TODO change not good enough
# l_shoulderY=[-90,-90,-90,30,30]
# l_armZ=     [-90,-90,-90,-5,-5]
# l_shoulderX=[50,50,50, 90,90]
# l_elbowY=   [-50,0,90,-10,-50]
#
# r_shoulderY=[-90,-90,-90,30,30]
# r_armZ=     [90,90,90,5,5]
# r_shoulderX=[-50,-50,-50,-90,-90]
# r_elbowY=   [-50,0,90,-10,-50]
#
# for num in range(10):
#     for i in range(len(l_elbowY)):
#         poppy.l_shoulder_y.goto_position(l_shoulderY[i], 1, wait=False)
#         poppy.r_shoulder_y.goto_position(r_shoulderY[i], 1, wait=False)
#         poppy.l_arm_z.goto_position(l_armZ[i], 1, wait=False)
#         poppy.r_arm_z.goto_position(r_armZ[i], 1, wait=False)
#         poppy.l_shoulder_x.goto_position(l_shoulderX[i], 1, wait=False)
#         poppy.r_shoulder_x.goto_position(r_shoulderX[i], 1, wait=False)
#         poppy.l_elbow_y.goto_position(l_elbowY[i], 1, wait=False)
#         poppy.r_elbow_y.goto_position(r_elbowY[i], 1, wait=True)
#
# #init
# poppy.l_shoulder_y.goto_position(0, 1, wait=False)
# poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
# poppy.l_arm_z.goto_position(0, 1, wait=False)
# poppy.r_arm_z.goto_position(0, 1.5, wait=False)
# poppy.l_shoulder_x.goto_position(0, 1, wait=False)
# poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
# poppy.l_elbow_y.goto_position(90, 1, wait=False)
# poppy.r_elbow_y.goto_position(90, 1, wait=True)

# #head - clock direction WORKSSSSSS
# headZ_degree=[-100,-50,0,50,100]
# for num in range(4):
#     # down
#     poppy.head_y.goto_position(8, 1, wait=False)
#     for i in range(len(headZ_degree)):
#         poppy.head_z.goto_position(headZ_degree[i], 1.5, wait=True)
#     # up
#     poppy.head_y.goto_position(-40, 1, wait=False)
#     for i in range(len(headZ_degree)):
#         poppy.head_z.goto_position(headZ_degree[len(headZ_degree) - 1 - i], 1.5, wait=True)
#
# poppy.head_y.goto_position(-20, 1, wait=False)
# poppy.head_z.goto_position(0, 1, wait=True)

# headZ_degree=[-100,-50,0,50,100]
# for num in range(4):
#     # down
#     poppy.head_y.goto_position(8, 1, wait=False)
#     for i in range(len(headZ_degree)):
#         poppy.head_z.goto_position(headZ_degree[len(headZ_degree) - 1 - i], 1.5, wait=True)
#     # up
#     poppy.head_y.goto_position(-40, 1, wait=False)
#     for i in range(len(headZ_degree)):
#         poppy.head_z.goto_position(headZ_degree[i], 1.5, wait=True)
#
# poppy.head_y.goto_position(-20, 1, wait=False)
# poppy.head_z.goto_position(0, 1, wait=True)


# #appluase
# poppy.r_elbow_y.goto_position(-25, 1, wait=True)
# poppy.l_elbow_y.goto_position(-20, 1, wait=True)
# for i in range(4):
#     poppy.r_arm_z.goto_position(45, 1, wait=False)
#     poppy.l_arm_z.goto_position(-45, 1, wait=True)
#     time.sleep(1)
#     poppy.r_arm_z.goto_position(0, 1, wait=False)
#     poppy.l_arm_z.goto_position(0, 1, wait=True)
#
# time.sleep(2)



#strech
#head
#my left
# poppy.head_y.goto_position(0,1,wait=True)
# poppy.head_z.goto_position(-50,1,wait=True)
# time.sleep(5)
# #my right
# poppy.head_z.goto_position(50,1,wait=True)
# time.sleep(5)

#back hands
#hands up
# poppy.l_shoulder_y.goto_position(-200, 1.5, wait=False)
# poppy.r_shoulder_y.goto_position(-200, 1.5, wait=False)
# poppy.l_shoulder_x.goto_position(-10, 1.5, wait=False)
# poppy.r_shoulder_x.goto_position(10, 1.5, wait=False)
# poppy.head_y.goto_position(40,1,wait=True)
# time.sleep(0.5)

# #left band
# poppy.l_elbow_y.goto_position(-20, 1.5, wait=True)
# poppy.l_arm_z.goto_position(-40, 1.5, wait=False)
# poppy.r_arm_z.goto_position(80, 1.5, wait=False)
# poppy.r_elbow_y.goto_position(0, 1.5, wait=True)
# time.sleep(5)
#
# #hands up
# poppy.l_shoulder_y.goto_position(-200, 1.5, wait=False)
# poppy.r_shoulder_y.goto_position(-200, 1.5, wait=False)
# poppy.l_shoulder_x.goto_position(-10, 1.5, wait=False)
# poppy.r_shoulder_x.goto_position(10, 1.5, wait=False)
# poppy.l_arm_z.goto_position(0, 1.5, wait=False)
# poppy.r_arm_z.goto_position(0, 1.5, wait=False)
# poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
# poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
# poppy.head_y.goto_position(40,1,wait=True)
# time.sleep(0.5)

#right band
# poppy.r_elbow_y.goto_position(-20, 1.5, wait=True)
# poppy.r_arm_z.goto_position(40, 1.5, wait=False)
# poppy.l_arm_z.goto_position(-70, 1.5, wait=False)
# poppy.l_elbow_y.goto_position(0, 1.5, wait=True)
# time.sleep(5)

# #open hands
# poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
# poppy.l_shoulder_x.goto_position(90, 1, wait=False)
# poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
# poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
# time.sleep(2)
#
# #left strech
# poppy.abs_z.goto_position(-15, 1, wait=False)
# poppy.head_z.goto_position(50,1,wait=False)
# #left
# poppy.l_shoulder_y.goto_position(-90, 1, wait=False)
# poppy.l_shoulder_x.goto_position(-120, 1, wait=True)
# #right
# poppy.r_shoulder_y.goto_position(-50, 1.5, wait=False)
# poppy.r_arm_z.goto_position(30,1.5,wait=False)
# poppy.r_shoulder_x.goto_position(20, 1.5, wait=False)
# poppy.r_elbow_y.goto_position(30, 1.5, wait=True)
# time.sleep(5)
#
# #init
# poppy.abs_z.goto_position(0, 1, wait=False)
# poppy.head_z.goto_position(0,1,wait=False)
# poppy.l_shoulder_y.goto_position(0, 1, wait=False)
# #poppy.l_shoulder_x.goto_position(0, 1, wait=False)
# poppy.r_shoulder_y.goto_position(0, 1.5, wait=False)
# poppy.r_arm_z.goto_position(0,1.5,wait=False)
# poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
# poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
# poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
#
# #open hands
# poppy.l_shoulder_x.goto_position(90, 1.5, wait=True)
# poppy.r_shoulder_x.goto_position(-90, 1, wait=False)
# poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
# poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
# time.sleep(2)
# for m in poppy.motors:
#     print( str(m.name)+" "+str(m.present_position))
#
# #right strech
# poppy.abs_z.goto_position(30, 1, wait=False)
# poppy.head_z.goto_position(-50,1,wait=False)
# #right
# poppy.r_shoulder_y.goto_position(-90, 1, wait=False)
# poppy.r_shoulder_x.goto_position(120, 1, wait=True)
# #left
# poppy.l_shoulder_y.goto_position(-50, 1.5, wait=False)
# poppy.l_arm_z.goto_position(-30,1.5,wait=False)
# poppy.l_shoulder_x.goto_position(-20, 1.5, wait=False)
# poppy.l_elbow_y.goto_position(30, 1.5, wait=True)
# time.sleep(5)





