import threading
import Settings as s
import winsound
from pygame import mixer
import pygame
import time


class TTS(threading.Thread):
    def __init__(self):
        #threading.Thread.__init__(self)
        #self.name=name
        #super().__init__()
        print ("tts init  - (tts class)")

    def run(self):
        print("tts start  - (tts class)")
        while (not s.finish_workout):
            if (s.str_to_say!=""):
                print(s.str_to_say)
                self.say_no_wait(s.str_to_say)
                #self.say(s.str_to_say) - not good
                #self.say_Naama(s.str_to_say)
                s.str_to_say = ""
        print ("tts done - (tts class)")

    def say_no_wait(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        #print("say_no_wait function - (tts class) " + str_to_say)
        mixer.init()
        mixer.music.load(s.audio_path+str_to_say+'.wav')
        mixer.music.play()
        #time.sleep(10)


    def say_Naama(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        #option1:
        # filename = s.audio_path+str_to_say+'.wav'
        # wave_obj = sa.WaveObject.from_wave_file(filename)
        # play_obj = wave_obj.play()
        # play_obj.wait_done()  # Wait until sound has finished playing
        #option2:


if __name__ == '__main__':
    language = 'Hebrew'
    gender = 'Female'
    s.finish_workout=False
    s.str_to_say='2'
    #s.general_path = R'C:/PycharmProjects/greatoded/'
    s.general_path=R'C:/Git/poppyCode/greatoded/'
    s.audio_path = s.general_path + 'audioFiles/' + language + '/' + gender + '/'
    #s.audio_path = 'audio files/' + language + '/' + gender + '/'
    tts = TTS()
    tts.start()
    #tts.say_Naama('3')
    time.sleep(3)
    s.finish_workout = True

