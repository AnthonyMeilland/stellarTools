# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 09:08:55 2025

@author: ame
"""

from matplotlib.colors import LinearSegmentedColormap
import numpy as np


def temperatureColor(temp):
    with np.errstate(invalid = 'ignore', divide = 'ignore'):
        temp = temp / 100
        r = (temp<=66)*255 + (temp>66)*np.clip(np.nan_to_num(329.698727446*np.power((temp-60),-0.1332047592),0),0,np.inf)
        
        g = (temp<66)* np.clip(np.nan_to_num(99.4708025861 * np.log(temp) - 161.1195681661,0),0,np.inf)+ \
            (temp>=66)* np.clip(np.nan_to_num(288.1221695283 * np.power((temp - 60), -0.0755148492),0),0,np.inf)
            
        b = (temp>=65)*255 + ((temp<65) & (temp>=10))*\
            np.clip(np.nan_to_num(138.5177312231 * np.log(temp - 10) - 305.0447927307,0),0,np.inf)
    
        return np.clip(np.transpose(np.array([r/255, g/255, b/255])),0,1)



_colortempFake = np.array([[0.,0,0],#0
                      [1,0,0],# 2000
                      [1,0.8,0],#4000
                      [1,1,0.5],#6000
                      [1,1,1],#8000
                      [0.9,0.9,1],#10000
                      [0.8,0.8,1],#12000                      
                      [0.7,0.7,1],#14000 
                      [0.6,0.6,1],#16000 
                      [0.5,0.5,1],#18000     
                      [0.4,0.4,1]])#20000  
    
_tempFake =np.arange(0,22000,2000)

def temperatureColorFake(temp):
    R = np.interp(temp,_tempFake,_colortempFake[:,0])
    G = np.interp(temp,_tempFake,_colortempFake[:,1])
    B = np.interp(temp,_tempFake,_colortempFake[:,2])    
    return np.transpose(np.array([R,G,B]))


_temp = np.linspace(0,20000,num=256)
_colortemp=temperatureColor(_temp)
temperatureColorMap = LinearSegmentedColormap.from_list("temp", _colortemp)

temperatureColorMapFake = LinearSegmentedColormap.from_list("tempFake", _colortempFake)

