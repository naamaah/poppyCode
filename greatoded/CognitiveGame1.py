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
        print("screen start - (Cog1 class)")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(GameOneStart)
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

class GameOneStart(tk.Frame):
    def __init__(self, master):
        s.str_to_say = "game 1 insturctions"
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'instructionGame1.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        image2 = Image.open(s.pic_path+'continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(image=self.photo_image2, command= lambda: self.on_click(master))
        button2.pack()
        button2.place(height=200, width=200, x=400, y=350)


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
        corx = 700
        cory = 100

        words = ["רמז", "מים", "תפוח", "בית", "פרח", "נייר", "מחשב", "בקבוק", "מחשבון", "בקבוק", "עפרון", "קלמר", "צבע", "שפה", "מאמן", "אור", "הופעה", "עיתון", "אינטרנט", "ספר", "ספורט"]
        while len(s.choosen_words) != s.words_number:
            word = random.choice(words)
            if word not in s.choosen_words:
                s.choosen_words.append(word)

        self.labels = []
        for i in range(s.words_number):
            label = tk.Label(text = s.choosen_words[i], font=("Ariel", 80), bg="#F3FCFB")
            label.pack()
            label.place(height=120, width=320, x=corx, y=cory)
            corx = corx - 340
            if corx < 10:
                cory = cory + 150
                corx = 700
            self.labels.append(label)

        i = 0
        while len(s.words_order) != s.words_number:
            number = random.randint(0,s.words_number-1)
            if number not in s.words_order:
                s.words_order.append(number)
                self.after(1500*i+1000, self.changeColor1, number)
                i = i + 1
        print (s.words_order)

        # self.button2 = tk.Button(text = "המשך", font=("Ariel", 40), bg="red", command= lambda: self.on_click(master))
        # self.button2.pack()
        # self.button2.place(height=100, width=150, x=290, y=0)

        image2 = Image.open(s.pic_path+'continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(image=self.photo_image2, command= lambda: self.on_click(master))
        button2.pack()
        button2.place(height=200, width=200, x=400, y=370)

    def changeColor1(self, number):
        self.labels[number].configure(background="yellow")
        self.after(1500, self.changeColor2, number)

    def changeColor2(self, number):
        self.labels[number].configure(bg="#F3FCFB")

    def on_click(self,master):
        self.background_label.destroy()
        s.screen.switch_frame(GamePageTwo)

class GamePageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'background.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(image=self.photo_image)
        self.background_label.pack()
        corx = 700
        cory = 155

        new_words_order = copy.deepcopy(s.choosen_words)
        random.shuffle(new_words_order)

        self.count = 0
        self.labels = []

        for i in range(s.words_number):

            label = tk.Button(text = new_words_order[i], font=("Ariel", 80), bg="#F3FCFB", command =lambda but2=i,button_number= s.choosen_words.index(new_words_order[i]): self.on_click(but2,button_number))
            label.pack()
            label.place(height=120, width=320, x=corx, y=cory)

            corx = corx - 340
            if corx < 10:
                cory = cory + 150
                corx = 700
            self.labels.append(label)

    def changeColor2(self, number):
        self.labels[number].configure(bg="#F3FCFB")
    def changecolor(self,number):
        self.labels[number].configure(bg="Yellow")
    def on_click(self, but2,button_number):
        print (button_number)


        if (s.words_order[self.count] == button_number):
            self.labels[self.count]
            self.after(50,self.changecolor,but2)
            self.count = self.count + 1
            print ("good - (Cog1 class)")
            self.after(850,self.changeColor2,but2)
            s.str_to_say ="correct"
            if (self.count == s.words_number):
                self.labels[but2].configure(bg="Yellow")
                self.finishGamePage(True)
        else:
            self.labels[but2].configure(bg="red")
            self.after(1500, self.changeColor2, but2)
            s.str_to_say = "GAME OVER"
            self.update()
            time.sleep(1.5)
            print ("bad - (Cog1 class)")
            self.finishGamePage(False)

    def finishGamePage(self, success):
        now=datetime.now()
        if (success):
            s.screen.switch_frame(SuccessPage)
            s.words_number += 1
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'success']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst=["cognitive mission 1 - success"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            print ("success - (Cog1 class)")
        else:
            s.words_number -= 1
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'Failure']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst = ["cognitive mission 1 - Failure"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            s.screen.switch_frame(WorngPage)
            print("didn't succeed - (Cog1 class)")

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
            s.words_number = 4  # game1
        else:
            s.screen.switch_frame(GamePageOne)


class WorngPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'worng.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        tk.Label(self, image=self.photo_image).pack()
        self.after(3000, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
            print("SCREENl COG1 FINISHED")
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
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
#???
if __name__ == "__main__":
    #s.general_path = R'C:/Users/Administrator'
    s.general_path = R'C:/PycharmProjects/greatoded/'
    s.words_number = 4
    choosen_words = []
    words_order = []
    s.cogGameCount = 0
    s.finish_workout = False
    s.camera = Camera()
    language = 'Hebrew'
    gender = 'Male'
    #audiopath = s.general_path+'/PycharmProjects/greatoded/audio files'
    #s.audio_path = audiopath +'/' + language + '/' + gender + '/'
    s.audio_path = s.general_path + 'audio files/' + '/' + language + '/' + gender + '/'
    s.pic_path = s.general_path + 'Pictures/'
    s.screen = Screen()
    s.tts = TTS()
    s.tts.start()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()