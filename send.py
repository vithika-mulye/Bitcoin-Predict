def send_data():
    from tensorflow import keras

    regressor = keras.models.load_model('RNN.h5')

    # First step, import libraries.
    import numpy as np
    import pandas as pd 
    import matplotlib
    from matplotlib import pyplot as plt

    # Import the dataset and encode the date
    df = pd.read_csv('coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv')
    df['date'] = pd.to_datetime(df['Timestamp'],unit='s').dt.date
    group = df.groupby('date')
    Real_Price = group['Weighted_Price'].mean()

    # split data
    prediction_days = 30
    df_train= Real_Price[:len(Real_Price)-prediction_days]
    df_test= Real_Price[len(Real_Price)-prediction_days:]

    # Data preprocess
    training_set = df_train.values
    training_set = np.reshape(training_set, (len(training_set), 1))
    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler()
    training_set = sc.fit_transform(training_set)
    X_train = training_set[0:len(training_set)-1]
    y_train = training_set[1:len(training_set)]
    X_train = np.reshape(X_train, (len(X_train), 1, 1))


    # Making the predictions
    test_set = df_test.values
    inputs = np.reshape(test_set, (len(test_set), 1))
    inputs = sc.transform(inputs)
    inputs = np.reshape(inputs, (len(inputs), 1, 1))
    predicted_BTC_price = regressor.predict(inputs)
    predicted_BTC_price = sc.inverse_transform(predicted_BTC_price)
    print(predicted_BTC_price)


    # Visualising the results
    plt.figure(figsize=(25,15), dpi=80, facecolor='w', edgecolor='k')
    ax = plt.gca()  
    plt.plot(test_set, color = 'red', label = 'Real BTC Price')
    plt.plot(predicted_BTC_price, color = 'blue', label = 'Predicted BTC Price')
    plt.title('BTC Price Prediction', fontsize=40)
    df_test = df_test.reset_index()
    x=df_test.index
    labels = df_test['date']
    plt.xticks(x, labels, rotation = 'vertical')
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(18)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(18)
    plt.xlabel('Time', fontsize=40)
    plt.ylabel('BTC Price(USD)', fontsize=40)
    plt.legend(loc=2, prop={'size': 25})
    plt.savefig("done.png")

    return str(predicted_BTC_price)

send_data()