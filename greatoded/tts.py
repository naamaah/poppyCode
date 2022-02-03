import threading
import Settings as s
import winsound
from pygame import mixer
import time
import sys
#for say_Naama
from playsound import playsound

class TTS(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name=name
        #super().__init__()
        print ("tts init  - (tts class)")

    def run(self):
        while (not s.finish_workout):
            if (s.str_to_say!=""):
                self.say_no_wait(s.str_to_say)
                #self.say(s.str_to_say)
                #self.say_Naama(s.str_to_say)
                s.str_to_say = ""
        print ("tts done - (tts class)")
        #sys.exit()

    def say_no_wait(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        mixer.init()
        mixer.music.load(s.audio_path+str_to_say+'.wav')
        mixer.music.play()
        #time.sleep(10)
        print ("say_no_wait function - (tts class) "+str_to_say)


    def say_Naama(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        print("say_Naama function - (tts class) " + str_to_say)
        playsound(s.audio_path + str_to_say + '.wav')


if __name__ == '__main__':
    language = 'Hebrew'
    gender = 'Female'
    s.general_path = R'C:/PycharmProjects/greatoded/'
    s.audio_path = s.general_path + 'audio files/' + '/' + language + '/' + gender + '/'
    #s.audio_path = 'audio files/' + language + '/' + gender + '/'
    tts = TTS("tts")
    tts.start()
    tts.say('2')
    tts.join()
    print("yotam")
