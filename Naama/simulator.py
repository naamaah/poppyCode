import os
import time
import subprocess

#path = R'"C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\coppeliaSim.exe"'\

def createSim():
    #path=R'C:\Program Files (x86)\V-REP3\V-REP_PRO_EDU\vrep.exe'
    path=R'C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\coppeliaSim.exe'
    os.startfile(path)
    #todo check another screen

def closeSim():
    subprocess.call('TASKKILL /F /IM coppeliaSim.exe')
    #subprocess.call('TASKKILL /F /IM vrep.exe')
    print("simulation close")


if __name__ == "__main__":
    fd=createSim()
    time.sleep(15)
    closeSim()

