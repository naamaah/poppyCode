# -*- coding: utf-8 -*-
import tkinter as tk
from PIL import Image, ImageTk
import PIL.Image
import Settings as s
import random
import time
import copy
#from Camera import Camera
from tts import TTS
from datetime import date,datetime
from numpy import savetxt

class Screen(tk.Tk):
    def __init__(self):
        print("screen start - (Cog4 class)")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(GameFourStart)
        self["bg"]="#F3FCFB"

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            if hasattr(self._frame, 'background_label'):
                self._frame.background_label.destroy()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class GameFourStart(tk.Frame):
    def __init__(self, master):
        s.str_to_say = "instruction game 4" #game 4 insturctions
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'instructionGame4.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        image2 = Image.open(s.pic_path+'continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(image=self.photo_image2, command= lambda: self.on_click(master))
        button2.pack()
        button2.place(height=200, width=200, x=200, y=390)

    def on_click(self, master):
        self.background_label.destroy()
        s.screen.switch_frame(GamePageOne)

class GamePageOne(tk.Frame):
    def __init__(self, master):
        s.cogGameCount = s.cogGameCount + 1
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        s.choosen_words = []
        s.words_order = []
        corx = 810 #750
        cory = 90 #120

        #color = ["circle_green","circle_blue","triangle_green","triangle_blue","hexagon_blue","hexagon_green",
         #        "square_blue","square_green","star_green","star_blue"]
        color = ["circle_green", "circle_blue", "circle_orange" ,"triangle_green", "triangle_blue","triangle_orange",
                 "hexagon_blue", "hexagon_green", "hexagon_orange", "square_blue", "square_green", "square_orange",
                 "star_green", "star_blue", "star_orange"]
        while len(s.choosen_words) != s.shape_number:
            word = random.choice(color)
            if word not in s.choosen_words:
                s.choosen_words.append(word)
        print (s.choosen_words)
        s.choosen_words=sorted(s.choosen_words*s.shape_number)
        #s.choosen_words=sorted(s.choosen_words*3)
        s.choosen_words=random.sample(s.choosen_words,len(s.choosen_words))
        print (s.choosen_words)
        while True:
            word = random.choice(color)
            if word not in s.choosen_words:
                s.choosen_words.append(word)
                break
        print(s.choosen_words)
        x=['0']*(s.shape_number**2)
        x.append('1')
        place=random.sample(x,len(x))
        print (x)
        print(place)
        self.labels = []
        index=place.index('1')
        s.choosen_words[index],s.choosen_words[len(x)-1]=s.choosen_words[len(x)-1],s.choosen_words[index]
        for i in range(len(s.choosen_words)):
            if place[i]=='0':
                image2 = Image.open(s.general_path+'shapes/'+s.choosen_words[i]+'.png')
                self.photo_image3 = ImageTk.PhotoImage(image2)
                label = tk.Button(image=self.photo_image3,command= lambda:self.finishGamePage(False))
                label.image=self.photo_image3
                label.pack()
                label.place(height=100, width=180, x=corx, y=cory) #hight=120
                corx = corx - 200
                if corx < 10: #<=
                    cory = cory + 130 #160
                    corx = 810 #750
                self.labels.append(label)
            else:
                image2 = Image.open(s.general_path+'shapes/' + s.choosen_words[i] + '.png')
                self.photo_image2 = ImageTk.PhotoImage(image2)
                label = tk.Button(image=self.photo_image2,command= lambda:self.finishGamePage(True))
                label.pack()
                label.place(height=100, width=180, x=corx, y=cory)#hight=120
                corx = corx - 200
                if corx == -160:
                    cory = cory + 130 #120
                    corx = 810
                self.labels.append(label)
            self.update()
        i = 0

    def finishGamePage(self, success):
        now=datetime.now()
        if (success):
            s.shape_number += 1
            s.str_to_say = "correct"
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'success']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst=["cognitive mission 4 - success"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            print ("success - (Cog4 class)")
        else:
            s.shape_number -= 1
            s.str_to_say = "GAME OVER"
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'Failure']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst = ["cognitive mission 4 - Failure"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            s.screen.switch_frame(WorngPage)
            print("didn't succeed - (Cog4 class)")
            #exit()

class SuccessPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'success.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        self.after(2500, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
        else:
            s.screen.switch_frame(GamePageOne)

class WorngPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'worng.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        self.after(2500, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
            s.shape_number = 2  # game 4
        else:
            s.screen.switch_frame(GamePageOne)

class HelloPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'Hello.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        master.geometry("1024x600")
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

###?????
if __name__ == "__main__":
    s.shape_number = 2 #game 4
    s.cogGameCount = 0
    s.finish_workout = False
    language = 'Hebrew'
    gender = 'Male'
    #s.general_path = R'C:/Users/Administrator'
    s.general_path = R'C:/PycharmProjects/greatoded/'
    #audiopath = s.general_path + '/PycharmProjects/greatoded/audio files'
    #s.audio_path = audiopath + '/' + language + '/' + gender + '/'
    s.audio_path = s.general_path + 'audio files/' + '/' + language + '/' + gender + '/'
    s.pic_path = s.general_path +'Pictures/'
    #s.camera = Camera()
    s.screen = Screen()
    s.tts = TTS()
    s.tts.start()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()