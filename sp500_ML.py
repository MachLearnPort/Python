import numpy as nump
import pandas as pd
import pickle

# ML model that determines what to do with a stock in 7 days
# Note: you dont want to look back to far with you ML models, as the relationships between compnaies
# has probably changed (and only look back about 1 - 2 years), as they may not be correlated then 
def process_data_for_labels(ticker):
  hm_days = 7; #How many days in the future do we have to loose/gain x-percent
  df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
  tickers = df.columns.values.tolist() #nested list to seperate each ticker
  df.fillna(0, inplace=True) ##fill all the N/A values with 0

  for i in range (1, hm_days+1): #hm_days+1 so that we get a loop from 1-7 and not 0-7
    
    # Calculate the percent change of the stock
    df['{}_{}d'.format(ticker, i)] = ((df[ticker].shift(-i) - df[ticker]) / df[ticker])     #{} brackets is where we put the items in the formate object 
    
    #so for APPL ticker on day 2, we have {ticker}_{i}d -> APPL_2d for the apple ticker on day 2
    # which = (((Price in 2 days from now)-(todays price))/todays price)*100
    # .shift, shifts the index negitively to get future data (up/down shift in the column). 
  df.fillna(0, inplace=True)
  return tickers, df

# Define out buy, hold and sell requirments
def buy_sell_hold(*args):
  cols = [c for c in args] #passing cols as parameters into pandas
  requirement = 0.02
  for col in cols:
    if col > requirement:
      return 1
    if col < -requirement:
      return -1
    else:
      return 0


