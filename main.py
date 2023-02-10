import os
import json
import threading
from tkinter import *
from tkinter import ttk
from pygame import mixer
from tkinter import filedialog
from PIL import Image,ImageTk

os.system("clear")


class main:

    def __init__(self,window):
        self.window = window
        self.WIDTH = 600
        self.HEIGHT = 400
        self.PAUSE_PLAY = False
        self.THEAM = "Night"
        self.PATH = ""
        self.THEAM_COLOR = {
            'Night':{
                'bg':'#353535',
                'fg':'white',
                'f_bg':'#252525',
                'f_fg':'white'
            },
            'Dracula':{
                'bg':"#363447",
                'fg':"white",
                'f_bg':"#22202c",
                'f_fg':'white'
            },
            'Abyss':{
                'bg':"#181b38",
                'fg':"#6589b9",
                'f_bg':"#0b0022",
                'f_fg':"white"
            },
            'Light':{
                'bg':'#fcf9e2',
                'fg':'black',
                'f_bg':'#d0ceb7',
                'f_fg':'black'
            }
        }
        self.gui_obj = {}
        self.data_obj = {}
        self.img_obj = {}

        try:
            with open("details.json",'r') as file:
                data = json.load(file)
            self.PATH = data['PATH']
            self.THEAM = data['THEAM']
        except:
            self.Write_Json()
        
        mixer.init()
        window.geometry(f"{self.WIDTH}x{self.HEIGHT}+200+200")
        window.title("Music Player... ( Created By NightDevilPT )")
        self.GUI_Making(window=window,obj=self.gui_obj)

        def Delete_Window():
            try:
                mixer.music.stop()
            except:
                pass
            window.destroy()
        
        window.protocol("WM_DELETE_WINDOW",lambda:Delete_Window())


    #####========= [ Write JSON File Start ] ========#####
    def Write_Json(self):
        data = {
            'PATH':self.PATH,
            'THEAM':self.THEAM
        }
        data = json.dumps(data)
        with open("details.json","w") as file:
            file.write(data)
    #####========= [ Write JSON File End ] ========#####

    #####========= [ Delete Widgets Function Start ] ========#####
    def Delete_Widgets(self,obj={}):
        for i in obj:
            try:
                obj[i].destroy()
            except:
                pass
        obj.clear()
    #####========= [ Delete Widgets Function End ] ========#####

    #####========= [ Apply Theams Function Start ] ========#####
    def Apply_Theam(self,obj={}):
        BG = self.THEAM_COLOR[self.THEAM]['bg']
        FG = self.THEAM_COLOR[self.THEAM]['fg']
        F_BG = self.THEAM_COLOR[self.THEAM]['f_bg']
        F_FG = self.THEAM_COLOR[self.THEAM]['f_fg']

        self.window.config(bg=BG)

        obj['frame.1'].config(bg=F_BG)
        obj['logo'].config(bg=F_BG)
        obj['song_name'].config(bg=F_BG,fg=F_FG)
        obj['song_end'].config(bg=F_BG,fg=F_FG)
        obj['song_start'].config(bg=F_BG,fg=F_FG)
        
        obj['song_next'].config(bg=F_BG,activebackground=F_BG,highlightbackground=F_BG,highlightcolor=F_BG)
        obj['song_play_pause'].config(bg=F_BG,activebackground=F_BG,highlightbackground=F_BG,highlightcolor=F_BG)
        obj['song_previous'].config(bg=F_BG,activebackground=F_BG,highlightbackground=F_BG,highlightcolor=F_BG)
        obj['song_volume'].config(bg=BG)
        obj['theam'].config(fg=F_FG,activeforeground=F_FG,bg=F_BG,activebackground=F_BG,highlightbackground=F_BG,highlightcolor=F_BG)
        
        obj['song_list'].config(bg=F_BG,fg=F_FG,highlightbackground=F_BG,highlightcolor=F_BG,relief=FLAT,font=("arial",12,"bold"))
        obj['h_scroll'].config(bg="grey",activebackground="grey",troughcolor=F_BG)
        obj['v_scroll'].config(bg="grey",activebackground="grey",troughcolor=F_BG)

        obj['sound_track'].config(background=BG,activebackground=BG,troughcolor=F_BG,highlightbackground=BG,highlightcolor=BG)

    #####========= [ Apply Theams Function End ] ========#####

    #####========= [ Set Theam Name Function Start ] ========#####
    def Change_Theam(self):
        try:
            self.top.destroy()
        except:
            pass
        
        BG = self.THEAM_COLOR[self.THEAM]['bg']
        FG = self.THEAM_COLOR[self.THEAM]['fg']

        self.top = Toplevel()
        self.top.geometry("300x50+300+300")
        self.top.title("Select Theam...")
        self.top.config(bg=BG)

        label = Label(self.top,text="Select Theam :",bg=BG,fg=FG,font=("arial",12,"bold"))
        label.pack(side=LEFT,fill=BOTH,padx=5)

        def select_theam():
            self.THEAM = show.get()
            self.Write_Json()
            self.top.destroy()
            self.Apply_Theam(obj=self.gui_obj)

        theams = ['','Night','Light','Dracula','Abyss']
        show = StringVar()
        show.set(self.THEAM)
        option = ttk.OptionMenu(self.top,show,*theams,command=lambda event=None:select_theam())
        option.place(x=130,y=10,width=150)

        self.top.mainloop()
    #####========= [ Set Theam Name Function End ] ========#####

    #####========= [ Song Folder Function Start ] ========#####
    def Open_Songs_Folder(self):
        self.PATH = filedialog.askdirectory(title="Select Folder")+"/"
        self.Write_Json()

        self.songs = []
        for i in os.listdir(self.PATH):
            if i.endswith(".mp3"):
                self.songs.append(i[0:-4])
        
        self.playlist = StringVar(value=self.songs)
        self.gui_obj['song_list']['listvariable'] = self.playlist
    #####========= [ Song Folder Function End ] ========#####
                
    #####========= [ Rotating Image Function Start ] ========#####
    def Rotate_Image(self,label=None,angle=0):
        if self.PAUSE_PLAY==True:
            img2 = self.img_obj['music'].rotate(angle)
            img3 = ImageTk.PhotoImage(img2)

            label.config(image=img3)
            label.image = img3

            self.angle = int(angle-2)%360
            
            if self.PAUSE_PLAY:
                position = mixer.music.get_pos()
                self.gui_obj['song_progress']['value'] = int(position)/1000
            
            if int(self.detail) == int(position/1000):
                print(None)
                try:
                    name = self.gui_obj['song_list'].get(ACTIVE)
                    ind = self.songs.index(name)
                    if ind == len(self.songs)-1:
                        ind = -1
                    self.gui_obj['song_list'].activate(ind+1)
                    self.song = self.gui_obj['song_list'].get(ind+1)
                except:
                    pass

                self.Put_Value()
                self.Play_Pause_Function(True)

        label.after(100,lambda:threading.Thread(target=self.Rotate_Image,args=(label,self.angle)).start())
    #####========= [ Rotating Image Function End ] ========#####

    #####========= [ Showing Song Details Function Start ] ========#####
    def Put_Value(self,cond=None):

        self.detail = mixer.Sound(f"{self.PATH}{self.song}.mp3").get_length()

        self.gui_obj['song_progress']['maximum'] = self.detail
        self.data_obj['song_name'].set(self.song)

        if self.detail>60 and self.detail<3600:
            minute = int(self.detail//60)
            second = int(self.detail%60)
            if minute<10:
                minute = "0"+str(minute)
            if second<10:
                second = "0"+str(second)
        
            time = f"{minute}:{second}"
        elif self.detail>=3600:
            hour = int((self.detail//60)//60)
            minute = int((self.detail//60)%60)
            second = int(self.detail%60)
            if minute<10:
                minute = "0"+str(minute)
            if second<10:
                second = "0"+str(second)
            if hour<10:
                hour = "0"+str(hour)
            time = f"{hour}:{minute}:{second}"
        elif self.detail<60:
            time = f"00:{int(self.detail)}"
        
        self.data_obj['song_end'].set(time)
    #####========= [ Showing Song Details Function Start ] ========#####

    #####========= [ Play / Pause Song Function Start ] ========#####
    def Play_Pause_Function(self,cond=False):
        volume = self.gui_obj['sound_track'].get()/100
        mixer.music.set_volume(volume)

        if len(self.songs)==0:
            return
        
        if cond:
            self.PAUSE_PLAY=True
            self.angle = 0
            mixer.music.load(f"{self.PATH}{self.song}.mp3")
            self.gui_obj['song_play_pause'].config(image=self.img_obj['pause'])
            self.gui_obj['song_play_pause'].image=self.img_obj['pause']
            mixer.music.play()
            return

        if self.PAUSE_PLAY:
            self.PAUSE_PLAY=False
            self.gui_obj['song_play_pause'].config(image=self.img_obj['play'])
            self.gui_obj['song_play_pause'].image=self.img_obj['play']
            mixer.music.pause()
        else:
            self.PAUSE_PLAY=True
            self.gui_obj['song_play_pause'].config(image=self.img_obj['pause'])
            self.gui_obj['song_play_pause'].image=self.img_obj['pause']
            
            if self.gui_obj['song_progress']['value'] == 0:
                self.song = self.gui_obj['song_list'].get(ACTIVE)
                self.Put_Value()
                mixer.music.load(f"{self.PATH}{self.song}.mp3")
                mixer.music.play()
            else:
                mixer.music.unpause()
    #####========= [ Play / Pause Song Function End ] ========#####

    #####========= [ Music Player GUI Function Start ] ========#####
    def GUI_Making(self,window=None,obj={}):
        self.Delete_Widgets(obj=obj)
        self.style = ttk.Style()
        
        BG = self.THEAM_COLOR[self.THEAM]['bg']
        FG = self.THEAM_COLOR[self.THEAM]['fg']
        F_BG = self.THEAM_COLOR[self.THEAM]['f_bg']
        F_BG = self.THEAM_COLOR[self.THEAM]['f_bg']

        window.config(bg=BG)

        #####======= Music Buttons Frame
        obj['frame.1'] = Frame(window,bg=F_BG)
        obj['frame.1'].place(x=10,y=10,width=240,height=380)

        img1 = Image.open("icons/music.png")
        self.img_obj['music'] = img1.resize((175,175),Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(self.img_obj['music'])

        obj['logo'] = Label(obj['frame.1'],image=img3,compound=CENTER,anchor=CENTER)
        obj['logo'].image = img3
        obj['logo'].place(x=30,y=20,width=180,height=180)
        self.angle = 0
        obj['logo'].after(100,lambda:self.Rotate_Image(label=obj['logo'],angle=self.angle))
        
        #####======= Song Name Label
        self.data_obj['song_name'] = StringVar()
        self.data_obj['song_name'].set("None")

        obj['song_name'] = Label(obj['frame.1'],textvariable=self.data_obj['song_name'],font=("arial",12,"bold"))
        obj['song_name'].place(x=5,y=210,width=230)

        #####======= Song Progress Bar Label
        self.style.configure("Horizontal.TProgressbar",background="#009025",troughcolor=BG)

        obj['song_progress'] = ttk.Progressbar(obj['frame.1'],value=0,orient=HORIZONTAL)
        obj['song_progress'].place(x=20,y=240,width=200,height=8)

        #####======= Song Start Label
        obj['song_start'] = Label(obj['frame.1'],text="00:00",font=("arial",10,"bold"))
        obj['song_start'].place(x=5,y=250)

        #####======= Song End Label
        self.data_obj['song_end'] = StringVar()
        self.data_obj['song_end'].set("00:00")

        obj['song_end'] = Label(obj['frame.1'],textvariable=self.data_obj['song_end'],font=("arial",10,"bold"),anchor=E)
        obj['song_end'].place(x=175,y=250,width=60)

        #####======= Song Play / Pause Button
        img1 = Image.open("icons/play.png")
        img2 = img1.resize((65,65),Image.ANTIALIAS)
        self.img_obj['play'] = ImageTk.PhotoImage(img2)

        img1 = Image.open("icons/pause.png")
        img2 = img1.resize((65,65),Image.ANTIALIAS)
        self.img_obj['pause'] = ImageTk.PhotoImage(img2)

        obj['song_play_pause'] = Button(obj['frame.1'],image=self.img_obj['play'],compound=CENTER,relief=FLAT,bd=0)
        obj['song_play_pause'].image = self.img_obj['play']
        obj['song_play_pause'].config(command=lambda:self.Play_Pause_Function())
        obj['song_play_pause'].place(x=240/2-35,y=300,width=70,height=70)

        #####======= Song Previous Button
        img1 = Image.open("icons/previous.png")
        img2 = img1.resize((45,45),Image.ANTIALIAS)
        self.img_obj['previous'] = ImageTk.PhotoImage(img2)

        def Set_Previous_Song():
            try:
                name = self.gui_obj['song_list'].get(ACTIVE)
                ind = self.songs.index(name)
                if ind-1 < 0:
                    ind = len(self.songs)
                self.gui_obj['song_list'].activate(ind-1)
                self.song = self.gui_obj['song_list'].get(ind-1)
            except:
                pass

            self.Put_Value()
            self.Play_Pause_Function(True)

        obj['song_previous'] = Button(obj['frame.1'],image=self.img_obj['previous'],compound=CENTER,relief=FLAT,bd=0)
        obj['song_previous'].image = self.img_obj['previous']
        obj['song_previous'].config(command=lambda:Set_Previous_Song())
        obj['song_previous'].place(x=20,y=310,width=50,height=50)

        #####======= Song Next Button
        img1 = Image.open("icons/next.png")
        img2 = img1.resize((45,45),Image.ANTIALIAS)
        self.img_obj['next'] = ImageTk.PhotoImage(img2)

        def Set_Next_Song():
            try:
                name = self.gui_obj['song_list'].get(ACTIVE)
                ind = self.songs.index(name)
                if ind == len(self.songs)-1:
                    ind = -1
                self.gui_obj['song_list'].activate(ind+1)
                self.song = self.gui_obj['song_list'].get(ind+1)
            except:
                pass

            self.Put_Value()
            self.Play_Pause_Function(True)

        obj['song_next'] = Button(obj['frame.1'],image=self.img_obj['next'],compound=CENTER,relief=FLAT,bd=0)
        obj['song_next'].image = self.img_obj['next']
        obj['song_next'].config(command=lambda:Set_Next_Song())
        obj['song_next'].place(x=170,y=310,width=50,height=50)

        #####======= Song Folder Button
        obj['song_folder'] = Button(window,text="Select Folder...",font=("arial",12,"bold"),bg="#009025",fg="white",activebackground="#009025",activeforeground="white",highlightbackground="#009025",highlightcolor="#009025",relief=FLAT,bd=0)
        obj['song_folder'].place(x=260,y=20,width=120,height=25)
        obj['song_folder'].config(command=self.Open_Songs_Folder)

        #####======= Song Folder Button
        obj['theam'] = Button(window,text="Theam Change",font=("arial",12,"bold"),relief=FLAT,bd=0)
        obj['theam'].place(x=self.WIDTH-170,y=20,width=150,height=25)
        obj['theam'].config(command=self.Change_Theam)

        def Select_Song(cond=False):
            os.system("clear")
            if cond:
                try:
                    self.song = self.gui_obj['song_list'].get(self.gui_obj['song_list'].curselection()[0])
                except:
                    self.song = self.gui_obj['song_list'].get(ACTIVE)
                self.Put_Value()
                self.Play_Pause_Function(True)

        #####======= Songs List ListBox
        obj['song_list'] = Listbox(window)
        obj['song_list'].bind("<Double-Button>",lambda event=None:Select_Song(cond=True))
        obj['song_list'].place(x=260,y=50,width=310,height=260)

        #####======= Horizontal ScrollBar
        obj['h_scroll'] = Scrollbar(window,orient=HORIZONTAL)
        obj['h_scroll'].place(x=260,y=312,width=310,height=12)
        obj['h_scroll'].config(command=obj['song_list'].xview)
        
        #####======= Vertical ScrollBar
        obj['v_scroll'] = Scrollbar(window,orient=VERTICAL)
        obj['v_scroll'].place(x=572,y=50,width=12,height=260)
        obj['v_scroll'].config(command=obj['song_list'].yview)

        self.songs = []
        try:
            for i in os.listdir(self.PATH):
                if i.endswith(".mp3"):
                    self.songs.append(i[0:-4])
        except:
            pass
        
        self.playlist = StringVar(value=self.songs)
        obj['song_list'].config(xscrollcommand=obj['h_scroll'].set,yscrollcommand=obj['v_scroll'].set,listvariable=self.playlist)

        #####======= Song Sound Button
        img1 = Image.open("icons/volume.png")
        img2 = img1.resize((45,45),Image.ANTIALIAS)
        self.img_obj['volume'] = ImageTk.PhotoImage(img2)

        obj['song_volume'] = Label(window,image=self.img_obj['volume'])
        obj['song_volume'].image=self.img_obj['volume']
        obj['song_volume'].place(x=260,y=340,width=50,height=50)

        def set_volume(event):
            vol = obj['sound_track'].get()/100
            mixer.music.set_volume(vol)

        self.style.configure("Horizontal.TScale",background=BG,activebackground=BG,troughcolor=F_BG,relief=FLAT,bd=0)

        obj['sound_track'] = Scale(window,orient=HORIZONTAL,showvalue=0,from_=0,to=100,bd=1,sliderrelief=GROOVE)
        obj['sound_track'].config(relief=FLAT,command=lambda event:set_volume(event))
        obj['sound_track'].set(50)
        obj['sound_track'].place(x=320,y=355,width=250)

        self.Apply_Theam(obj=obj)
    #####========= [ Music Player GUI Function End ] ========#####


window = Tk()
main(window)

window.mainloop()