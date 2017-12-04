import datetime as dt #date time
import matplotlib.pyplot as plt #create plots
from matplotlib import style #stylize graphs
import pandas as pd #module handles dataframes
import pandas_datareader.data as web #grab data from finance API

style.use('ggplot') #Set style using ggplot

start = dt.datetime(2000, 1, 1) #Set startdate [ yr, m, d]
end = dt.datetime(2016, 12, 31) #Set end date [ yr, m, d]

# df = web.DataReader('TSLA', 'yahoo', start, end) #Extract ('String is ticker name', 'source', start time, end time) and import as dataframe
# print(df.head()) #print header rows of frame
# print(df.tail()) #print end rows of frame
# print(df['Adj Close']) #print specific col
# print(df[['Adj Close', 'High']) #print specific cols

# df.to_csv('tsla.csv') #convert frame to csv

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0) #read in csv (but can also be json, sql, excel, etc.)

# df['Adj Close'].plot() #plot dataframe - in [] we can pick the column in the df
# plt.show() #show dataframe

df['100ma']= df['Adj Close'].rolling(window=100).mean() #Create new col in df for 100 moving average

print(df.tail())