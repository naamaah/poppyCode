import threading
import Settings as s
from pygame import mixer
import pygame
import time
import librosa
import math
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os




class TTS():
    def __init__(self):
        print("TTS start")
        name=str(s.subjectNum)
        folder_path = s.audio_path + name
        print(folder_path)
        # if (s.sessionNumber == 1):
        #     os.mkdir(folder_path)
        #     print("create folder")


    def say_wait(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        if (str_to_say!="" and str_to_say!='15'):
            print("say_wait function - (tts class) " + str_to_say)
            mixer.init()
            fileName=s.audio_path+str_to_say+'.wav'
            mixer.music.load(fileName)
            mixer.music.play()
            duration=librosa.get_duration(filename=fileName)
            time.sleep(int(math.ceil(duration)))
            print("done saying")

    def say_wait_comb(self, str_to_say, path):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        if (str_to_say!="" and str_to_say!='15'):
            print("say_wait function - (tts class) " + str_to_say)
            mixer.init()
            fileName=path
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
        if (str_to_say != ""  and str_to_say!='15'):
            print("say_no_wait function - (tts class) " + str_to_say)
            mixer.init()
            fileName=s.audio_path+str_to_say+'.wav'
            mixer.music.load(fileName)
            mixer.music.play()

    def combainedAudio(self, audio_clip_paths, fileName):
        """
        :param audio_clip_paths: list of path of the audio - get only name in the funation change to =>s.audio_path + name+ '.wav'
        :param fileName: the name of the new Audio combination
        :return: say the audio
        """
        print("insde")
        name = str(s.subjectNum)
        folder_path = s.audio_path + name+"/"
        clips=[]
        for c in audio_clip_paths:
            print("please")
            if (c!=""):
                clips.append(AudioFileClip(s.audio_path + c + '.wav'))
        #clips = [AudioFileClip(s.audio_path + c + '.wav') for c in audio_clip_paths]
        print("outside loop")
        final_clip = concatenate_audioclips(clips)
        new_path=folder_path+fileName+'.wav'
        final_clip.write_audiofile(new_path)
        print("before say combo")
        self.say_wait_comb(fileName, new_path)


if __name__ == '__main__':
    language = 'Hebrew'
    gender = 'Male'
    s.subjectNum=15
    s.sessionNumber=2
    s.finish_workout=False
    s.general_path=R'C:/Git/poppyCode/greatoded/'
    s.audio_path = s.general_path + 'audioFiles/' + language + '/' + gender + '/'
    tts = TTS()
    # tts.try2()
    # a1 = 'ForBicep'
    # a2='raise right and forward'
    # a3 =""
    # audioList=[a1,a2,a3]
    # tts.combainedAudio(audioList,"NaamaTry3")
    tts.say_wait('15')
    # tts.say_wait('ForIntensive')
    # tts.say_wait('beginExRep')
    # tts.say_wait('6')
    # tts.say_wait('rep')
    # tts.say_wait('acoordingYourTrain')



