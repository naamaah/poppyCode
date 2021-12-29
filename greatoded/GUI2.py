# -*- coding: utf-8 -*-
import time
import tkinter as tk
from PIL import Image, ImageTk
import Settings as s
import random
from datetime import date,datetime
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt
class Screen(tk.Tk):
    def __init__(self):
        print("screen start - (GUI class)")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(HelloPage)
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

    def quit(self):
        print("screen done")
        self.destroy()

class HelloPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'Hello.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()

class ExercisePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'exercise.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()

class Relax_Page_ber(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'bend_elbows_relax.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()
class relax_thr(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'turn_head_right.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()
class relax_thl(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'turn_head_left.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class relax_thd(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'turn_head_down.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class teeth(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'teeth.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class eyes(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'eyes.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class eyebrows(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'eyebrows.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class smile(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'smile.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
"""
class feedback_relax(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'feedback_relax.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
"""
class begin_page(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        if(s.female==False):
            image1 = Image.open(s.pic_path+'begin_page.jpg')
        else:
            image1 = Image.open(s.pic_path+'begin_page_female.png')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'physicaltraining.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)

        button2= tk.Button(image=self.photo_image2, command=self.on_click_right)
        button2["border"] = 0
        button2.pack()
        button2.place(height=310, width=300, x=663, y=180)

        image3 = Image.open(s.pic_path+'relax.jpg')
        self.photo_image3 = ImageTk.PhotoImage(image3)
        button2= tk.Button(image=self.photo_image3, command=self.on_click_left)
        button2["border"] = 0
        button2.pack()
        button2.place(height=310, width=300, x=62, y=180)


    def on_click_right(self):
        print("image clicked - (GUI class)")
        s.relax = False
        mylist = ['physical training']
        excel_path = s.general_path+'data_shik.csv'
        with open(excel_path, "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
        s.screen.switch_frame(BlankPage)

    def on_click_left(self):
        print("image clicked - (GUI class)")
        s.relax=True
        now = datetime.now()
        dt_t = str(date.today())
        td_t = str(now.strftime("%H:%M:%S"))
        mylist = [dt_t,td_t,'Relaxation mode']
        excel_path = s.general_path+'data_shik.csv'
        with open(excel_path, "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
        s.screen.switch_frame(BlankPage)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'Start.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'StartButton.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2 ,command=self.on_click)
        button2["border"]=0
        button2.pack()
        button2.place(height=480, width=480, x=265, y=100)

    def on_click(self):
        print("image clicked - (GUI class)")
        s.waved = True

class weightPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'Normal-or-weights.png')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'without-weights.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2 ,command=self.on_click_without)
        button2["border"]=0
        button2.pack()
        button2.place(height=330, width=395, x=555, y=160)

        image3 = Image.open(s.pic_path+'with-weights.png')
        self.photo_image3 = ImageTk.PhotoImage(image3)
        button3 = tk.Button(image=self.photo_image3, command=self.on_click_with)
        button3["border"] = 0
        button3.pack()
        button3.place(height=330, width=395, x=65, y=160)

    def on_click_without(self):
        print("image clicked - (GUI class)")
        s.pickWeights = True

    def on_click_with(self):
        self.background_label.destroy()
        s.str_to_say = "which weight"
        s.screen.switch_frame(weight_check)

class weight_check(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'which-weights.png')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'0.5.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(image=self.photo_image2, command=self.on_click_without)
        button2["border"] = 0
        button2.pack()
        button2.place(height=330, width=395, x=555, y=200)

        image3 = Image.open(s.pic_path+'1-KG.png')
        self.photo_image3 = ImageTk.PhotoImage(image3)
        button2 = tk.Button(image=self.photo_image3, command=self.on_click_with)
        button2["border"] = 0
        button2.pack()
        button2.place(height=330, width=395, x=65, y=200)

    def on_click_without(self):
        mylist = ['The weight is 0.5 KG']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
        print("image clicked - (GUI class)")
        s.pickWeights = True

    def on_click_with(self):
        mylist = ['The weight is 1KG']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
        print("image clicked - (GUI class)")
        s.pickWeights = True

class StartPage_Relax(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'relax_intrc.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'relax_next.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2 ,command=self.on_click)
        button2["border"]=0
        button2.pack()
        button2.place(height=230, width=340, x=350, y=340)

    def on_click(self):
        print("image clicked - (GUI class)")
        s.clickrelax = True
class facemovement_Relax(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'move_to_face.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'relax_next.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2 ,command=self.on_click)
        button2["border"]=0
        button2.pack()
        button2.place(height=230, width=340, x=350, y=332)

    def on_click(self):
        print("image clicked - (GUI class)")
        s.facemove = True
class TryAgainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'tryagain.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'tryagainright2.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2, command=self.on_click_right)
        button2["border"] = 0
        button2.pack()
        button2.place(height=395, width=395, x=555, y=125)

        image3 = Image.open(s.general_path+'tryagainleft2.jpg')
        self.photo_image3 = ImageTk.PhotoImage(image3)
        button2= tk.Button(image=self.photo_image3, command=self.on_click_left)
        button2["border"] = 0
        button2.pack()
        button2.place(height=395, width=395, x=65, y=125)


    def on_click_right(self):
        print("image clicked - (GUI class)")
        s.waved = True
        mylist = ['repeated', '1']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
        s.screen.switch_frame(BlankPage)

    def on_click_left(self):
        print("image clicked - (GUI class)")
        s.clickedTryAgain=True
        s.screen.switch_frame(BlankPage)


class BlankPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'Background.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class VeryGoodPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'verygood.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        mylist = ['success', '100']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
class Winnergreat(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'Winnergreat.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        mylist = ['success', '100']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
class robotverygood(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'robotverygood.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        mylist = ['success', '100']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
class ExcellentPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'excellent.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        mylist = ['success', '100']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
class WellDonePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'welldone.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        mylist = ['success', '100']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
class feedback_elbow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'feedback_elbow.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
class feedback_head(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'feedback_head.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
class feedback_relax(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'feedback_relax.jpg')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class GoodbyePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'Goodbye.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
class shutdown_win(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'shutdown_message.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        time.sleep(2)
        #self.quit()
class OnePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open(s.pic_path+'1.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
class lastquestion_relax(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'tryagain.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'ptafterrelax.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2, command=self.on_click_right)
        button2.pack()
        button2["border"]=0
        button2.place(height=395, width=395, x=555, y=125)

        image3 = Image.open(s.pic_path+'finish_relax.jpg')
        self.photo_image3 = ImageTk.PhotoImage(image3)
        button2= tk.Button(image=self.photo_image3, command=self.on_click_left)
        button2["border"] = 0
        button2.pack()
        button2.place(height=395, width=395, x=65, y=125)

    def on_click_right(self):
        print("image clicked - (GUI class)")
        mylist = ['physical training after relaxation']
        with open(s.general_path+"data_shik.csv", "ab") as f:
            f.write(b"\n")
            savetxt(f, mylist, fmt='%s')
        s.relax = True

    def on_click_left(self):
        print("image clicked - (GUI class)")
        s.relax=False

class lastquestion(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open(s.pic_path+'tryagain.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open(s.pic_path+'Yes.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2, command=self.on_click_right)
        button2.pack()
        button2["border"]=0
        button2.place(height=400, width=400, x=555, y=125)

        image3 = Image.open(s.pic_path+'No.jpg')
        self.photo_image3 = ImageTk.PhotoImage(image3)
        button2= tk.Button(image=self.photo_image3, command=self.on_click_left)
        button2["border"] = 0
        button2.pack()
        button2.place(height=400, width=400, x=65, y=125)

    def on_click_right(self):
        print("image clicked- (GUI class)")
        s.repeat_again = True
        s.screen.switch_frame(begin_page)

    def on_click_left(self):
        print("image clicked- (GUI class)")
        s.repeat_again=False
        s.screen.switch_frame(GoodbyePage)

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

if __name__ == "__main__":
    #general_path = R'C:\Users\TEMP.NAAMA\Downloads\greatoded'
    s.general_path=R'C:/PycharmProjects/greatoded/'
    s.pic_path = s.general_path +'Pictures/'
    s.screen = Screen()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()

    s.screen.quit()
