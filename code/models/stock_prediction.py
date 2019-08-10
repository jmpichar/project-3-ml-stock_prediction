'''
Helper functions used to predict stock price using RNN and LSTM model.
'''

# Import my dependencies
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
import tensorflow as tf

# from alpha_vantage import alpha_vantage.timeseries
from alpha_vantage.timeseries import TimeSeries
api_key = 'S7MZO4XSG71DN2NB'

def get_stock_data(ticker):
    # api_key = 'S7MZO4XSG71DN2NB'
    ts = TimeSeries(key=api_key,output_format='pandas')
    # ticker = 'NASDAQ:INTC'

    # Get the raw dataset
    dataset, meta_df = ts.get_daily(symbol=ticker, outputsize='full')

    # Rename columns
    dataset.columns = ['open_price', 'high', 'low', 'close', 'volume']

    # Add ticker name to each row
    dataset['name'] = ticker
    dataset.reset_index(inplace=True)

    # Create a ditionary to insert in  db
    data = dataset.to_dict(orient='record')

    # Data cleaning
    #print('Checking for null values')
    #orig_dataset.isna().any()

    # # plot the dataset
    # orig_dataset['close'].plot()
    # plt.title(f'{ticker} Daily Adjusted TimeSeries')
    # plt.show()

    # Look at volume
    #plt.figure()
    #plt.plot(dataset["volume"])
    #plt.title(f'{ticker} stock volume history')
    #plt.ylabel('Volume')
    #plt.xlabel('Days')
    #plt.show()
    return data

def data_prep():
    # Create data frame to use to extract traing, test data
    df = orig_dataset['close'].values
    df = df.reshape(-1,1)
    print(df.shape)

    # split data into train and test
    dataset_train = np.array(df[:int(df.shape[0]*0.8)])
    dataset_test = np.array(df[int(df.shape[0]*0.8)-60:])
    print(dataset_train.shape)
    print(dataset_test.shape)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0,1))
    dataset_train = scaler.fit_transform(dataset_train)
    dataset_test = scaler.transform(dataset_test)

# converting dataset into x_train and y_train
def create_dataset(df):
    x = []
    y = []
    for i in range(60,df.shape[0]):
        x.append(df[i-60:i,0])
        y.append(df[i,0])
    x = np.array(x)
    y = np.array(y)
    return x,y

def create_lstm_model():
    x_train, y_train = create_dataset(dataset_train)
    x_test, y_test = create_dataset(dataset_test)

    # Reshaping for LSTM
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1))
    print(x_train.shape)
    print(x_test.shape)

    tf.logging.set_verbosity(tf.logging.ERROR)
    model = Sequential()
    model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96,return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96))
    model.add(Dropout(0.2))
    model.add(Dense(units=1, activation='sigmoid'))

    model.summary()
    model.compile(loss='mean_squared_error', optimizer ='adam')

    if(not os.path.exists('./outputs/stock_prediction.h5')):
        model.fit(x_train, y_train, epochs=100, batch_size=32)
        model.save('./outputs/stock_prediction.h5')
    else:
        model = load_model('./outputs/stock_prediction.h5')

# Visualize the predictions
def create_visulalization():
    # get_ipython().run_line_magic('matplotlib', 'inline')
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    fig, ax = plt.subplots(figsize=(12,6))
    plt.plot(df, color='red', label='original Stockprice')
    ax.plot(range(len(y_train)+50, len(y_train)+50+len(predictions)),predictions,color='blue', label='predicted')
    plt.legend()
    print(range(len(y_train)+50, len(y_train)+50+len(predictions)))

    # convert scaled data back to normal values
    y_test_scaled = scaler.inverse_transform(y_test.reshape(-1,1))

    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(y_test_scaled, color='red', label = 'True Price of testing set')
    plt.plot(predictions, color = 'blue', label='predicted')

    plt.legend()

# create data frame with the actual close, prediction and percent difference for last 30 days
# percentdiff = ((val1-val2)/((val1+val2)/2))*100
# ((46.970-50.077579)/((46.970+50.077579)/2))*100
def percent_diff():
    orig_arr = np.array(df[:-11:-1])
    orig_reversed_arr = orig_arr[::-1]
    orig_reversed_arr

    pred_arr = np.array(predictions[:-11:-1])
    pred_reversed_arr = pred_arr[::-1]
    pred_reversed_arr

    new_df = orig_dataset.copy()
    new_df = new_df.reset_index()
    new_df = new_df.iloc[-10:]
    #new_df.shape

    new_df = new_df[['date','close']]
    tmp_date = new_df['date']

    percent_diff = pd.DataFrame({'close':orig_reversed_arr[:,0], 'pred':pred_reversed_arr[:,0]})

    mask = ((percent_diff['close'] - percent_diff['pred']) / ((percent_diff['close'] + percent_diff['pred'])/2))*100
    percent_diff['percent difference'] = mask.round(2)

    new_df.merge(percent_diff, on='close').set_index('date')
