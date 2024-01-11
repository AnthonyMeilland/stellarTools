# -*- coding: utf-8 -*-
"""
*******************************************************************************

Created on Thu Jan 28 09:54:52 2021

@author: Anthony Meilland

This module contains the class genevaStar that return evolutionary tracks for 
stars using data from the Geneva evolutionnary code found at on their website
https://www.unige.ch/sciences/astro/evolution/en/database/file-formats

"""

import numpy as np
import math
from scipy import interpolate
from stellarTools import kurucz as kz
import os

path = os.path.abspath(__file__)
dir0 = os.path.dirname(path)
dirmodel=dir0+"geneva_data"

class typicalStar:

    def __init__(self,Mass):
        pass
    
    
    def _getListOfMass(self):
        filenames=[os.listdir(dirmodel)
        