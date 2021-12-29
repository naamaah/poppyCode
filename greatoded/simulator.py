import os
import time

#path = R'"C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\coppeliaSim.exe"'\

def createSim():
    #path=R'C:\Program Files (x86)\V-REP3\V-REP_PRO_EDU\vrep.exe'
    path=R'C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\coppeliaSim.exe'
    os.startfile(path)



def closeSim():
    os.system('TASKKILL /F /IM coppeliaSim.exe')
    #os.system('TASKKILL /IM coppeliaSim.exe')

    print("simulation close")
    # os.system('shutdown -s -t 0') #delete for sumulation


if __name__ == "__main__":
    fd=createSim()
    time.sleep(16)
    closeSim()

