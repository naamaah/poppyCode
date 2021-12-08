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
        print("screen start - (Cog5 class)")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(GameFiveStart)
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

class GameFiveStart(tk.Frame):
    def __init__(self, master):
        s.str_to_say = "instruction game 5" #game 5 insturctions
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'instructionGame5.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        image2 = Image.open(s.pic_path+'continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(image=self.photo_image2, command= lambda: self.on_click(master))
        button2.pack()
        button2.place(height=180, width=200, x=100, y=425)

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
        corx = 750
        cory = 120

        color = ["RED","BLUE","BLACK","PINK","GREEN","PURPLE","ORANGE","BROWN","YELLOW"]
        color_dict={"RED":"אדום","BLUE":"כחול","BLACK":"שחור","PINK":"ורוד","GREEN":"ירוק","PURPLE":"סגול"
        ,"ORANGE":"כתום","BROWN":"חום","YELLOW":"צהוב"}
        while len(s.choosen_words) != s.words_number_color:
            word = random.choice(color)
            if word not in s.choosen_words:
                s.choosen_words.append(word)
        x=['1']+['0']*(s.words_number_color-1)
        place=random.sample(x,len(x))
        print(place)
        self.labels = []
        bg_color=[]

        for i in range(s.words_number_color):
            if place[i]=='0':
                bg_color.append(random.choice([ele for ele in color if ele !=s.choosen_words[i] and ele not in bg_color]))
                label = tk.Button(text =color_dict[s.choosen_words[i]], font=("Ariel", 80), fg=bg_color[i],bg="#F3FCFB",command= lambda:self.finishGamePage(False))
                label.pack()
                label.place(height=120, width=220, x=corx, y=cory)
                corx = corx - 300
                if corx < 100:
                    cory = cory + 150
                    corx = 750

                self.labels.append(label)

            else:
                bg_color.append(s.choosen_words[i])
                label = tk.Button(text=color_dict[s.choosen_words[i]], font=("Ariel", 80),fg= s.choosen_words[i],bg="#F3FCFB",command= lambda:self.finishGamePage(True))
                label.pack()
                label.place(height=120, width=220, x=corx, y=cory)
                corx = corx - 300
                if corx < 100:
                    cory = cory + 150
                    corx = 750
                self.labels.append(label)

        i = 0
        #while len(s.words_order) != s.words_number:
        #    number = random.randint(0,s.words_number-1)
        #    if number not in s.words_order:
        #        s.words_order.append(number)
        #        self.after(1500*i+1000, self.changeColor1, number)
        #        i = i + 1
        #print (s.words_order)

        # self.button2 = tk.Button(text = "המשך", font=("Ariel", 40), bg="red", command= lambda: self.on_click(master))
        # self.button2.pack()
        # self.button2.place(height=100, width=150, x=290, y=0)

    def finishGamePage(self, success):
        now=datetime.now()
        if (success):
            s.str_to_say = "correct"
            s.screen.switch_frame(SuccessPage)
            s.words_number_color += 1
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'success']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst=["cognitive mission 5 - success"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            print ("success - (Cog5 class)")
        else:
            s.words_number_color -= 1
            s.str_to_say = "GAME OVER"
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'Failure']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst = ["cognitive mission 5 - Failure"]
            with open(s.general_path+"data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            s.screen.switch_frame(WorngPage)
            print("didn't succeed - (Cog5 class)")

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
            s.words_number_color = 4  # game5
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
        #master.geometry("1024x600")
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

if __name__ == "__main__":
    s.words_number_color = 4
    choosen_words = []
    words_order = []
    s.cogGameCount = 0
    s.finish_workout = False
    language = 'Hebrew'
    gender = 'Male'
    #s.general_path = R'C:/Users/Administrator'
    s.general_path = R'C:/PycharmProjects/greatoded/'
    s.audio_path = s.general_path + 'audio files/' + '/' + language + '/' + gender + '/'
    s.pic_path = s.general_path +'Pictures/'
    #audiopath = s.general_path + '/PycharmProjects/greatoded/audio files'
    #s.audio_path = audiopath + '/' + language + '/' + gender + '/'
    #s.camera = Camera()
    s.screen = Screen()
    language = 'Hebrew'
    gender = 'Male'
    s.tts = TTS()
    s.tts.start()
    app = FullScreenApp(s.screen)
    #s.screen.geometry("1024x600")
    s.screen.mainloop()