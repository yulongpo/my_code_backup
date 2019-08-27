# -*- coding: utf-8 -*-

from keras.models import Model
from keras.layers import Input
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
from keras.layers import BatchNormalization
from keras.layers import LeakyReLU
from keras.layers import Concatenate
from keras.layers import UpSampling1D
from keras.layers import Lambda
from keras.optimizers import Adam

import tensorflow as tf
import keras.backend as K


def band_conv(x_in, x_concat=None, filters=32, kernel_size=3, 
              layer_num=1, inner_num=1):
    """simple conv with BN"""
    x = Conv1D(filters=filters, 
               kernel_size=kernel_size,
               padding="same", 
               kernel_initializer="he_normal", 
               name="b{}_c{}".format(layer_num, inner_num))(x_in)
    
    x = BatchNormalization(name="b{}_bn{}".format(layer_num, inner_num))(x)  # BN
    x = LeakyReLU(0.1, name="b{}_lrelu{}".format(layer_num, inner_num))(x)  # Leaky Relu
    
    if x_concat is not None:
        x = Lambda(concat, arguments={"x_concat":x_concat})(x)
        x = Concatenate(name="b{}_concat".format(layer_num))([x, x_concat])
        
    return x


def concat(x, x_concat):
    """
    
    """
    diff = K.shape(x_concat)[1] - K.shape(x)[1]
    x = K.temporal_padding(x, padding=(diff//2, diff-diff//2))    
    return x
    

def band_conv_down(x_in, layer_num=1, inner_num=1):
    """normal conv with maxpool"""
    x = Conv1D(32, 3, 
               padding="same", 
               kernel_initializer="he_normal", 
               name="b{}_c{}".format(layer_num, inner_num))(x_in)
    
    x = BatchNormalization(name="b{}_bn{}".format(layer_num, inner_num))(x)  # BN
    x = LeakyReLU(0.1, name="b{}_lrelu{}".format(layer_num, inner_num))(x)
    p = MaxPooling1D(name="b{}_p".format(layer_num))(x)
    
    return p
    
def band_conv_up(x_in, x_concat=None, layer_num=9):
    """normal conv with upsampling"""
#    x = Conv1D(32, 3, 
#               padding="same", 
#               kernel_initializer="he_normal", 
#               name="b{}_c1".format(layer_num))(x_in)
#    
#    x = BatchNormalization(name="b{}_bn1".format(layer_num))(x)  # BN
#    x = LeakyReLU(0.1, name="b{}_lrelu1".format(layer_num))(x)
#    
#    if x_concat is not None:
#        x = Concatenate(name="b{}_concat".format(layer_num))([x, x_concat])
#        
#    x = Conv1D(32, 3, padding="same", 
#               kernel_initializer="he_normal", 
#               name="b{}_c2".format(layer_num))(x)
#    
#    x = BatchNormalization(name="b{}_bn2".format(layer_num))(x)  # BN
#    x = LeakyReLU(0.1, name="b{}_lrelu2".format(layer_num))(x)
    x = band_conv(x_in, x_concat=x_concat, layer_num=layer_num, inner_num=1,
                  filters=32, kernel_size=3,)
    x = band_conv(x, layer_num=layer_num, inner_num=2,
                  filters=32, kernel_size=3)
    up = UpSampling1D(name="b{}_up".format(layer_num))(x)
    
    return up
    

def band_net(input_length=8192):
    """band net wrapper"""
    inputs = Input((input_length, 1), name="inputs")    # 8192 * 1
    x_in = band_conv(inputs, layer_num=1, inner_num=1)  # 8192 * 32
    x1   = band_conv_down(x_in, layer_num=1, inner_num=2)    # 4096 * 32
    x2   = band_conv_down(x1, layer_num=2)      # 2048 * 32
    x3   = band_conv_down(x2, layer_num=3)      # 1024 * 32
    x4   = band_conv_down(x3, layer_num=4)      # 512 * 32
    x5   = band_conv_down(x4, layer_num=5)      # 256 * 32
    x6   = band_conv_down(x5, layer_num=6)      # 128 * 32
    x7   = band_conv_down(x6, layer_num=7)      # 64 * 32
    
    x8   = band_conv_up(x7, layer_num=8)        # 128 * 32
    x9   = band_conv_up(x8, x6, layer_num=9)    # 256 * 32
    x10  = band_conv_up(x9, x5, layer_num=10)   # 512 * 32
    x11  = band_conv_up(x10, x4, layer_num=11)  # 1024 * 32
    x12  = band_conv_up(x11, x3, layer_num=12)  # 2048 * 32
    x13  = band_conv_up(x12, x2, layer_num=13)  # 4096 * 32
    x14  = band_conv_up(x13, x1, layer_num=14)  # 8192 * 32
    x15  = band_conv(x14, x_concat=x_in, layer_num=15)  # 8192  * 64
    x15  = band_conv(x15, layer_num=15, inner_num=2)    # 8192 * 32
    x15  = band_conv(x15, layer_num=15, inner_num=3)    # 8192 * 32
    
    x16  = band_conv(x15, filters=2, kernel_size=3,
                     layer_num=16, inner_num=1)         # 8192 * 2
    
    x16 = Conv1D(1, 1, padding="same", 
                 activation="sigmoid", name="b16_c2")(x16)  # 8192 * 1
    
    model = Model(inputs=inputs, outputs=x16)
    model.compile(optimizer = Adam(lr = 1e-4), 
                  loss = 'binary_crossentropy', metrics = ['accuracy'])
    
    return model
    

def band_net_v(input_length=None):
    """band net wrapper"""
    inputs = Input((input_length, 1), name="inputs")    # 8192 * 1
    x_in = band_conv(inputs, layer_num=1, inner_num=1)  # 8192 * 32
    x1   = band_conv_down(x_in, layer_num=1, inner_num=2)    # 4096 * 32
    x2   = band_conv_down(x1, layer_num=2)      # 2048 * 32
    x3   = band_conv_down(x2, layer_num=3)      # 1024 * 32
    x4   = band_conv_down(x3, layer_num=4)      # 512 * 32
    x5   = band_conv_down(x4, layer_num=5)      # 256 * 32
    x6   = band_conv_down(x5, layer_num=6)      # 128 * 32
    x7   = band_conv_down(x6, layer_num=7)      # 64 * 32
    
    x8   = band_conv_up(x7, layer_num=8)        # 128 * 32
    x9   = band_conv_up(x8, x6, layer_num=9)    # 256 * 32
    x10  = band_conv_up(x9, x5, layer_num=10)   # 512 * 32
    x11  = band_conv_up(x10, x4, layer_num=11)  # 1024 * 32
    x12  = band_conv_up(x11, x3, layer_num=12)  # 2048 * 32
    x13  = band_conv_up(x12, x2, layer_num=13)  # 4096 * 32
    x14  = band_conv_up(x13, x1, layer_num=14)  # 8192 * 32
    x15  = band_conv(x14, x_concat=x_in, layer_num=15)  # 8192  * 64
    x15  = band_conv(x15, layer_num=15, inner_num=2)    # 8192 * 32
    x15  = band_conv(x15, layer_num=15, inner_num=3)    # 8192 * 32
    
    x16  = band_conv(x15, filters=2, kernel_size=3,
                     layer_num=16, inner_num=1)         # 8192 * 2
    
    x16 = Conv1D(1, 1, padding="same", 
                 activation="sigmoid", name="b16_c2")(x16)  # 8192 * 1
    
    model = Model(inputs=inputs, outputs=x16)
    model.compile(optimizer = Adam(lr = 1e-4), 
                  loss = 'binary_crossentropy', metrics = ['accuracy'])
    
    return model

    
if __name__ == "__main__":
#    import tensorflow as tf
    import numpy as np
    
    in_length = 25288
    data = np.random.randn(in_length)

    data[1000:2000] += 8 + np.random.rand(1000)
    data[-2000:-300] += 10 + np.random.rand(1700)
    data = (data - np.min(data))/(np.max(data) - np.min(data))
    data = np.reshape(data, (1, in_length, 1))
    
    with tf.device("/cpu:0"):
        model = band_net(input_length=None)
        model.load_weights("../models/true_best_v5.1.h5", by_name=True)
        
        pred = model.predict(data)
    
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 8))
    plt.plot(data.flatten())
    plt.plot(pred.flatten())
        
        
#        model.summary()
#        model.load_weights("../models/mix_best_8192.h5", by_name=True)
#        print("succcessful!")