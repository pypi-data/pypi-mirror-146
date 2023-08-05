from PyQt5 import QtWidgets, QtCore
import sys
from shutil import copyfile

from select_p import Ui_MainWindow as Ui1
from suspect_p1 import Ui_MainWindow as Ui2
from suspect_p2 import Ui_MainWindow as Ui3
from lastphoto import Ui_MainWindow as Ui4

import algo_genetique as ag
import common_functions as cf
import neural_network_function as nn

import numpy as np
import random
import matplotlib.pyplot as plt  # plotting routines
import keras
from keras.models import Model  # Model type to be used
from keras.layers.core import Dense, Dropout, Activation  # Types of layers to be used in our model
from keras.utils import np_utils  # NumPy related tools
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd

import os
import glob

import logging

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


#Suspect screening page initialisation
class mywindow(QtWidgets.QMainWindow, Ui1):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

#Suspect picture selection page 1 initialisation
class mywindow2(QtWidgets.QMainWindow, Ui2):
    def __init__(self):
        super(mywindow2, self).__init__()
        self.setupUi2(self)

#Suspect picture selection page 2 initialisation
class mywindow3(QtWidgets.QMainWindow, Ui3):
    def __init__(self):
        super(mywindow3, self).__init__()
        self.setupUi(self)

#Return suspect photo page initialization
class mywindow4(QtWidgets.QMainWindow, Ui4):
    def __init__(self):
        super(mywindow4, self).__init__()
        self.setupUi(self)

#Multi-page dedicated page system

class Controller():
    def __init__(self):
        pass

    def show_select(self):
        self.login = mywindow()
        self.login.switch_window.connect(self.show_main)
        # self.window_three = mywindow4()
        if cycle >=1:
            self.window_three.close()
        if restart:
            self.window_two.close()
        self.login.show()

    def show_main(self):
        self.window = mywindow2()
        self.window.switch_window.connect(self.show_window_two)
        self.login.close()
        self.window.show()

    def show_window_two(self):
        self.window_two = mywindow3()
        self.window.close()
        if cycle >=1:
            self.window_three.close()
        self.window.switch_window.connect(self.show_window_two)
        self.window_two.switch_window2.connect(self.show_window_lastphoto)
        self.window_two.switch_window3.connect(self.show_select)
        global restart
        restart = True
        self.window_two.show()

    def show_window_lastphoto(self):
        self.window_three = mywindow4()
        self.window_two.close()
        self.window_three.switch_window.connect(self.show_select)
        self.window_three.switch_window2.connect(self.show_window_two)
        global cycle
        cycle +=1
        self.window_three.show()


if __name__ == "__main__":

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    #Page initialisation
    cycle = 0
    restart = False
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QWidget()
    latout = QtWidgets.QHBoxLayout()
    main.setLayout(latout)

    #Generate a multi-page selection system, initialise it and show it
    controller = Controller()
    controller.show_select()
    sys.exit(app.exec_())
