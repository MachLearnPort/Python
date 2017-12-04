import bs4 as bs
import datetime as dt
import os #Misc operating system interfaces
import pandas as pd
import pandas_datareader.data as web 
import pickle
import requests
import fix_yahoo_finance #Had to add as their was an issue reteriving the data

def save_sp500_tickers(): #function for getting the ticker names
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers

print(save_sp500_tickers())

def get_data_from_yahoo(reload_sp500=False): #function for getting the ticker data
  if reload_sp500: 
    tickers = save_sp500_tickers()
  else:
      with open("sp500tickers.pickle","rb") as f:
        tickers=pickle.load(f)

  if not os.path.exists('stock_dfs'):
      os.makedirs('stock_dfs')

    #set start and end time for loop
  start = dt.datetime(2000,1,1)
  end = dt.datetime(2017,12,31)
  
  for ticker in tickers: # you could use tickers[], and inside the brackets, say what tickers you want
    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
      fix_yahoo_finance.pdr_override() #had to add to fix the yahoo issue with cookies
      df = web.get_data_yahoo(ticker, start, end)
      df.to_csv('stock_dfs/{}.csv'.format(ticker))
    else:
      print('Already have {}'. format(ticker))
      
get_data_from_yahoo()

    