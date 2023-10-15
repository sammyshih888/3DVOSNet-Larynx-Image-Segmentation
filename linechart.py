# [Lib]
import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
import numpy as np
import xlrd
import os





# 各指標名稱
name = ["",  "B. Length(R)", "C. Length(L)", "D. Dev_LenVF", "E. Area(R)", 
        "F. Area(L)", "G. Dev_AreaVF", "H. Curvature(R)", "I. Curvature(L)", "J. Area(Glot)", "K. Angle(Glot)", "L. Symmetry(VF)"]

def rename(ex_name):
    # data 去除檔名
    filename = ex_name["A. Filename(Label)"].values
    F = []
    for i in range(filename.shape[0]):
        fn = int(filename[i].strip('.png'))
        F.append(fn)
        
    # int64 才可以排序
    F = np.array(F, dtype='int64')
       
    ex_name["filename"] = pd.Series(F)
    
    ex_name.sort_values(by="filename", inplace=True, ascending=False) 
	
# https://ithelp.ithome.com.tw/articles/10211485
# [drawing] -- linechart
def draw_linechart(df1,f_info): 

    for item in range(1,12):
        # setting x_value, y_value
        plt.plot(df1["filename"], df1[str(name[item])], c="r")
        
        # setting tag / position
        plt.legend(labels=["filename", str(name[item])], loc="best")
        plt.xlabel("number", fontweight = "bold")
        plt.ylabel(str(name[item]), fontweight = "bold") 
        
        # 設定標題、文字大小、粗體及位置
        plt.title("ob3", fontsize = 15, fontweight = "bold", y = 1)
        
        # 將x軸數字旋轉45度，避免文字重疊
        plt.xticks(rotation=45)   

        # save image [3]:interface_miao；[1]:search_analysis
        
        if f_info == 3:
            plt.savefig("./result/" + str(item) + ".png")
            
        elif f_info == 1:
            plt.savefig("./result/all_patient/"+ str(item) + ".png")

        # del 
        plt.cla()
        
    
    # close picture
    #plt.close()
        

 