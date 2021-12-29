# -*- coding: utf-8 -*-
import tkinter as tk
from PIL import Image, ImageTk
import PIL.Image
import Settings as s
import random
import time
import copy
from Camera import Camera
from tts import TTS
from datetime import date,datetime
from numpy import savetxt

class Screen(tk.Tk):
    def __init__(self):
        print("screen start - (Cog2 class)")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(GameTwoStart)
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

class GameTwoStart(tk.Frame):
    def __init__(self, master):
        #TODO - RECORD GAME 2 INSTURCTIONS
        s.str_to_say = "game 2 instructions" #game 2 insturctions
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'instructionGame2.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        image2 = Image.open(s.pic_path+'continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        #button2 = tk.Button(self.background_label, image=self.photo_image2, command= lambda: self.on_click(master))
        button2 = tk.Button(image=self.photo_image2, command=lambda: self.on_click(master))
        button2.pack()
        button2.place(height=200, width=200, x=400, y=400)

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

        self.labels=[]
        square_length=4
        corx = 620
        cory = 120

        for i in range(square_length*square_length):
            label = tk.Label(font=("Ariel", 90), bg="gray")
            label.pack()
            label.place(height=80, width=80, x=corx, y=cory)
            corx = corx - 100
            if corx <= 260:
                cory = cory + 100
                corx = 620
            self.labels.append(label)

        global light_tiles
        light_tiles=[]
        while len(light_tiles) != s.light_tiles_num:
            number = random.randint(0,square_length*square_length-1)
            if number not in light_tiles:
                light_tiles.append(number)
                self.after(500, self.changeColor1, number)
        print (light_tiles)

        self.after(4000,lambda: self.on_click(master))

    def changeColor1(self, number):
        self.labels[number].configure(background="blue")

    def on_click(self, master):
        self.background_label.destroy()
        s.screen.switch_frame(Game2PageTwo)

class Game2PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'background.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(image=self.photo_image)
        self.background_label.pack()

        self.buttons=[]
        square_length=4
        corx = 620
        cory = 120

        for i in range(square_length*square_length):
            button = tk.Button(self.background_label, bg="gray", command = lambda button_number = i: self.on_click(button_number))
            button.pack()
            button.place(height=80, width=80, x=corx, y=cory)
            corx = corx - 100
            if corx <= 260:
                cory = cory + 100
                corx = 620
            self.buttons.append(button)

        self.count = 0 # to count the number of tries, we will limit to 10
        self.count_successes = 0

    def on_click(self,i):
        if (i in light_tiles):
            self.buttons[i].configure(background="blue")
            self.count_successes = self.count_successes+1
            s.str_to_say = "correct"
        else:
            self.buttons[i].configure(text="X", fg="red",font=("Courier", 44))
        self.count = self.count + 1
        if (self.count_successes == s.light_tiles_num):
            self.finishGamePage(True)
        if (self.count==10):
            self.finishGamePage(False)

    def finishGamePage(self, success):
        now=datetime.now()
        if (success):
            s.light_tiles_num += 1
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'success']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst=["cognitive mission 2 - success"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            print ("success - (Cog2 class)")
        else:
            s.light_tiles_num -= 1
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'Failure']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst = ["cognitive mission 2 - Failure"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            s.screen.switch_frame(WorngPage)
            print("didn't succeed - (Cog2 class)")
        # time.sleep(5)
class SuccessPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'success.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        self.after(3000, self.last)

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
        self.after(3000, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
            s.light_tiles_num = 7  # game2
        else:
            s.screen.switch_frame(GamePageOne)


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

###??
if __name__ == "__main__":
    s.light_tiles_num = 6
    choosen_words = []
    words_order = []
    s.cogGameCount = 0
    s.finish_workout = False
    #s.camera = Camera()
    language = 'Hebrew'
    gender = 'Male'
    #audiopath = R'C:\Users\Administrator\PycharmProjects\greatoded\audio files'
    #s.audio_path = audiopath + '/' + language + '/' + gender + '/'
    s.general_path = R'C:/PycharmProjects/greatoded/'
    s.audio_path = s.general_path + 'audio files/' + '/' + language + '/' + gender + '/'
    s.pic_path = s.general_path + 'Pictures/'
    s.screen = Screen()
    s.tts = TTS()
    s.tts.start()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()