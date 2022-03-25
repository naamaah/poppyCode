import threading
import Settings as s
from pygame import mixer
import pygame
import time
import librosa
import math



class TTS():
    def say_wait(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        if (str_to_say!=""):
            print("say_wait function - (tts class) " + str_to_say)
            mixer.init()
            fileName=s.audio_path+str_to_say+'.wav'
            mixer.music.load(fileName)
            mixer.music.play()
            duration=librosa.get_duration(filename=fileName)
            time.sleep(int(math.ceil(duration)))
            print("done saying")

    def say_no_wait(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        if (str_to_say != ""):
            print("say_no_wait function - (tts class) " + str_to_say)
            mixer.init()
            fileName=s.audio_path+str_to_say+'.wav'
            mixer.music.load(fileName)
            mixer.music.play()




if __name__ == '__main__':
    language = 'Hebrew'
    gender = 'Female'
    s.finish_workout=False
    s.general_path=R'C:/Git/poppyCode/greatoded/'
    s.audio_path = s.general_path + 'audioFiles/' + language + '/' + gender + '/'
    tts = TTS()
    tts.say_no_wait('bend_elbows_relax')



