# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 16:51:59 2019

@author: D3ll
"""

""" GUI for breast cancer NN"""

import tkinter as tk
from tkinter import filedialog, Text
import os
import scipy.io as sp
import numpy as np

#loading variables for neural network
cancer_results=sp.loadmat("cancer_weights.mat")
w1=cancer_results["w1"]
b1=cancer_results["b1"]
w2=cancer_results["w2"]
b2=cancer_results["b2"]
data_val=cancer_results["data_val"]
index=int(cancer_results["index"])
training=data_val[:index,:]
testing=data_val[index:,:]

#variables for visuals
color="#FFB4BC"#"#263D42"
font_color="#050000"
app_font="Helvetica"
canvas_width=700
canvas_height=400
fields_y=canvas_height*.4

sigma= lambda x: 1/(1+np.exp(-x))
dsigma= lambda x: sigma(x)*(1-sigma(x))

def test_nn():
    x=np.array([float(texture.get()), float(area.get()), float(smoothness.get())])
    x=x.reshape((1,3))
    d=np.vstack((training[:,:-1],x))
    d=(d - d.mean(axis=0)) / d.std(axis=0)
    x=d[-1,:]
    x=x.reshape((3,1))
    net1=w1.dot(x)+b1
    out1=sigma(net1)
    net2=w2.dot(out1)+b2
    out2=sigma(net2)
    if np.float(out2)>.5:
        dx_label=tk.Label(root, text="Maligno",font=(app_font,20), background=color,foreground=font_color)
        canvas.create_window(canvas_width*.5,canvas_height*.6,window=dx_label)
    else:
        dx_label=tk.Label(root, text="Benigno", font=(app_font,20), background=color,foreground=font_color)
        canvas.create_window(canvas_width*.5,canvas_height*.6,window=dx_label)

def knn():
    k=7
    x=np.array([float(texture.get()), float(area.get()), float(smoothness.get())])
    assigned_types=[]
    #target=x[-1]
    x=x.reshape((1,3))
    dist=np.sum((data_val[:,:-1]-x)**2,axis=1)
    ind=np.argsort(dist)
    dist=dist[ind[:k]]
    neighbors=data_val[ind[:k],:]
    types=list(set(neighbors[:,-1]))
    n_type=[]
    for t in types:
        n_type.append(np.sum((neighbors[:,-1]==t)*1))
        
    assigned_types.append(types[np.argmax(n_type)])
    assigned_types=np.array(assigned_types)
    assigned_types=np.resize(assigned_types,(len(assigned_types),1))
    x=np.hstack((x,assigned_types)) #ultima columna idica resultado de knn
    if np.float(x[:,-1])==1:
        dx_label=tk.Label(root, text="Maligno",font=(app_font,20), background=color,foreground=font_color)
        canvas.create_window(canvas_width*.5,canvas_height*.6,window=dx_label)
    else:
        dx_label=tk.Label(root, text="Benigno", font=(app_font,20), background=color,foreground=font_color)
        canvas.create_window(canvas_width*.5,canvas_height*.6,window=dx_label)

root=tk.Tk()
canvas=tk.Canvas(root,height=canvas_height,width=canvas_width,bg=color)
canvas.pack()

#title
title_label=tk.Label(root, text="Diagnóstico de Cáncer", pady=5, padx=10, 
                     background=color, font=(app_font,30), foreground=font_color)
canvas.create_window(canvas_width*.5,canvas_height*.1,window=title_label)

#texture entry
texture_x=canvas_width*.25
texture_label=tk.Label(root, text="Textura",background=color, font=(app_font,15), foreground=font_color)
canvas.create_window(texture_x, fields_y, window=texture_label)
texture=tk.Entry(canvas, width=8)
canvas.create_window(texture_x+70, fields_y, window=texture)

#area entry
area_x=canvas_width*.45
area_label=tk.Label(root,text="Área", background=color, font=(app_font,15), foreground=font_color)
canvas.create_window(area_x, fields_y, window=area_label)
area=tk.Entry(canvas, width=8)
canvas.create_window(area_x+60, fields_y, window=area)

#smoothness entry
smoothness_x=canvas_width*.65
smoothness_label=tk.Label(root,text="Suavidad", background=color, font=(app_font,15), foreground=font_color)
canvas.create_window(smoothness_x, fields_y, window=smoothness_label)
smoothness=tk.Entry(canvas,width=8)
canvas.create_window(smoothness_x+80, fields_y, window=smoothness)

#NN button
nn_button=tk.Button(root,text="Red Neuronal",font=(app_font,15), command=test_nn)
canvas.create_window(canvas_width*.45,canvas_height*.9,window=nn_button)

#KNN button
knn_button=tk.Button(root,text="KNN",font=(app_font,15), command=knn)
canvas.create_window(canvas_width*.6,canvas_height*.9,window=knn_button)

root.mainloop()
