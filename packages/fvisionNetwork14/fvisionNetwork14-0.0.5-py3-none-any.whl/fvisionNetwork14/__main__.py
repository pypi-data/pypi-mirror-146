'''
@auther : Kalyan Mohanty
pip install fvisionNetwork14

version: 1.9.2
modules:
        - image_preprocessing
        - fvNet14
        - plot_accuracy
        - plot_loss
        
Dependancy modules:
        - numpy
        - from tensorflow
        - matplotlib

    
 
'''

# import os
# import numpy as np
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.preprocessing import image
# import matplotlib.pyplot as plt
from fvNet14 import *
from image_pre_processing import *
from plot_model_acuracy import *
from plot_model_loss import *

# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.preprocessing import image

def display_welcome_message():
    print('Welcome to fvisionNetwork14')

def main():
    display_welcome_message()


if __name__ == '__main__':
    main()