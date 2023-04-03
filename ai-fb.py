# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 14:13:07 2021

@author: 577
"""


import torch
import torch.nn as nn
import torch.nn.functional as F


from sko.GA import GA

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import numpy as np

import cv2
import matplotlib.pyplot as plt

import win32con
import win32gui
import win32com.client

import pyautogui

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

import requests
import json

import sys
import time
import os
import random
import warnings


shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')

#avoiding warning

warnings.filterwarnings("ignore")

#reproduct

seed = 577

np.random.seed(seed)
random.seed(seed)

torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)

torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = True



def opt_L():
    
    ga = GA(func=opt_min_L, n_dim=1, size_pop=20, max_iter=20, lb=[1.1], ub=[5], precision=1e-7)
    
    best_x, best_y = ga.run()
    
    print('best_x:', best_x, '\n', 'best_y:', best_y)

    return best_x, best_y

def opt_R():
    
    ga = GA(func=opt_min_R, n_dim=1, size_pop=20, max_iter=20, lb=[1.1], ub=[5], precision=1e-7)
    
    best_x, best_y = ga.run()
    
    print('best_x:', best_x, '\n', 'best_y:', best_y)

    return best_x, best_y


def opt_min_L(x):
    
    global var_L_G
    global var_L_P
    
    global G
    global P
    
    # input: GHPLC(0) GCOUNTER(T) GSET(T+1) BCOUNTER(T) B(T)-B(T-2) 
        
    # output: GHPLC(T+1) PDOHPLC(T+1)
    
    core_net = core_init(0)
    
    LX2 = LX1 + (x[0]*5)*2.1
    
    tmp_x = np.array([[LX0,LX1,LX2,LX3,LX4]])
    
    tmp_x = core_1_minMax_input.transform(tmp_x)
    
    tmp_x = torch.Tensor(tmp_x)
    
    tmp_x = torch.unsqueeze(tmp_x,dim=1)
    
    y = core_net(tmp_x).detach().numpy()
    
    G = core_1_minMax_output.inverse_transform(np.array([[y[0,0,0],y[0,0,1]]]))[0,0]
    
    P = core_1_minMax_output.inverse_transform(np.array([[y[0,0,0],y[0,0,1]]]))[0,1]
    
    core_net = core_init(0.1)
    
    result = (G-10)**2 + 50*(1/(P+1))**2
    
    print(G)
    
    print(P)


    return result


def opt_min_R(x):
    
    global var_R_G
    global var_R_P
    
    global G
    global P
    
    
    # input: GHPLC(0) GCOUNTER(T) GSET(T+1) BCOUNTER(T) B(T)-B(T-2) 
        
    # output: GHPLC(T+1) PDOHPLC(T+1)
    
    core_init(0)
    
    RX2 = RX1 + (x[0]*5)*(62/30)
    
    tmp_x = np.array([[RX0,RX1,RX2,RX3,RX4]])
    
    tmp_x = core_1_minMax_input.transform(tmp_x)
    
    tmp_x = torch.Tensor(tmp_x)
    
    tmp_x = torch.unsqueeze(tmp_x,dim=1)
        
    y = core_net(tmp_x).detach().numpy()
    
    G = core_1_minMax_output.inverse_transform(np.array([[y[0,0,0],y[0,0,1]]]))[0,0]
    
    P = core_1_minMax_output.inverse_transform(np.array([[y[0,0,0],y[0,0,1]]]))[0,1]
    
    core_init(0.1)
    
    result = (G-15)**2 + 50*(1/(P+1))**2
    


    return result

def data_loading():
    
    global train_x
    global train_y
    global test_x
    global test_y
    global proof_x
    global proof_y
    global core_1_minMax_input
    global core_1_minMax_output
    global core_2_minMax_input
    global core_2_minMax_output
    
    
    data = np.array(pd.read_excel('data_new.xlsx'))

    x = data[:,0:5] # without T
    y = data[:,6:8]
    
    
    core_1_minMax_input = MinMaxScaler()
    
    core_1_minMax_input.fit(x)
    
    
    
    core_1_minMax_output = MinMaxScaler()
    
    core_1_minMax_output.fit(y)
    


    data = np.array(pd.read_excel('data_new_new.xlsx'))
    
    x = data[:,0:4] # without T
    y = data[:,5:7]
    
    core_2_minMax_input = MinMaxScaler()
    
    core_2_minMax_input.fit(x)
    
    
    core_2_minMax_output = MinMaxScaler()
    
    core_2_minMax_output.fit(y)
    


def core_init(drop_out_rate):
    
    global core_net
    # global core
    
    class core(nn.Module):
        
        def __init__(self):
            
            super(core, self).__init__()
            
            self.layer1 = nn.Linear(5, 60)
            
            self.layer2 = nn.Linear(60, 60)
            
            self.layer3 = nn.Linear(60, 60)
            
            self.layer4 = nn.Linear(60, 60)
                        
            self.layer5 = nn.Linear(60, 60)
            
            self.layer6 = nn.Linear(60, 60)
            
            self.layer7 = nn.Linear(60, 60)
            
            self.layer8 = nn.Linear(60, 60)

            self.layer9 = nn.Linear(60, 2)
    
    
        def forward(self, x):
    
            x1 = F.relu(self.layer1(x))
            
            x2 = F.relu(self.layer2(x1))
            
            x3 = F.relu(self.layer3(x2))
            
            x4 = F.relu(self.layer4(x3))
    
            x5 = F.relu(self.layer5(x4))
            
            x6 = F.relu(self.layer6(x5))
            
            x7 = F.relu(self.layer7(x6))
    
            x8 = F.relu(self.layer8(x7))

    
            
            output = self.layer9(x8)        
    
            return output

    
    core_net = core()

    core_net.load_state_dict(torch.load(path + '\\final_core.pth.tar', map_location='cpu'))
    
    # net.cuda()
    
    # net.cpu()
    
    return core_net




def core_init2():
    
    global core_net2
    # global core2
    
    
    class core2(nn.Module):
        
        def __init__(self):
            super(core2, self).__init__()
            
            self.layer1 = nn.Linear(4, 80)
            
            self.layer2 = nn.Linear(80, 80)
            
            self.layer3 = nn.Linear(80, 80)
            
            self.layer4 = nn.Linear(80, 80)
                        
            self.layer5 = nn.Linear(80, 2)
    
    
        def forward(self, x):
    
            x1 = F.relu(self.layer1(x))
            
            x2 = F.relu(self.layer2(x1))
            
            x3 = F.relu(self.layer3(x2))
            
            x4 = F.relu(self.layer4(x3))
            
            output = self.layer5(x4)        
    
            return output

        
    core_net2 = core2()

    core_net2.load_state_dict(torch.load(path + '\\final_core2.pth.tar', map_location='cpu'))
    
    # net.cuda()
    
    # net.cpu()
    
    return core_net2

class CNN(nn.Module):

    def __init__(self):

        super(CNN, self).__init__()

        self.conv1 = nn.Sequential(nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1, padding=2,),
                                   nn.ReLU(), nn.MaxPool2d(kernel_size=2),)

        self.conv2 = nn.Sequential(nn.Conv2d(16, 32, 5, 1, 2), nn.ReLU(), nn.MaxPool2d(2),)

        self.out = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):

        x = self.conv1(x)

        x = self.conv2(x)

        x = x.view(x.size(0), -1)

        output = self.out(x)

        return output

def cnn_init():
    
    global cnn_net
    
    cnn_net = CNN()
    
    cnn_net.load_state_dict(torch.load( path + '\\final_mnist.pth.tar',map_location='cpu'))
    
    # net.cuda()
    
    # net.cpu()
    
    return cnn_net
    

def img_reading_gray(path):
    
    img = cv2.imread(path)
    
    gray_img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        
    return gray_img


def img_bindary(img,trend=60):
    
    _ , bindary_gray = cv2.threshold( img , trend, 255, cv2.THRESH_BINARY)
        
    return bindary_gray


def on_off_check(img,function):
    
    # x y reverse comparing to ImageLabelling
    
    function_table_x = {
    
    'acid':[284, 300],
    'baset':[331, 348],
    'folet':[379, 396],
    'subst':[428, 444],
    
    }
    
    function_table_y = {
    
    'acid':[160, 201],
    'baset':[162, 201],
    'folet':[162, 201],
    'subst':[162, 201],
    
    }
    
    area = img[function_table_x[function][0]:function_table_x[function][1],
               function_table_y[function][0]:function_table_y[function][1]]
    
    return area
    
    
def speed_img_get(img,function):
        
    # x y reverse comparing to ImageLabelling
    
    function_table_x = {
    
    'acid':[284, 300],
    'baset':[331, 348],
    'folet':[379, 396],
    'subst':[427, 444],
    
    }

    function_table_y = {
    
    'acid':[160, 182],
    'baset':[160, 181],
    'folet':[162, 181],
    'subst':[160, 181],
    
    }
        
    area = img[function_table_x[function][0]:function_table_x[function][1],
               function_table_y[function][0]:function_table_y[function][1]]
    
    return area    

def counter_img_get(img,function):
    
    # x y reverse comparing to ImageLabelling
    
    function_table_x = {
    
    'acid':[301, 326],
    'baset':[349, 373],
    'folet':[397, 422],
    'subst':[445, 470],
    'stirr':[120, 145],
    'temp':[206, 229],
    'ph':[253, 277],
    
    }
    
    function_table_y = {
    
    'acid':[65, 114],
    'baset':[65, 115],
    'folet':[65, 115],
    'subst':[65, 115],
    'stirr':[564, 605],
    'temp':[661, 697],
    'ph':[660, 698],
    
    }
        
    area = img[function_table_x[function][0]:function_table_x[function][1],
               function_table_y[function][0]:function_table_y[function][1]]
    
    return area

def area_divid_cnn_check(area, ):
    
    plt.imshow(area)
    plt.show()
    
    # global cut_y_direaction
    # global bound_y_begin
    # global bound_y_end
        
    bound_y_begin = []
    bound_y_end = []
    
    mark = 0
    
    for i in range(area.shape[1]):
        
        if mark == 0:
            
            if False in (area[:,i] == 255):
                            
                bound_y_begin.append(i)
                
                mark = 1
            
        else:
            
            if not(False in (area[:,i] == 255)):
                
                bound_y_end.append(i)
                
                mark = 0
    
    if len(bound_y_begin) != len(bound_y_end):
        
        bound_y_end.append(i)
    
    
    cut_y_direaction = []
    
    # avoiding the edge
    
    for i in range(len(bound_y_begin)):
        
        cut_y_direaction.append(area[:,bound_y_begin[i]:bound_y_end[i]])
    
    
    cut_final = []
    
    for i in cut_y_direaction:
        
        bound_x_begin = []
        bound_x_end = []
                
        mark = 0
        
        for j in range(i.shape[0]):
            
            if mark == 0:
                
                if False in (i[j,:] == 255):
                                
                    bound_x_begin.append(j)
                    
                    mark = 1
                
            elif mark == 1:
                
                if not(False in (i[j,:] == 255)):
                    
                    bound_x_end.append(j)
                    
                    mark = 0
        

        
        for j in range(len(bound_x_begin)):
            
            cut_final.append(i[bound_x_begin[j]:bound_x_end[j],:])

    cnn_check = []

    real_number = []
    
    for i in cut_final:
        
        if i.shape[0] < 3 and i.shape[1] < 3:
            
            cnn_check.append(0)
            
            real_number.append('.')
        
        else:
            
            cnn_check.append(1)
            
            real_number.append('fuck')
        
    
    return cut_final, cnn_check, real_number
        

def padding_28_28(img):
    
    img = -img + 255
    
    final_img = np.zeros([28,28],dtype='uint8')
    
    a = img.shape[0]
    
    b = img.shape[1]
    
    
    if a >= b:
        
        img_resize = cv2.resize(img, (int((20/a)*b),20))
        
        final_img[int(final_img.shape[0]/2-img_resize.shape[0]/2):int(final_img.shape[0]/2-img_resize.shape[0]/2) + img_resize.shape[0], 
                  int(final_img.shape[1]/2-img_resize.shape[1]/2):int(final_img.shape[1]/2-img_resize.shape[1]/2) + img_resize.shape[1]] = img_resize
    
    elif a < b:
        
        img_resize = cv2.resize(img, (20,int((20/b)*a)))
        
        final_img[int(final_img.shape[0]/2-img_resize.shape[0]/2):int(final_img.shape[0]/2-img_resize.shape[0]/2) + img_resize.shape[0],
                  int(final_img.shape[1]/2-img_resize.shape[1]/2):int(final_img.shape[1]/2-img_resize.shape[1]/2) + img_resize.shape[1]] = img_resize
        
    
    return final_img/255



def mnist(net,img_list, cnn_check, real_number):
    
    # global mnist_img
    
    mnist_img = []
    
    for i in range(len(cnn_check)):
        
        if cnn_check[i] == 1:
            
            mnist_img.append(padding_28_28(img_list[i]))
    
    mnist_img = torch.Tensor(np.array(mnist_img)).unsqueeze(dim=1)
    
    predict_result = torch.max(net(mnist_img),1)[1].numpy().tolist()
    
    for i in range(len(cnn_check)):
        
        if cnn_check[i] == 1:
            
            real_number[i] = str(predict_result[0])
            
            del predict_result[0]
    
    number = ''
    
    for i in real_number:
        
        number += i
    
    number = float(number)
    
    return number
    
def rt_speed_reading(net, path, function):
    
    mm = area_divid_cnn_check(img_bindary(speed_img_get(img_reading_gray(path),function)))
    
    num = mnist(net,mm[0],mm[1],mm[2])
    
    return num


def rt_counter_reading(net, path, function):
    
    # global mm
    
    # Bug_repairing
    
    mm = area_divid_cnn_check(img_bindary(counter_img_get(img_reading_gray(path),function)))
    
    num = mnist(net,mm[0],mm[1],mm[2])
    
    return num

def off_line(path,function):
    
    os.chdir(path)
    
    files = os.listdir()
    
    files.sort()
    
    data = []
    
    for i in files:
        
        data.append(rt_counter_reading(i, function))
    
    plt.plot(data)
    
    plt.show()
    
    return np.array(data)



def get_hwnd():
    
    
    handle_left = 0
    
    handle_right = 0
    
    right = 'PC-Panel 礑CU - right - 10.50.131.37 [full access]'

    left = 'PC-Panel 礑CU - left - 10.50.129.29 [full access]'

    hwnd_title = dict()
    
    def get_all_hwnd(hwnd,mouse):
        
      if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
     
    win32gui.EnumWindows(get_all_hwnd, 0)
    
      
    for h,t in hwnd_title.items():
        
      if t != "":
          
          # print(h, t)
          
          if t == right:
              
              handle_right = h
          
          if t == left:
              
              handle_left = h
    
    
    return handle_left, handle_right

def show_postion(hwnd):
    
    rect = win32gui.GetWindowRect(hwnd)
    
    x = rect[0]
    
    y = rect[1]
    
    w = rect[2] - x
    
    h = rect[3] - y
    
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    
    print("\tLocation: (%d, %d)" % (x, y))
        
    print("\t    Size: (%d, %d)" % (w, h))
    
    return x,y

def recover_position():
    
    handle_left, handle_right = get_hwnd()
    
    left_x, left_y = show_postion(handle_left)
    
    right_x, right_y = show_postion(handle_right)
            
    # left

    shell = win32com.client.Dispatch("WScript.Shell")
    
    shell.SendKeys('%')    
    
    win32gui.SetForegroundWindow(handle_left)
    
    click_position_x = left_x + 400
    
    click_position_y = left_y + 10
    
    pyautogui.moveTo(click_position_x, click_position_y, duration = 0.5)
    
    pyautogui.mouseDown()
    
    pyautogui.moveRel(-left_x, -left_y, duration = 2)
    
    pyautogui.mouseUp()

    #right
    
    shell = win32com.client.Dispatch("WScript.Shell")
    
    shell.SendKeys('%')
    
    win32gui.SetForegroundWindow(handle_right)
    
    click_position_x = right_x + 400
    
    click_position_y = right_y + 10
    
    pyautogui.moveTo(click_position_x, click_position_y, duration = 0.5)
    
    pyautogui.mouseDown()
    
    pyautogui.moveRel(-right_x, -right_y, duration = 2)
    
    pyautogui.mouseUp()



def control_panel_location(handle):
    
    shell = win32com.client.Dispatch("WScript.Shell")
    
    shell.SendKeys('%')    
    
    win32gui.SetForegroundWindow(handle)
    
    x, y = show_postion(handle)
    
    control_panel_x = x + 20
    
    control_panel_y = y + 600
    
    pyautogui.moveTo(control_panel_x, control_panel_y, duration = 0.5)
    
    pyautogui.click()
    
    
def trend_plot_location(handle):

    shell = win32com.client.Dispatch("WScript.Shell")
    
    shell.SendKeys('%')    
    
    win32gui.SetForegroundWindow(handle)
    
    x, y = show_postion(handle)
    
    trend_plot_x = x + 150
    
    trend_plot_y = y + 600
    
    pyautogui.moveTo(trend_plot_x, trend_plot_y, duration = 0.5)
    
    pyautogui.click()

def screen(time,handle,ID):

    shell = win32com.client.Dispatch("WScript.Shell")
    
    shell.SendKeys('%')    
    
    win32gui.SetForegroundWindow(handle)
    
    hwnd = handle
    
    app = QApplication(sys.argv)
    
    screen = QApplication.primaryScreen()
    
    img = screen.grabWindow(hwnd).toImage()
    
    img.save(str(time)+ '_' + ID + ".jpg")


def function_click(handle, function):
    
    #without edge
        
    function_table = {
        
        'acid':[44, 297],
        'baset':[39, 354],
        'folet':[36, 398],
        'subst':[45, 446],
        'stirr':[537, 126],
        'temp':[756, 206],
        'ph':[755, 252],
        
        }
    
    x, y = show_postion(handle)
    
    pyautogui.moveTo(x + 3 + function_table[function][0], y + 25 + function_table[function][1], duration = 0.5)
    
    pyautogui.click()
    
        
def switch_click(handle, function):
        
    #without edge
    
    switch_table = {
        
        'acid':[177, 290],
        'baset':[178, 339],
        'folet':[179, 387],
        'subst':[176, 434],
        
        }
    
    x, y = show_postion(handle)
    
    pyautogui.moveTo(x + 3 + switch_table[function][0], y + 25 + switch_table[function][1], duration = 0.5)
    
    pyautogui.click()

    
def switch_on_off_auto(handle, state):
    
    #with edge
        
    on_off_table = {
        
        'off':[357, 279],
        'on':[358, 334],
        'auto':[358, 386],
        'ok':[446, 467],
        
        }
    
    x, y = show_postion(handle)
    
    pyautogui.moveTo(x + on_off_table[state][0], y + on_off_table[state][1], duration = 0.5)
    
    pyautogui.click()
    
    pyautogui.moveTo(x + on_off_table['ok'][0], y + on_off_table['ok'][1], duration = 0.5)
    
    pyautogui.click()

    
def number_panel(handle, num):
    
    #with edge
    
    number_table = {
        
        
        '0':[316, 427],
        '1':[267, 374],
        '2':[313, 378],
        '3':[362, 377],
        '4':[267, 325],
        '5':[314, 327],
        '6':[363, 328],
        '7':[267, 276],
        '8':[316, 274],
        '9':[365, 275],
        '.':[363, 426],
        'ok':[538, 483]        

        }
    
    x, y = show_postion(handle)
    
    number = str(num)
    
    for i in number:
        
        pyautogui.moveTo(x + number_table[i][0], y + number_table[i][1], duration = 0.5)
    
        pyautogui.click()
    
    pyautogui.moveTo(x + number_table['ok'][0], y + number_table['ok'][1], duration = 0.5)
    
    pyautogui.click()


    
def number_panel_on_off_auto(handle, state):
    
    #with edge
    
    on_off_table = {
        
        'on':[443, 275],
        'off':[446, 335],
        'auto':[442, 375],
        'ok':[542, 486],
                
        }
    
    x, y = show_postion(handle)
    
    pyautogui.moveTo(x + on_off_table[state][0], y + on_off_table[state][1], duration = 0.5)
    
    pyautogui.click()
    
    pyautogui.moveTo(x + on_off_table['ok'][0], y + on_off_table['ok'][1], duration = 0.5)
    
    pyautogui.click()


def main(LGHPLC0, RGHPLC0,LOD0, ROD0):
    
    # init
    
    global path
        
    global Time_points
    
    global L_B
    global L_G
    
    global R_B
    global R_G
    
    global LX0
    global LX1
    global LX2
    global LX3
    global LX4
    
    global RX0
    global RX1
    global RX2
    global RX3
    global RX4
    
    global begin_feed_L
    global begin_feed_R
    
    global goal_L
    global goal_R
    
    global Now_G_L_Rate
    global Now_G_R_Rate
    
    global handle_left
    global handle_right
    
    Now_G_L_Rate = 10
    
    Now_G_R_Rate = 10
    
    path = os.getcwd()
    
    Time_points = []
    
    L_B = []
    
    L_G = []
    
    R_B = []
    
    R_G = []
    
    begin_feed_L = 0
    
    begin_feed_R = 0
    
    cnn_init()
    
    core_init(0)
    
    core_init2()
    
    time_resoliton = 10 #unit:min
        
    # working flow
    
    handle_left, handle_right = get_hwnd()
    
    start_time = int(time.time())
    
    os.chdir('Chonpca')
    
    os.mkdir(str(start_time))
    
    os.chdir(str(start_time))
    
    start_time = int(time.time())
    
    recover_position()
    
    
    control_panel_location(handle_right)
    
    screen(start_time,handle_right,'right_control')
    
    trend_plot_location(handle_right)
    
    screen(start_time,handle_right,'right_trend')
    
    control_panel_location(handle_right)
    
    
    control_panel_location(handle_left)
    
    screen(start_time,handle_left,'left_control')
    
    trend_plot_location(handle_left)
    
    screen(start_time,handle_left,'left_trend')
    
    control_panel_location(handle_left)
    
    # input: GHPLC(0) GCOUNTER(T) GSET(T+1) BCOUNTER(T) B(T)-B(T-1) 
        
    # output: GHPLC(T+1) PDOHPLC(T+1)
        
    Time_points.append(start_time)
    
    LX0 = LGHPLC0

    LX1 = rt_counter_reading(cnn_net, str(start_time) + '_left_control.jpg', 'subst')*2.1
    
    LX2 = None
    
    LX3 = rt_counter_reading(cnn_net, str(start_time) + '_left_control.jpg', 'baset')*1
    
    LX4 = None
    
    L_G.append(LX1)
    
    L_B.append(LX3)
    
    
    RX0 = RGHPLC0
    
    RX1 = rt_counter_reading(cnn_net, str(start_time) + '_right_control.jpg', 'subst')*(62/30)
    
    RX2 = None
    
    RX3 = rt_counter_reading(cnn_net, str(start_time) + '_right_control.jpg', 'baset')*(31/50)
    
    RX4 = None
    
    R_G.append(RX1)
    
    R_B.append(RX3)
    
    # data upload
    
    while True:
                
        # recording
        
        now_time = int(time.time())
        
        if (now_time - start_time)%60 == 0:
            
            handle_left, handle_right = get_hwnd()
            
            recover_position()
            
            
            control_panel_location(handle_right)
    
            screen(now_time,handle_right,'right_control')
            
            trend_plot_location(handle_right)
            
            screen(now_time,handle_right,'right_trend')
            
            control_panel_location(handle_right)
            
            
            control_panel_location(handle_left)
            
            screen(now_time,handle_left,'left_control')
            
            trend_plot_location(handle_left)
            
            screen(now_time,handle_left,'left_trend')
            
            control_panel_location(handle_left)
            
            # data_collect
            
            if (now_time - start_time) <= 3700:
                
                # BEFORE 1H
                
                
                Time_points.append(now_time)
            
                LX0 = LGHPLC0
        
                LX1 = rt_counter_reading(cnn_net, str(now_time) + '_left_control.jpg', 'subst')*2.1
                
                LX2 = None
                
                LX3 = rt_counter_reading(cnn_net, str(now_time) + '_left_control.jpg', 'baset')*1
                
                LX4 = None
                
                L_G.append(LX1)
    
                L_B.append(LX3)

                
                RX0 = RGHPLC0
                
                RX1 = rt_counter_reading(cnn_net, str(now_time) + '_right_control.jpg', 'subst')*(62/30)
                
                RX2 = None
                
                RX3 = rt_counter_reading(cnn_net, str(now_time) + '_right_control.jpg', 'baset')*(31/50)
                
                RX4 = None
                
                R_G.append(RX1)
    
                R_B.append(RX3)

            
            else:
                
                # after 1H

                LX0 = LGHPLC0
        
                LX1 = rt_counter_reading(cnn_net, str(now_time) + '_left_control.jpg', 'subst')*2.1
                
                LX2 = None
                
                LX3 = rt_counter_reading(cnn_net, str(now_time) + '_left_control.jpg', 'baset')*1
                
                LX4 = None
                
                L_G.append(LX1)
    
                L_B.append(LX3)
                                
                    
                RX0 = RGHPLC0
                
                RX1 = rt_counter_reading(cnn_net, str(now_time) + '_right_control.jpg', 'subst')*(62/30)
                
                RX2 = None
                
                RX3 = rt_counter_reading(cnn_net, str(now_time) + '_right_control.jpg', 'baset')*(31/50)
                
                RX4 = None
    
                R_G.append(RX1)
    
                R_B.append(RX3)
                
                
                # X4_calculate
                
                files = os.listdir()
                
                file_exit_L = 0
                
                file_exit_R = 0
                
                for i in range(10):
                    
                    if file_exit_L == 0:
                        
                        L_file_T_minus_1 = str(now_time - 3600 - i*60) + '_left_control.jpg'
                        
                    
                        if L_file_T_minus_1 in files:
                            
                            file_exit_L = 1
                            
                            LX3_T_minus_1 = rt_counter_reading(cnn_net, L_file_T_minus_1, 'baset')*1
                            
                            LX4 = LX3 - LX3_T_minus_1
        
                    if file_exit_R == 0:
                        
                        R_file_T_minus_1 = str(now_time - 3600 - i*60) + '_right_control.jpg'
                                            
                        if R_file_T_minus_1 in files:
                            
                            file_exit_R = 1
                            
                            RX3_T_minus_1 = rt_counter_reading(cnn_net, R_file_T_minus_1, 'baset')*(31/50)
                            
                            RX4 = RX3 - RX3_T_minus_1
        
        # control        

        if begin_feed_R == 0:
            
            if  (now_time - start_time) > 4000:

                tmp_xx = np.array([[RX0,ROD0,RX3,RX4]])

                tmp_xx = core_2_minMax_input.transform(tmp_xx)
    
                tmp_xx = torch.Tensor(tmp_xx)
    
                tmp_xx = torch.unsqueeze(tmp_xx,dim=1)
                
                yy = core_net2(tmp_xx).detach().numpy()
                                
                RRX4 = core_2_minMax_output.inverse_transform(np.array([[yy[0,0,0],yy[0,0,1]]]))[0,0]
                                
                if RRX4 < 15:
                    
                    begin_feed_R = 1
                    
                    control_panel_location(handle_right)
                    
                    function_click(handle_right, 'subst')
                    
                    number_panel(handle_right, '10')
        
        if begin_feed_R == 1:
            
            if (now_time - start_time)%600 == 0:
                
                RX0 = RX0
                
                RX1 = RX1
                
                RX2 = RX1 + (Now_G_R_Rate*5)*(62/30)
                
                RX3 = RX3
                
                RX4 = RX4
                
                # input: GHPLC(0) GCOUNTER(T) GSET(T+1) BCOUNTER(T) B(T)-B(T-1) 
        
                # output: GHPLC(T+1) PDOHPLC(T+1)
                                                
                aaa = opt_R()
                
                Now_G_R_Rate = aaa[0][0]
                                
                control_panel_location(handle_right)
                
                function_click(handle_right, 'subst')
                
                number_panel(handle_right,str(Now_G_R_Rate)[0:4])



        
        if begin_feed_L == 0:
            
            if  (now_time - start_time) > 4000:
                
                tmp_xx = np.array([[LX0,LOD0,LX3,LX4]])
                
                tmp_xx = core_2_minMax_input.transform(tmp_xx)
    
                tmp_xx = torch.Tensor(tmp_xx)
    
                tmp_xx = torch.unsqueeze(tmp_xx,dim=1)
                
                yy = core_net2(tmp_xx).detach().numpy()

                LLX4 = core_2_minMax_output.inverse_transform(np.array([[yy[0,0,0],yy[0,0,1]]]))[0,0]
                                
                if LLX4 < 15:
                    
                    begin_feed_L = 1
                    
                    control_panel_location(handle_left)
                    
                    function_click(handle_left, 'subst')
                    
                    number_panel(handle_left, '10')
                    
        if begin_feed_L == 1:
            
            if (now_time - start_time) % (time_resoliton*60) == 0:
                
                LX0 = LX0
                
                LX1 = LX1
                
                LX2 = LX1 + (Now_G_L_Rate*5)*2.1
                
                LX3 = LX3
                
                LX4 = LX4
                
                
                # input: GHPLC(0) GCOUNTER(T) GSET(T+1) BCOUNTER(T) B(T)-B(T-1) 
        
                # output: GHPLC(T+1) PDOHPLC(T+1)
                                
                aaa = opt_L()
                
                Now_G_L_Rate = aaa[0][0]
                                
                control_panel_location(handle_left)
                
                function_click(handle_left, 'subst')
                
                number_panel(handle_left,str(Now_G_L_Rate)[0:4])
                
        



data_loading()

main(44,44,0.290,0.242)