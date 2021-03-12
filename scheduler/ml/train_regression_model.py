import os
import pickle
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from scheduler.ml.regression_model import LSTM, RNN
# from regression_model import LSTM, RNN
import yfinance as yf
import joblib
import numpy as np
import pandas as pd
import datetime

def check_path(stock_symbol):
    base_path= "./trained_model/{}/".format(stock_symbol)
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    return base_path

def preprocess(stock_symbol, dataset):
    dataset = np.average(dataset, axis=1)
    dataset = np.reshape(dataset, (-1, 1))

    base_path = check_path(stock_symbol)
    scaler_path = base_path + "scaler"

    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
        dataset = scaler.fit_transform(dataset)
    else:
        scaler = MinMaxScaler(feature_range=(0, 1))
        dataset = scaler.fit_transform(dataset)
        joblib.dump(scaler, scaler_path)

    return dataset

def inverse_preprocess(stock_symbol, data):
    base_path = check_path(stock_symbol)
    scaler_path = base_path + "scaler"
    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
        data = scaler.inverse_transform(data)

    return data


def create_dataset(dataset, time_step = 1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i : (i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])

    # data format [samples, timestep]
    dataX = np.array(dataX)
    # data format [samples, timestep, feature]
    dataX = dataX.reshape(dataX.shape[0], dataX.shape[1], 1)
    dataY = np.array(dataY) 	
    return dataX, dataY


def generate_dataset_for_train(time_step, dataset, split_rate=0.9):
    train_size = int(len(dataset) * split_rate)
    test_size = len(dataset) - train_size
    train, test = dataset[:train_size,:], dataset[train_size:len(dataset), : ]
    trainX, trainY = create_dataset(train, time_step)
    testX, testY = create_dataset(test, time_step)
    return (trainX, trainY), (testX, testY)


def train(stock_symbol, time_step, trainX, trainY, testX, testY, model_type="LSTM"):
    base_path = check_path(stock_symbol)
    model_path = base_path + model_type + ".h5"
    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
        if model_type == 'LSTM':
            model = LSTM((time_step, 1))
        elif model_type == 'RNN':
            model = RNN((time_step, 1))
        else:
            model = RNN((time_step, 1))
    model.fit(trainX, trainY, validation_data=(testX, testY), epochs=100, batch_size=16)
    model.save(model_path)
    return model

def train_model(stock_symbol, time_step=5):
    data = yf.download(stock_symbol, period = "2y", interval = "1d")
    dataset = data.values[:, :-2]
    dataset = preprocess(stock_symbol, dataset)    
    (trainX, trainY), (testX, testY) = generate_dataset_for_train(time_step, dataset)
    train(stock_symbol, time_step, trainX, trainY, testX, testY, "RNN")
    train(stock_symbol, time_step, trainX, trainY, testX, testY, "LSTM")


def predict(stock_symbol, model_type, next_days = 5, time_step=5):
    # prepare data
    data = yf.download(stock_symbol, period = "30d", interval = "1d")
    dataset = data.values[:, :-2]
    today = data.index[-1]
    dataset = preprocess(stock_symbol, dataset)
    dataset = dataset[-time_step:]
    # load model
    base_path = check_path(stock_symbol)
    model_path = base_path + model_type + ".h5"
    if not os.path.exists(model_path):
        train_model(stock_symbol)
    model = load_model(model_path)

    # predict next_days stock
    predict = []
    for i in range(5):
        next_value = model.predict(np.array([dataset]))
        predict.append(next_value[0])
        # remove the first one and add the predict value to the end
        dataset = np.append(dataset[1:], next_value, axis=0)

    predict = np.array(predict)
    predict = inverse_preprocess(stock_symbol, predict)

    # next date
    next_5days = []
    today = today.to_pydatetime()
    oneday = datetime.timedelta(days=1)
    for i in range(next_days):
        today = today + oneday
        next_5days.append([today, predict[i][0]])
    
    return next_5days
    


if __name__ =="__main__":
    # train_model("AAPL")
    next_5days = predict("AAPL", "LSTM")
    print(next_5days)
    print(type(next_5days[3]))

