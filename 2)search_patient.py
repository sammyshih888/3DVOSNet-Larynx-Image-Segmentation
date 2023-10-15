# - [Use] - Interface of search
# - [Author] - miao
# - [Library] -
import tkinter as tk
import pandas as pd
import subprocess
import easygui
import imageio
import time
import cv2
import os

from tkinter import messagebox,ttk
from PIL import Image, ImageTk
from imageio import get_reader

# miao ob3
import linechart  as LC


# - [Root] - Tkinter Window
root = tk.Tk()
root.configure(background="#EDEDED")
root.state("zoomed")
root.title("利用3D VOSNet 進行連續喉內視鏡影像物件切割暨喉部物件之聲帶及聲門指標產生系統")

# - [icon] -
# setting icon need to put behind
root.iconbitmap("./image/ob3_icon.ico")

# ---------------------- [Function] ------------------------------#
lock=0

ratio_H = 0.6
ratio_W = 0.9
#ratio_S = 1.5
#ratio_L = 0.8
i=0

def control_video():
	
	global lock
	lock += 1
	
	print(f"lock = {lock}")
	
	if lock % 2 == 1:
		btn_play.set("Play")
	else:
		btn_play.set("Stop")

# - [Func] - indicator      
def indicator(name, img_show):
    # - Show Analyzed Result -
    with open("./Output/"+name[0:-4]+"/txt/"+img_show[0:-4]+".txt","r",encoding="utf-8") as f:
        # 變數 lines 會儲存 filename.txt 的內容
        line   =  f.readlines()
        
        Length_R.set(line[0])
        Length_L.set(line[1])
        Dev_LenVF.set(line[2])
        Area_R.set(line[3])
        Area_L.set(line[4])

        Dev_AreVF.set(line[5])
        Cur_R.set(line[6])
        Cur_L.set(line[7])
        Area_Glot.set(line[8])
        Angle_Glot.set(line[9])
        Symmetry.set(line[10])

# - [Func] - select video
def select_video(content):
	
	global path,name,new_path,lock
	
	# Select Video
	path = easygui.fileopenbox()
	
	# Check if choose video file
	try:
		if not path.endswith(".mp4"):
			tk.messagebox.showinfo(title='Warning', message='Please Choose a "Video"！') #警告:未選擇視訊檔
			print(f"\n[Err] File type : {type(path)}")
			return
	except:
		return
	
	v_name = path
	name = os.path.basename(path)
	new_path = os.path.dirname(path)
	
	print(f"\n[INFO] Video Name: {name}\nPath: {new_path}")
	
   
    
	logs = open('name.txt',"w+")
	logs.write(name[0:-4])
	logs.close()
	
	# [Label] - show video infromation - 
	
	video_name.set(f"Video Name：{name}")
	
	video = imageio.get_reader(v_name)
   
	# video_size
	vid = cv2.VideoCapture(v_name)
	height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
	width  = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
	fps    = int(vid.get(cv2.CAP_PROP_FPS)+0.5)
	print(f"\n[INFO] VID:{vid} \n height:{height} \n width:{width} \n fps:{fps}")
	

	
	delay = int(1000 / video.get_meta_data()['fps'])
	
	def stream(label):
		
		try:
			if lock % 2 == 0:
				image = video.get_next_data()
		
		except:
			video.close()
			return
		
		label.after(delay, lambda: stream(label))
		frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        
		label.config(image=frame_image)
		label.image = frame_image
	
	my_label = tk.Label(content,height=300,width=400,bg='#000000')
	my_label.place(x=45,y=165)
	my_label.after(delay, lambda: stream(my_label))
	
	# - [Change] - (1) Button
	analysis['state'] = tk.NORMAL
	btn_playVideo['state'] = tk.NORMAL
	Physical['state'] = tk.NORMAL
    
    # - [Change] - (2) Label
	P_ID.set("ID：" + name[0:-4] )
	P_Name.set("Name：TING-TING CHANG")
	P_Gender.set("Gender：Female")
    
	return name

# - [Func] - show result
def show_analysis(content):
    global IMG_Result,img11
    # - [change] - (1) Button        
    Last['state'] = tk.NORMAL
    Next['state'] = tk.NORMAL
    
    # - [Time] -
    tk.messagebox.showinfo(title='Hint', message='Start Analysis !!')
    
    progress = ttk.Progressbar(content, length=300, mode='determinate')
    progress.place(x=700, y=220)
    progress['value'] = 0
    percent.set("0%")
    content.update()
    
    runProgressBar(progress, content, iter=256)

            
    progress.destroy()
    
    tk.messagebox.showinfo(title='Hint', message='Analysis Complete!!')
    
    # - [Name] -
    with open('./name.txt',"r") as fid:
        fname = fid.read()
        fid.close()
        
    # - [Show Image] - 
    find_path = ("./Output/"+fname+"/raw_label")
    a=os.listdir(find_path)
    a.sort()
    a.sort(key=lambda x:int(x[:-4]))
    img_show=a[0]
    print(f"\n[info]img_show = {img_show}")
	
    im6 = Image.open("./Output/"+fname+"/raw_label/"+img_show)
    (Width,Height) = im6.size
    
    if Width > 400:
        reWidth = int(Width * ratio_W)
        reHeight = int(Height * ratio_H)
    else:
        reWidth = int(Width * ratio_W)
        reHeight = int(Height* ratio_H)
        
	
    img10=im6.resize((reWidth,reHeight),Image.ANTIALIAS)
    img11=ImageTk.PhotoImage(img10)
    IMG_Result = tk.Label(content, image=img11,bd=0,bg='#000000').place(x=620, y=70) #50
    
    icon_vocal = tk.Label(content, image=icon_vocal_change, bd=0, bg='#E7E6E6').place(x=980, y=470)
    
    frame_name.set(f"Image Name：{img_show[0:-4]}.png")
    
    # - [show] -
    indicator(name, img_show)


# - [Func] - frame_Change   
def frame_Change(control, content): 
	
	global i,img11,name,IMG_Result
	
	if control == "<" and i==0 :
		i = 0
        
	elif control == "<" and i!=0 :
		i -= 1
        
	elif control == ">":  
		i += 1
	
	find_path = ("./Output/"+name[0:-4]+"/raw_label")
	a = os.listdir(find_path)
	a.sort()
	a.sort(key = lambda x:int(x[:-4]))
	img_show = a[i]
	
	im6 = Image.open("./Output/"+name[0:-4]+"/raw_label/"+img_show)
	(Width,Height) = im6.size
	
	if Width >400:
		reWidth = int(Width * ratio_W)
		reHeight = int(Height * ratio_H)
	else:
		reWidth = int(Width * ratio_W)
		reHeight = int(Height * ratio_H)
	
	img10 = im6.resize((reWidth,reHeight),Image.ANTIALIAS)
	img11 = ImageTk.PhotoImage(img10)
	IMG_Result = tk.Label(content, image=img11, bd=0,bg='#000000').place(x=620, y=70) #50
	frame_name.set(f"Image Name：{img_show[0:-4]}.png")


	# - [show] -
	indicator(name, img_show)

# - [Func] - progressbar
def runProgressBar(progress, content, iter=256):
    ITER = range(iter)
    
    try:
        for idx,i in enumerate(ITER):
            idx += 1
            unit = idx / len(ITER) * 100
            
            time.sleep(0.02)
            progress['value'] = unit
            percent.set(f"{int(unit)}%")
            content.update()
        
        percent.set("")       
            
    except Exception as e:
        tk.messagebox.showinfo('Info', 'ERROR: {}'.format(e))
	
    return progress
        


# - [Func] - logout
def logout():
    subprocess.call('python ./1)login.py',shell=True);#跳到下一頁
    root.destroy() 

# - [Func] - more information
def more_info():
    global name
    
    # - [Draw] - line_Chart
    indicators = pd.read_excel("./Output/"+str(name[0:-4])+"/"+str(name[0:-4])+".xlsx")
    LC.rename(indicators)    
    LC.draw_linechart(indicators,3)
    
    subprocess.call('python ./3)show_data.py',shell=True);#跳到下一頁
    root.destroy()  
# ---------------------- [Frame] ---------------------------------#
# - [Frame] - (1) tool bar
tool_bar = tk.Frame(root, background="#BFBFBF", height=820, width=350)
tool_bar.place(x=0, y=0)

# - [Frame] - (2) content
content = tk.Frame(root, background="#E7E6E6", height=820, width=1200)
content.place(x=350, y=0)

# ---------------------- [tool bar] ------------------------------#
# - [Image] -
_icon       = Image.open("./image/icon.png")
icon_resize = _icon.resize((200, 200), Image.ANTIALIAS)
icon_change = ImageTk.PhotoImage(icon_resize)
icon        = tk.Label(tool_bar, image=icon_change, bd=0, bg='#BFBFBF').place(x=65, y=50)

_doctor       = Image.open("./image/doctor_info.png")
doctor_resize = _doctor.resize((290, 80), Image.ANTIALIAS)
doctor_change = ImageTk.PhotoImage(doctor_resize)
doctor        = tk.Label(tool_bar, image=doctor_change, bg='#BFBFBF').place(x=30, y=700)

# - [Text] -
tk.Label(tool_bar, text="Doctor Information", bd=0, bg="#BFBFBF", fg="#342569", font=("times new roman", 15)).place(x=43, y=693)
tk.Label(tool_bar, text="Attending Physician：Dr. Wang", bd=0, bg="#BFBFBF", fg="#000000", font=("times new roman", 15)).place(x=50, y=730)

# - [Button] -
open_file = tk.Button(tool_bar, text='Open File',bd=0, activebackground='#DBDBDB', bg="#D9D9D9", font=("times new roman", 20), command=lambda:select_video(content),padx=84, pady=10)
open_file.place(x=30, y=300)

analysis = tk.Button(tool_bar, text='Analysis', bd=0, activebackground='#DBDBDB', bg="#D9D9D9", font=("times new roman", 20),padx=90, pady=10, command=lambda:show_analysis(content))
analysis.place(x=30, y=400)
analysis['state'] = tk.DISABLED

Physical = tk.Button(tool_bar, text='More Information', bd=0, activebackground='#DBDBDB', bg="#D9D9D9", font=("times new roman", 20),padx=40, pady=10, command=more_info)
Physical.place(x=30, y=500)
Physical['state'] = tk.DISABLED

Log_out = tk.Button(tool_bar, text='Log Out', bd=0, activebackground='#DBDBDB', bg="#D9D9D9", font=("times new roman", 20), command=logout,padx=92, pady=10)
Log_out.place(x=30, y=600)

# ---------------------- [content] ------------------------------#
# - [Image] -
_analysis_bg = Image.open("./image/analysis_bg.png")
bg_resize    = _analysis_bg.resize((1200, 800), Image.ANTIALIAS)
bg_change    = ImageTk.PhotoImage(bg_resize)
analysis_bg  = tk.Label(content, image=bg_change, bd=0, bg='#E7E6E6').place(x=0, y=0)

_icon_vocal = Image.open("./image/icon_pic.png")
icon_vocal_resize = _icon_vocal.resize((120, 70), Image.ANTIALIAS)
icon_vocal_change = ImageTk.PhotoImage(icon_vocal_resize)


# - [Text] -         (1) Patient_INFO
tk.Label(content, text="Patient Information", bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=43, y=10)

# - [Textvariable] - (1) Patient_INFO
P_ID     = tk.StringVar()
P_Name   = tk.StringVar()
P_Gender = tk.StringVar()


tk.Label(content, textvariable=P_ID, bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 13)).place(x=43, y=40)
P_ID.set("ID：")
tk.Label(content, textvariable=P_Name, bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 13)).place(x=43, y=70)
P_Name.set("Name：")
tk.Label(content, textvariable=P_Gender, bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 13)).place(x=43, y=100)
P_Gender.set("Gender：")

# - [Text] -         (2) Video
tk.Label(content, text="Patient Video", bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=43, y=145)

# - [Textvariable] - (2) Video
video_name = tk.StringVar()
tk.Label(content, textvariable=video_name, bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=43, y=490)
video_name.set("Video Name：")

# - [Button] - (2) Video
btn_play = tk.StringVar()
btn_playVideo = tk.Button(content,textvariable=btn_play,command=control_video,state=tk.DISABLED,bg="#D9D9D9",bd=0,padx=6,pady=2,activebackground="#C9C9C9",font=("times new roman",12))
btn_playVideo.place(x=420,y=490)
btn_play.set("Pause")

# - [Text] -         (3) Video Frame
tk.Label(content, text="Video Frame", bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=620, y=10)

# - [Textvariable] - (3) Video Frame
frame_name = tk.StringVar()
tk.Label(content, textvariable=frame_name, bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=620, y=490)
frame_name.set("Frame Name：")

# - [Button] -       (3) Video Frame
Last = tk.Button(content, text='\n<\n\n', bd=0, activebackground='#C9C9C9', bg="#D9D9D9", font=("times new roman", 20),command=lambda:frame_Change("<", content),padx=10, pady=155)
Last.place(x=520, y=18)
Last['state'] = tk.DISABLED

Next = tk.Button(content, text='\n>\n\n', bd=0, activebackground='#C9C9C9', bg="#D9D9D9", font=("times new roman", 20), command=lambda:frame_Change(">", content),padx=10, pady=155)
Next.place(x=1115, y=18)
Next['state'] = tk.DISABLED

# - [Text] -         (4) Indicators
tk.Label(content, text="Various Indicators", bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=43, y=535)


# - [Textvariable] - (5) Indicator Length(R)
Length_R = tk.StringVar()
Length_L = tk.StringVar()

Dev_LenVF = tk.StringVar()
Dev_AreVF = tk.StringVar()

Area_R = tk.StringVar()
Area_L = tk.StringVar()

Cur_R = tk.StringVar()
Cur_L = tk.StringVar()

Area_Glot  = tk.StringVar()
Angle_Glot = tk.StringVar()

Symmetry   = tk.StringVar()


# - [Text] - 
tk.Label(content, textvariable=Length_R,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=60, y=570)
tk.Label(content, textvariable=Length_L,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=60, y=610)
tk.Label(content, textvariable=Dev_LenVF,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=60, y=650)
tk.Label(content, textvariable=Area_R,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=60, y=690)
tk.Label(content, textvariable=Area_L,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=60, y=730)

tk.Label(content, textvariable=Dev_AreVF,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=600, y=570)
tk.Label(content, textvariable=Cur_R,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=600, y=600)
tk.Label(content, textvariable=Cur_L,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=600, y=630)
tk.Label(content, textvariable=Area_Glot,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=600, y=660)
tk.Label(content, textvariable=Angle_Glot,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=600, y=690)
tk.Label(content, textvariable=Symmetry,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=600, y=720) 


# - [Progressbar] -
percent = tk.StringVar()
tk.Label(content, textvariable=percent,  bd=0, bg="#E7E6E6", fg="#000000", font=("times new roman", 15)).place(x=850, y=200) 


# - [Root] - keep showing
root.mainloop() 