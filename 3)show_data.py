# [Lib]
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
import subprocess
import win32gui
import win32con
import time
import os

# [miao] - def - 
import func.ob3_func as ob3_f

from tkinter import PhotoImage
from PIL import Image,ImageTk

# [ROOT] - TKinter Window - 

root=tk.Tk()
root.configure(background="#EDEDED")
#root.title("基於人工智慧之喉頻閃視訊辨識系統")
root.state("zoomed")
root.title("利用3D VOSNet 進行連續喉內視鏡影像物件切割暨喉部物件之聲帶及聲門指標產生系統")


# need to put behind
root.iconbitmap("./image/ob3_icon.ico")

# put image
im1 = Image.open("./images/bg2.png")
img = im1.resize((1500,730),Image.ANTIALIAS)
# img.paste(img,(237,237,237),mask=img)
img1=ImageTk.PhotoImage(img)
imLabe=tk.Label(root, image=img1,bd=0,bg='#EDEDED').place(x=10, y=60)


im2 = Image.open("./images/back1.png")
img2= im2.resize((40,40),Image.ANTIALIAS)
img3=ImageTk.PhotoImage(img2)

h  = Image.open("./images/home1.png")
h1 = h.resize((40,40),Image.ANTIALIAS)
h2=ImageTk.PhotoImage(h1)

# [txt] - video_name
vid = open("./name.txt", mode = "r")
vidname = vid.read()


# [variable] - declare textvariable -  
statis_name = tk.StringVar()
max_value   = tk.StringVar()
min_value   = tk.StringVar()
std_value   = tk.StringVar()
mean_value  = tk.StringVar()
medi_value  = tk.StringVar()
Mode_value  = tk.StringVar()
class_n  = tk.StringVar()

img_name    = tk.StringVar()



# 各指標名稱
name = ["",  "B. Length(R)", "C. Length(L)", "D. Dev_LenVF", "E. Area(R)", 
        "F. Area(L)", "G. Dev_AreaVF", "H. Curvature(R)", "I. Curvature(L)", "J. Area(Glot)", "K. Angle(Glot)", "L. Symmetry(VF)"]

# [global] - variable - 
global item 
item=0


# [Func] - Function Definition - 

# [show_sort]  
def show_sort(root,img_name, medi_value,item, df):
    # [sort]
    ob3_f.sort(img_name, name, medi_value, item, df,2)
    # tree    
    tree, scrollBar = ob3_f.search(root, img_name, vidname, item, df, 2)
    
# [corr]
def data_corr(item,df):
    # del excel col
    df = df. drop(['Unnamed: 0'],axis=1) 
    
    cor = df.corr()
    tree, scrollBar = ob3_f.search(root, img_name, vidname, item, cor, 2)
     
# [img] - show linechart - 
def show_LC(item):
    # image open in def need to global it
    global LC
    im3  = Image.open("./result/"+str(item)+".png")
    img4 = im3.resize((448,336),Image.ANTIALIAS)
    LC   = ImageTk.PhotoImage(img4)
    imLabe=tk.Label(root, image=LC,bd=0,bg='#EDEDED').place(x=610, y=60)
    
# [Func] - btn analysis - 
def processing(item):
    
    # load excel
    df = pd.read_excel("./Output/"+str(vidname)+"/"+str(vidname)+".xlsx")

    
    if item ==0:
        show_sort(root,img_name, medi_value,item, df)

        ob3_f.cal(max_value, min_value, std_value, mean_value, Mode_value, medi_value, item, df, name)

        statis_name.set("Statistical indicators")
        show_LC(str(item+1))
        
        
    elif item==12:
        data_corr(item,df)
        
    else:
        show_sort(root,img_name, medi_value,item, df)

        ob3_f.cal(max_value, min_value, std_value, mean_value, Mode_value, medi_value, item, df, name)
        
        # put [text]
        sn = name[item]
        statis_name.set(str(sn[3:]))
               
        show_LC(str(item))

# back
def back():
    subprocess.call('python ./2)search_patient.py',shell=True);#跳到下一頁
    root.destroy()

# home
def Home():
    subprocess.call('python ./1)login.py',shell=True);#跳到下一頁
    root.destroy()
    
# initial 
processing(0)


# [obj] - Text - 
tk.Label(root, text="Sort By",bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 20, "bold")).place(x=60, y=70)

# [obj] - Textvariable - 
statis_name.set("Statistical indicators")
tk.Label(root, textvariable=statis_name,bd=0,bg='#EDEDED',fg="#e6bb00",font=("times new roman", 20)).place(x=250, y=80)

max_value.set("Max：")
tk.Label(root, textvariable=max_value,bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 18)).place(x=250, y=125)

min_value.set("Min：")
tk.Label(root, textvariable=min_value,bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 18)).place(x=250, y=165)

std_value.set("Std：")
tk.Label(root, textvariable=std_value,bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 18)).place(x=250, y=205)

mean_value.set("Mean：")
tk.Label(root, textvariable=mean_value,bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 18)).place(x=250, y=245)

medi_value.set("Median：")
tk.Label(root, textvariable=medi_value,bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 18)).place(x=250, y=285)

Mode_value.set("Mode：")
tk.Label(root, textvariable=Mode_value,bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 18)).place(x=250, y=325)

#class_n.set("Class：")
tk.Label(root, textvariable=class_n,bd=0,bg='#EDEDED',fg="#000000",font=("times new roman", 18)).place(x=250, y=365)

# ---
img_name.set("Image name：please choose image")
tk.Label(root, textvariable=img_name,bd=0,bg='#000000',fg="#ffffff",font=("times new roman", 18)).place(x=1145, y=350)

# ---------------------------------------------------

# [Obj] - Button - 
button= tk.Button(root, image=img3,bg="#EDEDED",bd=0,activebackground="#EDEDED",command=back).place(x=10, y=10)

button= tk.Button(root, image=h2,bg="#EDEDED",bd=0,activebackground="#EDEDED",command=Home).place(x=1470, y=10)

# -------------- choose data analyzed ---------------

Len_R, Len_L, Dev_L, A_R, A_L, Dev_A, C_A, C_L, A_G, Ang_G, Symmetry, File_N, Corr = ob3_f.btn(root)

cor_x = 35

Len_R['command'] = lambda:processing(1)
Len_R.place(x=cor_x,y=115)

Len_L['command'] = lambda:processing(2)
Len_L.place(x=cor_x,y=170)

Dev_L['command'] = lambda:processing(3) 
Dev_L.place(x=cor_x,y=220)

A_R['command'] = lambda:processing(4)
A_R.place(x=cor_x,y=270)

A_L['command'] = lambda:processing(5)
A_L.place(x=cor_x,y=320)

Dev_A['command'] = lambda:processing(6)
Dev_A.place(x=cor_x,y=370)

C_A['command'] = lambda:processing(7)
C_A.place(x=cor_x,y=420)

C_L['command'] = lambda:processing(8)
C_L.place(x=cor_x,y=470)

A_G['command'] = lambda:processing(9)
A_G.place(x=cor_x,y=520)

Ang_G['command'] = lambda:processing(10)
Ang_G.place(x=cor_x,y=570)

Symmetry['command'] = lambda:processing(11)
Symmetry.place(x=cor_x,y=620)

File_N['command'] = lambda:processing(0)
File_N.place(x=cor_x,y=670)

Corr['command'] = lambda:processing(12)
Corr.place(x=cor_x,y=720)

# -------------- choose data analyzed ---------------

# [ROOT] - Main Loop - 

root.mainloop()



