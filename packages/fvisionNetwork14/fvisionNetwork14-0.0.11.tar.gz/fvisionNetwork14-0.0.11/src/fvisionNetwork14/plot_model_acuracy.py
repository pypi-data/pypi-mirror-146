import matplotlib.pyplot as plt

def plot_accuracy(hist,height,width):
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
  train_acc = hist.history['accuracy']
  val_acc = hist.history['val_accuracy']
  train_loss = hist.history['loss']
  val_loss = hist.history['val_loss']
  epochs = range(1, len(train_acc) + 1)
  plt.plot(epochs, train_acc, 'b', label='Training accurarcy')
  plt.plot(epochs, val_acc, 'r', label='Validation accurarcy')
  plt.title('fvNet14 - Training and Validation accurarcy')
  plt.xlabel("Number of Epochs")
  plt.ylabel("Accuracy")
  plt.grid()
  plt.legend()

  
if __name__ == '__main__':
    plot_accuracy()