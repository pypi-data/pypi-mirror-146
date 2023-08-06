import os
import numpy as np
import tensorflow
import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image

def image_preprocessing( path, image_height, image_width):
  '''
  args:
      path = dataset path
      image_height = input image height
      image_width = input image width

  e.g:
      image_preprocessing(path, 50, 50)

  image_array = image converted to numpy array
  class_label =  class names(categorical)

  dependency module:
    tensorflow


  '''

  class_names = os.listdir(path)
  print("Name of the classes \n", class_names)
  images = []
  image_preprocessing.image_array = []
  image_preprocessing.class_label = []
  for folder in class_names:
    files = os.listdir(path + folder)
    for file in files:
      img = image.load_img(path + folder+"/"+file,target_size=(image_height, image_width))
      images.append(img)
      img = image.img_to_array(img)
      image_preprocessing.image_array.append(img)
      image_preprocessing.class_label.append(class_names.index(folder))
  image_preprocessing.image_array = np.array(image_preprocessing.image_array)
  image_preprocessing.class_label = np.array(image_preprocessing.class_label)
  print('Shape of image array: ',image_preprocessing.image_array.shape)
  print('Shape of class label before converting to categorical: ',image_preprocessing.class_label.shape)
  image_preprocessing.class_label = to_categorical(image_preprocessing.class_label)
  print('Class Names Converted to categorical:',image_preprocessing.class_label.shape)
  image_preprocessing.image_array = image_preprocessing.image_array/255

  
if __name__ == '__main__':
    image_preprocessing()