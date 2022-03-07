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
import sys


class Screen(tk.Tk):
    def __init__(self):
        print("screen start- (CogMath class)")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(introduction)
        self["bg"] = "#F3FCFB"

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            if hasattr(self._frame, 'background_label'):
                self._frame.background_label.destroy()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class introduction(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.count = 0
        self.first = random.randint(1, 50)
        self.second = random.randint(1, 50)
        s.str_to_say = "math game"
        image1 = Image.open(s.pic_path+'start_page.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.label = tk.Label(image=self.photo_image1)
        self.label.pack()
        image2 = Image.open(s.pic_path+'continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        self.button = tk.Button(image=self.photo_image2, command=lambda: self.onclick(master))
        self.button.pack()
        self.button.place(height=200, width=200, x=400, y=350)

    def onclick(self,master):
        self.label.destroy()
        self.button.destroy()
        s.screen.switch_frame(gamemaths)


class gamemaths(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        s.cogGameCount = s.cogGameCount + 1
        self.math_generate()

    def math_generate(self):
        maths_functions = [self.additions, self.substractions, self.multiplications]
        self.first = random.randint(s.low_addsub, s.high_addsub)
        self.second = random.randint(s.low_addsub, s.high_addsub)
        a=0
        if (self.first<self.second):
            a=self.first
            self.first=self.second
            self.second=a
        print(self.first)
        print(self.second)
        fun_choice = random.choice(maths_functions)
        print(fun_choice)
        fun_choice()


    def additions(self):

        ans_right = self.first + self.second
        answer=[ans_right]
        i=0
        while(i<3):
            ans_wrong= random.randint(1, 100)
            if ans_wrong not in answer:
                answer.append(ans_wrong)
                i+=1
        image1 = Image.open(s.pic_path + 'question_page.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        label = tk.Label(text=str(self.first) + "  +  " + str(self.second)+ " = ? ", font=("Ariel", 80), bg="white")
        label.pack()
        label.place(height=100, width=650, x=170, y=250)
        corx = 150
        cory = 400
        random.shuffle(answer)
        self.button2=[]
        for i in range(len(answer)):
            button = tk.Button(text=str(answer[i]), font=("Ariel", 80), bg="white",
                               command=lambda ans_right=ans_right, i=i, current_number=answer[i]: self.check_respons(ans_right, i,
                                                                                                    current_number))
            button.pack()
            button.place(height=100, width=130, x=corx, y=cory)
            print(corx, cory)
            if corx == 1000:
                corx-=200
                cory+=200
            else:
                corx += 150
            self.button2.append(button)
    def changeColor2(self, number):
        self.button2[number].configure(bg="#F3FCFB")

    def check_respons(self, ans_right, i, current_number):
        if (ans_right == current_number):
            print("success - (CogMath class)")
            print(self.button2)
            self.button2[i].configure(bg="yellow")
            self.after(6000,self.changeColor2,i)
            self.update()
            print("well done - (CogMath class)")
            s.str_to_say = "correct"
            time.sleep(1)
            self.finishGamePage(True)
            # self.success()
        else:
            self.button2[i].configure(bg="red")
            self.after(6000, self.changeColor2, i)
            self.update()
            s.str_to_say = "GAME OVER"
            time.sleep(1)
            self.finishGamePage(False)
            print("failure - (CogMath class)")

    def substractions(self):

        ans_right = self.first - self.second

        print(ans_right)

        answer = [ans_right]
        i=0
        while (i < 3):
            ans_wrong = random.randint(1, 50)
            if ans_wrong not in answer:
                answer.append(ans_wrong)
                i+=1
        image1 = Image.open(s.pic_path + 'question_page.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        label = tk.Label(text=str(self.first) + "  -  " + str(self.second)+" = ? ", font=("Ariel", 80), bg="white")
        label.pack()
        label.place(height=100, width=650, x=170, y=250)
        corx = 150
        cory = 400
        random.shuffle(answer)
        self.button2 = []
        for i in range(len(answer)):

            button = tk.Button(text=str(answer[i]), font=("Ariel", 80), bg="white",
                               command=lambda ans_right=ans_right, i=i, current_number=answer[i]: self.check_respons(ans_right, i,
                                                                                                    current_number))
            button.pack()
            button.place(height=100, width=130, x=corx, y=cory)
            print(corx, cory)
            if corx == 1000:
                corx -= 240
                cory += 200
            else:
                corx += 150
            self.button2.append(button)


    def multiplications(self):
        self.first = random.randint(s.low_mul_first, s.high_mul_first)
        self.second = random.randint(s.low_mul_second, s.high_mul_second)
        ans_right = self.first * self.second
        answer = [ans_right]
        i=0
        while (i < 3):
            ans_wrong = random.randint(1, 30)
            if ans_wrong not in answer:
                answer.append(ans_wrong)
                i+=1
        image1 = Image.open(s.pic_path + 'question_page.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        label = tk.Label(text=str(self.first) + "  X  " + str(self.second)+ " = ? ", font=("Ariel", 80), bg="white")
        label.pack()
        label.place(height=100, width=650, x=170, y=250)
        corx = 150
        cory = 400
        random.shuffle(answer)
        self.button2 = []
        for i in range(len(answer)):

            button = tk.Button(text=str(answer[i]), font=("Ariel", 80), bg="white",
                               command=lambda ans_right=ans_right, i=i, current_number=answer[i]: self.check_respons(ans_right, i,
                                                                                                    current_number))
            button.pack()
            button.place(height=100, width=130, x=corx, y=cory)
            print(corx,cory)
            if corx == 1000:
                corx -= 240
                cory += 200
            else:
                corx += 150
            self.button2.append(button)
    def finishGamePage(self, success):
        now=datetime.now()
        if (success):
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'success']
            with open(s.general_path+"oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst=["cognative mission maths- success"]
            with open(s.general_path + "data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            print ("success - (CogMath class)")
        else:
            s.screen.switch_frame(SuccessPage)
            dt_t = str(date.today())
            td_t = str(now.strftime("%H:%M:%S"))
            mylist = [dt_t, td_t, 'Failure']
            with open(s.general_path + "oded_gr8_cog.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylist, fmt='%s')
            mylst = ["cognative mission maths- Failure"]
            with open(s.general_path + "data_shik.csv", "ab") as f:
                f.write(b"\t")
                savetxt(f, mylst, fmt='%s')
            s.screen.switch_frame(WorngPage)
            print("didn't succeed - (CogMath class)")
        #s.cogGame = False

class SuccessPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path + 'success.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        self.after(3000, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
        else:
            s.screen.switch_frame(gamemaths)

class WorngPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path + 'worng.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        self.after(3000, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
            s.low_addsub = 10  # level 1:1 level2:10 level3:10
            s.high_addsub = 50  # level 1:50 level2:50 level3:100
            s.low_mul_first = 1  # level 1:1 level2:1 level3:1
            s.high_mul_first = 5  # level 1:5 level2:5 level3:9
            s.low_mul_second = 10  # level 1:2 level2:10 level3:10
            s.high_mul_second = 50  # level 1:6 level2:50 level3:50
        else:
            s.screen.switch_frame(gamemaths)

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)
        master.geometry("1024x600")
    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

# understand the code
if __name__ == "__main__":
    #s.general_path = R'C:/Users/Administrator'
    s.general_path = R'C:/PycharmProjects/greatoded/'
    s.low_addsub = 1
    s.high_addsub = 50
    s.low_mul_first = 1
    s.high_mul_first = 5
    s.low_mul_second = 2
    s.high_mul_second = 6
    s.count=0
    s.cogGameCount = 0
    s.finish_workout = False
    #s.camera = Camera()
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
