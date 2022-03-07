import sys, os, time
import threading
import Settings as s #Global settings variables


class Realsense (threading.Thread) :

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        os.system(s.realsense_path)
        print("running")

    def stop(self):
        os.system("taskkill /f /im  nuitrack_console_sample.exe")
        print("stop realsense"+str(self.is_alive()))

if __name__ == '__main__':
    s.realsense_path = "C:\\Users\\TEMP.NAAMA\\Documents\\nuitrack-sdk-master\\Examples\\nuitrack_console_sample\\out\\build\\x64-Debug\\nuitrack_console_sample.exe"
    r = Realsense()
    r.run()
