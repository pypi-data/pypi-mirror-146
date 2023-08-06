
import matplotlib.pyplot as plt
from fvNet14 import *


def plot_loss(hist,height, width):
  '''
  Plots the model accuracy

  args:
      hist = model history
      height = plot height
      width = plot width
  
  e.g: plot_accuracy(history, 10, 10)
  
  dependency module:
      matplotlib
  '''
  plt.figure(figsize = (height, width))
  train_loss = hist.history['loss']
  val_loss = hist.history['val_loss']
  epochs = range(1, len(train_loss) + 1)
  plt.plot(epochs, train_loss, 'b', label='Training loss')
  plt.plot(epochs, val_loss, 'r', label='Validation loss')
  plt.title('fvNet14 - Training and Validation loss')
  plt.xlabel("Number of Epochs")
  plt.ylabel("Loss")
  plt.legend()
  plt.grid()
 
