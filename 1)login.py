# - [Use] - Interface of ob3 login
# - [Author] - miao
# - [Library] -
import tkinter as tk
import subprocess

from PIL import Image, ImageTk


# - [Root] - Tkinter Window
root = tk.Tk()
root.state("zoomed")
root.title("利用3D VOSNet 進行連續喉內視鏡影像物件切割暨喉部物件之聲帶及聲門指標產生系統")

# - [icon] -
# setting icon need to put behind
root.iconbitmap("./image/ob3_icon.ico")

# - [Func] - choose mode
def choice_mode():
    choose_value.get()

# - [Func] - 
def login():
    subprocess.call('python ./2)search_patient.py',shell=True);#跳到下一頁
    root.destroy()       

# ---------------------- [header] ------------------------------#
# - [Frame] - 
header = tk.Frame(root, background="#E7E6E6", height=350, width=1600)
header.place(x=0, y=0)

# - [Image] - 
_icon       = Image.open("./image/icon.png")
icon_resize = _icon.resize((200, 200), Image.ANTIALIAS)
icon_change = ImageTk.PhotoImage(icon_resize)
icon        = tk.Label(header, image=icon_change, bd=0, bg='#E7E6E6').place(x=150, y=80)


# - [Text] - 
title = tk.Label(header, text="Intelligent Videostroboscopy\nIdentification System", bd=0, bg='#E7E6E6',\
                 fg='#843C0C', font=("times new roman", 60)).place(x=420, y=80)




# ---------------------- [Footer] ------------------------------#
# - [Frame] - 
footer = tk.Frame(root, background="#BFBFBF", height=500, width= 1600)
footer.place(x=0, y=350)

# - [Image] - 
_login_frame = Image.open("./image/login_frame.png")
frame_resize = _login_frame.resize((700, 300), Image.ANTIALIAS)
frame_change = ImageTk.PhotoImage(frame_resize)
login_frame  = tk.Label(footer, image=frame_change, bd=0, bg='#BFBFBF').place(x=400, y=80)

# - [Text] - 
manual = tk.Label(footer, text="System Manual", bd=0, bg="#BFBFBF", font=("times new roman", 15, "bold")).place(x=700, y=5)
hint   = tk.Label(footer, text="This system uses the deep learning algorithm to automatically analyze the stroboscopy to assist the doctor.",\
                  bd=0, bg="#BFBFBF", font=("times new roman", 13)).place(x=380,y=40)
                  
#Mode   = tk.Label(footer, text="Mode", bd=0, bg="#E7E6E6", font=("times new roman", 20, "bold")).place(x=550, y=100)
Account= tk.Label(footer, text="Account", bd=0, bg="#E7E6E6", font=("times new roman", 20, "bold")).place(x=700, y=100) #x=850
Password= tk.Label(footer, text="Password", bd=0, bg="#E7E6E6", font=("times new roman", 20, "bold")).place(x=700, y=210)

# - [Radio Button]-
#choose_value  = tk.IntVar()
#Individual    = tk.Radiobutton(footer, text="Individual Anaylsis", bg="#E7E6E6", font=("times new roman", 18), variable=choose_value, value=1, command=choice_mode)
#Individual.place(x=450, y=180)
#Individual.select()

#Comprehensive = tk.Radiobutton(footer, text="Comprehensive Analysis", bg="#E7E6E6", font=("times new roman", 18), variable=choose_value, value=2,command=choice_mode)
#Comprehensive.place(x=450, y=250)

# - [Entry] -
Account_entry = tk.Entry(footer, width=30, relief="groove", font="5").place(x=615, y=160) #x=780
Password_entry = tk.Entry(footer, width=30, relief="groove", font="5", show="*").place(x=615, y=250)

# - [Button] -
login = tk.Button(footer, text='Login', activebackground='#8093AE', bg="#D6DCE5", font=("times new roman", 15), command=login).place(x=710, y=320)



# - [Root] - keep showing
root.mainloop()