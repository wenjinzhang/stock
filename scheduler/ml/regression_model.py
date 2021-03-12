from keras.models import Sequential
from keras import layers

def LSTM(input_shape = (1, 1)):
    LSTM = Sequential()
    LSTM.add(layers.LSTM(5, input_shape=input_shape))
    LSTM.add(layers.Dense(1))
    LSTM.compile(loss='mean_squared_error', optimizer='adam')
    return LSTM

def RNN(input_shape = (1, 1)):
    RNN = Sequential()
    RNN.add(layers.SimpleRNN(5, input_shape=input_shape))
    RNN.add(layers.Dense(1))
    RNN.compile(loss='mean_squared_error', optimizer='adam')
    return RNN

