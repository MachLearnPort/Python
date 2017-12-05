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

#print(save_sp500_tickers())

def get_data_from_yahoo(reload_sp500=False): #function for getting the ticker data
  nowork=[]
  if reload_sp500: 
    tickers = save_sp500_tickers()
  else:
      with open("sp500tickers.pickle","rb") as f:
        tickers=pickle.load(f)

  if not os.path.exists('stock_dfs'):
      os.makedirs('stock_dfs')

    #set start and end time for loop
  start = dt.datetime(2000,1,1)
  today = dt.datetime.today()
  end = dt.datetime(today.year, today.month, today.day)
  
  for ticker in tickers: # you could use tickers[], and inside the brackets, say what tickers you want
    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
      fix_yahoo_finance.pdr_override() #had to add to fix the yahoo issue with cookies
      df = web.get_data_yahoo(ticker, start, end)
      df.to_csv('stock_dfs/{}.csv'.format(ticker))
    if os.path.getsize("stock_dfs/{}.csv".format(ticker)) <= 3:      
      nowork.append(ticker)       
    else:
      print('Already have {}'. format(ticker))
  print(nowork) 

get_data_from_yahoo()

def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close':ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


compile_data()
