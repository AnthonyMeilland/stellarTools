# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:13:43 2013

@author: ame
"""

from distutils.core import setup

setup(name='stellarTools',
      version='1.2',
      description='Stellar Tools Package',
      author='Anthony Meilland',
      author_email='ame@oca.eu',
      url='',
      packages=['stellarTools'],
      package_data={'stellarTools':['kurucz_data/*','misc_data/*','geneva_data/*']})
