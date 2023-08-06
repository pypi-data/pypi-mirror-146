import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models,layers
from tensorflow.keras.layers import LeakyReLU

def fvNet14(image_height, image_width, color_channel, output_layer):
    '''
    fvNet14(image_height = None, image_width = None, color_channel = None, output_layer = None)
    args:
        image_height = input image height
        image_width = input image width   
        color_channel = number of color channels
        output_layer = number of output layers in the model
    
    e.g:
        image_height = 50
        image_width = 50
        color_channel = 3
    
    model_test = fvNet14(image_height = 50, image_width = 50, color_channel = 3, output_layer = 10)
    model_test.fit(xtrain,ytrain,epochs=50,validation_data=(xtest,ytest))
    
    - fvNet14 is a 14 layer sequential model having six convolutional 2D layers of filters 64, 128, 256.
    - Leaky Relu is the activation function used in the model.
    - Max pooling layer of pool size (2,2).
    - Two dense layer 180 and 100 is present in the network.
    - Model uses a Dropout rate of 0.2

    dependency module:
        tensorflow   
    '''
    model = models.Sequential()
    model.add(layers.Conv2D(64,(3,3),input_shape=(image_height, image_width,color_channel),activation=LeakyReLU(alpha=0.01)))
    model.add(layers.Conv2D(64,(3,3),activation=LeakyReLU(alpha=0.01)))
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Conv2D(128,(3,3),activation=LeakyReLU(alpha=0.01)))
    model.add(layers.Conv2D(128,(3,3),activation=LeakyReLU(alpha=0.01)))
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Conv2D(256,(3,3),activation=LeakyReLU(alpha=0.01)))
    model.add(layers.Conv2D(256,(3,3),activation=LeakyReLU(alpha=0.01)))
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Flatten())
    model.add(layers.Dense(180,activation=LeakyReLU(alpha=0.01)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(100,activation=LeakyReLU(alpha=0.01)))
    model.add(layers.Dense(output_layer,activation='softmax'))
    return model
if __name__ == '__main__':
    fvNet14()