# [Lib]
import tkinter as tk
import pandas as pd
import numpy as np
import os

from tkinter import Frame,PhotoImage,ttk,Scrollbar,TclError
from tkinter.ttk import Treeview
from PIL import Image,ImageTk
from tkinter import ttk


# [rename]
def rename(ex_name):
    # data 去除檔名
    filename = ex_name["A. Filename(Label)"].values
    F = []
    for i in range(filename.shape[0]):
        fn = int(filename[i].strip('.png'))
        F.append(fn)
        
    # int64 才可以排序
    F = np.array(F, dtype='int64')
    
    ex_name["number"] = pd.Series(F)
    
    ex_name.sort_values(by="number", inplace=True, ascending=False)
    

# [sort]  
def sort(img_name, name,medi_value, item, df, f_info):
    # 若無點選btn 
    if item == 0 and f_info!=1:
        # change pic name
        rename(df)

    else:
        df.sort_values(by=str(name[item]), inplace=True, ascending=True) 
        
        # median 
        row = df.shape[0]
        all = list(df[str(name[item])])
       
        
        if row % 2 and item != 0:
            m = all[int((row/2))]
            medi_value.set("Median："+str(round(m,4)))
         
        elif item==0:
            medi_value.set("")
        else:
            m = (all[int((row/2))] + (all[int((row/2))]))/2
            medi_value.set("Median："+str(round(m,4)))



# [pic resize] -- reHeight == 280
def pic_size(Width,Height,f_info):
    
    if f_info == 2:
        reHeight = 280 
        
    elif f_info == 1:
        reHeight = 220 
        
    reWidth  = int(reHeight * Width / Height)
    
    return reWidth, reHeight
        
# [treeview]
def search(root, img_name, vidname, item, df, f_info):

    #frame容器放置表格,使用Treeview元件實現表格功能
    frame = Frame(root)
    
    # f_info [1]:多病患; [2]:單一病患
    if f_info == 1 or f_info=="":
        frame.place(x=430, y=410, width=1100,height=380)
    else:
        frame.place(x=235, y=410, width=1265,height=380)

    #加載滾動條
    scrollBar = tk.Scrollbar(frame)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

    tree=ttk.Treeview(root)
    
    # 欄位名稱
    if item == 12:
        tree_cols = ["","Length(R)","Length(L)","Dev_LenVF"
                    ,"Area(R)", "Area(L)", "Dev_AreaVF", "Curvature(R)", "Curvature(L)"
                    , "Area(Glot)", "Angle(Glot)", "L. Symmetry(VF)"]
                      
    else:
        tree_cols = ["filename","Length(R)","Length(L)","Dev_LenVF"
                    ,"Area(R)", "Area(L)", "Dev_AreaVF", "Curvature(R)", "Curvature(L)"
                    , "Area(Glot)", "Angle(Glot)", "Symmetry(VF)"]    

    #準備表格Treeview元件, 3列, 顯示標頭. 帶垂直滾動條
    tree = Treeview(frame ,
                    columns=tree_cols,
                    show="headings",
                    yscrollcommand=scrollBar.set)
    
    
    for i in range(len(tree_cols)):
   
        tc = tree_cols[i]
        if f_info==1 or f_info=="":
            #設定每列寬度和對其方式
            tree.column(tc, width=92,anchor="center")
        else:
            #設定每列寬度和對其方式
            tree.column(tc, width=105,anchor="center")
            
        #設應每列標題文字
        tree.heading(tc ,text=tc )


    #加載表格訊息
    tree.pack(side=tk.LEFT, fill=tk.Y)

    # 設置關聯, Treeview元件與垂直滾動條結合
    scrollBar.config(command=tree.yview)
    
    if f_info != "":
        # reverse
        del tree_cols[0]
        tree_cols.reverse()
        
        # put data to tree
        
        for i in range(df.shape[0]):
            ttk.Style().theme_use('default')
            
            # [Value] excel to list
            L_data = list(df.iloc[i,:])
            
            #print(L_data)
            
            if item == 0 and f_info !=1:
                del L_data[0], L_data[12]
                
            elif item == 12: 
                L_data.reverse()
                
                L_data.insert(0,str(tree_cols[i]))

            elif f_info !=1:
                del L_data[0]
          
            
            tree.insert("",0,values=L_data)
        
       # 雙擊後執行
    def treeviewClick(event):
        global ob3
        
        item_text=""
        for item in tree.selection():
            item_text = tree.item(item,"values")
            # print(item_text[0])#輸出所選行的第一列的值
        
        # 若是單個病患則顯示該影像；若是多病患則顯示第一張
        if f_info==2:
            im4  = Image.open("./Output/"+str(vidname)+"/raw_label/"+str(item_text[0]))
         
        else:
           # all analysed patient
           path = "./Output/"+str(item_text[0])+"/raw_label"
           
           lists = os.listdir(path) 
           
           #按時間排序
           lists.sort(key=lambda fn:os.path.getmtime(path + "\\" + fn))
           
           #獲取最新的文件保存到file_new
           file_new = os.path.join(path,lists[0])
           
           im4  = Image.open(str(file_new))
           
        (Width,Height) = im4.size
        reWidth,reHeight = pic_size(Width,Height,f_info)
        
        img5 = im4.resize((reWidth,reHeight),Image.ANTIALIAS)
        
        #print(reWidth,reHeight)
        ob3   = ImageTk.PhotoImage(img5)
        
        if f_info==1:
            imLabe=tk.Label(root, image=ob3,bd=0,bg='#000000').place(x=1100, y=90)
        else:
           imLabe=tk.Label(root, image=ob3,bd=0,bg='#000000').place(x=1100, y=70) 
        # put [text]
        img_name.set("Image name："+str(item_text[0])) 
        
    if item != 12 and f_info!="":
        #<Double-1> 左鍵點一下
        tree.bind('<ButtonRelease-1>', treeviewClick)
    
    return tree, scrollBar

# [calculate]
def cal(max_value, min_value, std_value, mean_value, Mode_value, medi_value, item, df, name):
    if item!=0 :
        ob3_Max = df[name[item]].max()
        ob3_Min = df[name[item]].min()
        ob3_Std = df[name[item]].std()
        ob3_Mean = df[name[item]].mean()
        
        max_mode = list(df[name[item]])
        ob3_mode = max(max_mode,key=max_mode.count)
        
        
        # put [text]
        max_value.set("Max：" + str(round(ob3_Max, 4)))
        min_value.set("Min：" + str(round(ob3_Min, 4)))
        std_value.set("Std：" + str(round(ob3_Std, 4)))
        mean_value.set("Mean：" + str(round(ob3_Mean,4)))
        Mode_value.set("Mode：" + str(round(ob3_mode,4)))

    else:
        # Remove [text]
        max_value.set("Max：")
        min_value.set("Min：")
        std_value.set("Std：")
        mean_value.set("Mean：")
        medi_value.set("Median：")
        Mode_value.set("Mode：" )    


# [btn]
def btn(root):
    Len_R = tk.Button(root, text="Length(R)" ,bg="#EDEDED",bd=3,padx=29,activebackground="#EDEDED",font=("times new roman",15))
    

    Len_L = tk.Button(root, text="Length(L)" ,bg="#EDEDED",bd=3,padx=29,activebackground="#EDEDED",font=("times new roman",15))
    

    Dev_L = tk.Button(root, text="Dev_LenVF" ,bg="#EDEDED",bd=3,padx=21, activebackground="#EDEDED",font=("times new roman",15))
   

    A_R = tk.Button(root, text="Area(R)" ,bg="#EDEDED",bd=3,padx=35, activebackground="#EDEDED",font=("times new roman",15))
    

    A_L = tk.Button(root, text="Area(L)" ,bg="#EDEDED",bd=3,padx=35, activebackground="#EDEDED",font=("times new roman",15))
   

    Dev_A = tk.Button(root, text="Dev_AreVF" ,bg="#EDEDED",bd=3,padx=20,activebackground="#EDEDED",font=("times new roman",15))
    

    C_A = tk.Button(root, text="Cur(R)" ,bg="#EDEDED",bd=3,padx=40, activebackground="#EDEDED",font=("times new roman",15))
    

    C_L = tk.Button(root, text="Cur(L)" ,bg="#EDEDED",bd=3,padx=40, activebackground="#EDEDED",font=("times new roman",15))
   

    A_G = tk.Button(root, text="Area_Glot" ,bg="#EDEDED",bd=3,padx=25,activebackground="#EDEDED",font=("times new roman",15))
    

    Ang_G = tk.Button(root, text="Angle_Glot" ,bg="#EDEDED",bd=3,padx=22, activebackground="#EDEDED",font=("times new roman",15))
    
    Symmetry = tk.Button(root, text="Symmetry(VF)" ,bg="#EDEDED",bd=3,padx=10,activebackground="#EDEDED",font=("times new roman",15))
    
    File_N = tk.Button(root, text="filename" ,bg="#EDEDED",bd=3,padx=33,activebackground="#EDEDED",font=("times new roman",15))
    

    Corr = tk.Button(root, text="correlation" ,bg="#EDEDED",bd=3,padx=24,activebackground="#EDEDED",font=("times new roman",15))
    
    
    
    return Len_R, Len_L, Dev_L, A_R, A_L, Dev_A, C_A, C_L, A_G, Ang_G, Symmetry, File_N, Corr
    
    