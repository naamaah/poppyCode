import time
from pypot.creatures import PoppyTorso

poppy = PoppyTorso(simulator='vrep')
for i in range(4):
    right_hand_up = [poppy.r_shoulder_x.goto_position(-90, 1.7, wait=False),
                     poppy.r_elbow_y.goto_position(90, 1.7, wait=False)]
    time.sleep(2)
    right_hand_down = [poppy.r_shoulder_x.goto_position(0, 1.7, wait=False),
                       poppy.r_elbow_y.goto_position(90, 1.7, wait=False)]
    time.sleep(2)

