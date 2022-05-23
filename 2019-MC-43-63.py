from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from math import isclose
import time
import os

from pose import PoseDetector
import cv2 
import mediapipe as mp

def slope(a,b):
    return (b[1]-a[1])/(b[0]-a[0])
def startscreen():
    global st
    d=(os.getcwd())
    st=Tk()
    st.geometry("500x500+500+100")
    st.title("Welcome to PlankApp")
    sbg= ImageTk.PhotoImage(file=f"{d}\\p.png")
    slabel=Label(st, bg='white',image=sbg)
    slabel.place(x=0,y=0)
    Bs=Button(st,width=10,height=2,text="Start",padx=10,font=('Helvatical bold',20),fg="white",bg="royal blue",command=start)
    Bs.place(x=170,y=400)
    st.mainloop()

def checkSlope(a,b,c,d,e):
    w1=w2=w3=""
    s1=True
    try:
        if (isclose(slope(a,b),slope(b,c),abs_tol=0.4)== False):
            w1="Straighten Head"
            s1=False
        if (isclose(slope(b,c),slope(c,d),abs_tol=0.2)== False):
            w2="Straighten Back"
            s1=False    
        if (isclose(slope(c,d),slope(d,e),abs_tol=0.2)== False):
            w3="Straighten legs"
            s1=False
        if (s1):
            w1="Fine"
            return w1
        return f"{w1}\n{w2}\n{w3}"
    except:
        pass
def start():
    global st
    st.destroy()
def box():
    global bbox
    if bbox==True:
        bbox=False
        B1.config(bg="orange")
    else:
        bbox=True
        B1.config(bg="green")

def search():
    global f,label1,cap,seconds,minutes
    nf=0
    nf=filedialog.askopenfilename(title="Select MP4 FILE",filetypes=(("mp4","*.mp4"),("all files","*.*")))
    if nf:
        minutes=0
        seconds=0
        destroyl()
        messagebox.showinfo(title="Press ok",message="This will start new video")
        B3.config(state="normal")
        B4.config(state="normal")
        B5.config(state="disabled")
        
        
        f=nf
        
        initilize(f)
def retime():
    global tseconds,tminutes
    tminutes=tseconds=0
def again():
    global minutes,seconds
    minutes=0
    seconds=0
    destroyl()
    messagebox.showinfo(title="Press ok",message="This will restart the video")
    initilize(f)   
    
def destroyl():
    global f,label1,cap,d
    b= ImageTk.PhotoImage(file=f"{d}\\loadn.png")
    
    cap.release()
    
    cv2.destroyAllWindows()
    
    label1.config(image=b)
    label1.image=b
   
def live():
    global f,minutes,seconds
    minutes=0
    seconds=0

    destroyl()
    messagebox.showinfo(title="Press ok",message="This will open the camera")
    f=0
    B3.config(state="disabled")
    B4.config(state="disabled")
    B5.config(state="normal")

    initilize(f)  
def select_img() :
    global f,cTime,pTime,minutes,seconds,tminutes,tseconds,bbox,cap,label1,bbox,l1,l2,l3,l4,l5,B1,B2,B3,B5,win,frame_1,cap,detector,side,warning
    def loop():
        global f,cTime,pTime,minutes,seconds,tminutes,tseconds,bbox,cap,label1,bbox,l1,l2,l3,l4,l5,B1,B2,B3,B5,win,frame_1,cap,detector,img,side,warning
        success, img = cap.read()
        if(success==False and seconds!=0):
            ques=messagebox.askyesno(title="Video Ended",message="Play Again?")
            if ques:
                again()
            else:
                destroyl()
        img = cv2.resize(img, (win.winfo_screenwidth ()-300,win.winfo_screenheight()-180))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findPose(img,draw=bbox)  # with draw
        poses=detector.findPosition(img,bboxWithHands=bbox,draw=bbox) 
         
        if poses:
            try:
                lmList1 = {i[0]:[i[1],i[2],i[3]] for i in poses[0]}
                if lmList1[11][2]<lmList1[12][2]:
                    side="Left"
                    p1=lmList1[7][0:2]
                    p2=lmList1[11][0:2]
                    p3=lmList1[23][0:2]
                    p4=lmList1[25][0:2]
                    p5=lmList1[27][0:2]
                elif lmList1[11][2]>lmList1[12][2]:
                    side="Right"
                    p1=lmList1[8][0:2]
                    p2=lmList1[12][0:2]    
                    p3=lmList1[24][0:2]
                    p4=lmList1[26][0:2]
                    p5=lmList1[28][0:2]
            except:
                warning="Get into\n Position"
                
            finally:
                
                if lmList1=={}:
                    side="__"
                    warning="no detection"
                else:
                    try:
                        warning=checkSlope(p1,p2,p3,p4,p5)
                    except:
                        pass
                if(f==0):
                    img=cv2.flip(img, 1)
                    B3.config(state="disabled")
                    B4.config(state="disabled")
                    B5.config(state="normal")
   
                l1.config(text=f"side: {side}")
                l5.config(text=warning)
                cTime=time.time()
                fps=1/(cTime-pTime)
                dif=cTime-pTime
                pTime=cTime
                seconds+=dif
                if (seconds)>=60:
                    seconds=0
                    minutes+=1
                if warning=="Fine":
                    print(dif)
                    tseconds += dif
                    if (tseconds)>=60:
                        tseconds=0
                        tminutes+=1
                l3.config(text=f"Total Time\n{minutes}: {int(seconds):02}")
                l4.config(text=f"Plank Time\n{tminutes}: {int(tseconds):02}")
                # print(f"Plank Time\n{tminutes}: {int(tseconds):02}")
                # print(warning)
                img = Image.fromarray(img)
                finalImage = ImageTk.PhotoImage(img)
                label1.configure(image=finalImage)
                label1.image = finalImage
                win.after(1, loop)
        
    loop()
    win.mainloop() 
def initilize(f):
    global win,frame_1,side,bbox,l1,l2,l3,l4,l5,B1,B2,B3,B4,B5,w,h,cTime,pTime,minutes,seconds,tminutes,tseconds,cap,detector,label1,side,warning
    minutes=0
    seconds=0
    tminutes=0
    tseconds=0
    pTime=time.time()
    cap = cv2.VideoCapture(f)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, win.winfo_screenwidth ()-300)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, win.winfo_screenheight()-180)
    detector = PoseDetector(detectionCon=0.5)
    label1 = Label(frame_1,width=win.winfo_screenwidth ()-300,height= win.winfo_screenheight()-180,bg="black")
    label1.place(x=0, y=0)
    select_img()

#main progrm
#global f
#global win,frame_1,side,bbox,l1,l2,l3,l4,l5,B1,B2,B3,B4,B5,w,h,cTime,pTime,minutes,seconds,tminutes,tseconds,cap,detector,label1,warning,d
startscreen()
win = Tk()
win.geometry(f"{win.winfo_screenwidth ()-20}x{win.winfo_screenheight()}+0+0")
win.title("PlankApp")

d=(os.getcwd())
bg= ImageTk.PhotoImage(file=f"{d}\\l.jpg")
canv = Label(win, bg='white',image=bg)
canv.place(x=0,y=0)

frame_1 = Frame(win, bg="#581845",width=win.winfo_screenwidth ()-300,height= win.winfo_screenheight()-180).place(x=0, y=0)
side="__"
bbox=True
l1= Label(win,text=f"side: {side}",font=('Helvatical bold',20),relief=RIDGE)
l1.place(x=win.winfo_screenwidth ()-290,y=10)
warning="Not detected\najust camera"
l2= Label(win,text="Message box",font=('Helvatical bold',20),relief=RIDGE)
l2.place(x=win.winfo_screenwidth ()-290,y=50)
l5= Label(win,text=warning,font=('Helvatical bold',20))
l5.place(x=win.winfo_screenwidth ()-290,y=100)
B1=Button(win,width=10,height=2,text="bbox",padx=10,font=('Helvatical bold',20),fg="black",bg="green",command=box)
B1.place(x=0,y=win.winfo_screenheight()-180)
B2=Button(win,width=10,height=2,text="Search File",padx=10,font=('Helvatical bold',20),fg="black",bg="gold",command=search)
B2.place(x=200,y=win.winfo_screenheight()-180)
B3=Button(win,width=10,height=2,text="Live Cam",padx=10,font=('Helvatical bold',20),fg="white",bg="red",command=live)
B3.place(x=400,y=win.winfo_screenheight()-180)
B4=Button(win,width=10,height=2,text="↺\nPlay Again",padx=10,font=('Helvatical bold',20),fg="white",bg="blue",command=again)
B4.place(x=600,y=win.winfo_screenheight()-180)
B5=Button(win,width=10,height=2,text="Reset Timer",padx=10,font=('Helvatical bold',20),fg="white",bg="sky blue",command=retime)
B5.place(x=800,y=win.winfo_screenheight()-180)
w = 1280
h = 720
cTime=0 # Current Time Value

minutes=0
seconds=0
tminutes=0
tseconds=0
f=0
l3= Label(win,text=f"Total Time\n{minutes}: {int(seconds):02}",font=('Helvatical bold',20),relief=GROOVE)
l3.place(x=win.winfo_screenwidth ()-290,y=250)
l4= Label(win,text=f"Plank Time\n{tminutes}: {int(tseconds):02}",font=('Helvatical bold',20),relief=GROOVE)
l4.place(x=win.winfo_screenwidth ()-290,y=350)

initilize(f)



    