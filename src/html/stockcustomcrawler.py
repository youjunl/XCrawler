import tushare as ts
from pandas_datareader import data as pdr
import yfinance as yf
import src.data_processor as data_processor
import src.html as html
import requests
import json
from algorithm.stock import Stock
# ==================================== 第三方
# tushare获取股票数据
def getStockData(stockNum):
   dd = ts.get_hist_data(stockNum) #爬取股票近三年的全部日k信息
   print(dd)
   #dd.applymap('002837'+'.xlsx') #将信息导出到excel表格中

# pandas_datareader通过yahoo获取股票数据
def getStockData_datareader(stockNum,enginstr):
   yf.pdr_override()
   code = stockNum + '.ss'
   stockData = pdr.get_data_yahoo(code,'2023-10-01')
   stockData = stockData.round(2) 
   stockData.to_csv('Assets/' + code + '.csv')
   stockData.to_excel('Assets/' + code + '.xlsx')
   stockData.to_json('Assets/' + code + '.json')   
   # 已mysql为例,如果已localhost为host,那port端口一般为3306
   # enginstr = "mysql+pymysql://root:Akeboshi123~@localhost:3306/stockData"
   name = data_processor.GetDataFromSql("代码库","代码","名称",stockNum,enginstr)
   if name == "":
      html.getStocksTime(stockNum,enginstr)
      name = data_processor.GetDataFromSql("代码库","代码","名称",stockNum,enginstr)
   data_processor.customDataSavetosql(name,enginstr,stockData)
   
   stock_instance = Stock(stockData, [10,10,10,10,10,10])
   print(stock_instance)
   print(f"{name} customDatareader crawle completed")
   return
   # 5日收盘价均价
   # mean_price_5 = stock['Close'].rolling(window=5).mean() 
   # mean_price_10 = stock['Close'].rolling(window=10).mean() 
   # mean_price_20 = stock['Close'].rolling(window=20).mean() 
   # mean_price_30 = stock['Close'].rolling(window=30).mean() 
   # mean_price_40 = stock['Close'].rolling(window=40).mean() 
   # mean_price_60 = stock['Close'].rolling(window=60).mean() 
   # 绘制均线逻辑
   # zonghe_data=pd.concat([mean_price_5,mean_price_10,mean_price_20,mean_price_30,mean_price_40,mean_price_60],axis=1)
   # zonghe_data.columns = ['MA5','MA10','MA20','MA30','MA40','MA60']
   # zonghe_data[ ['MA5','MA10','MA20','MA30','MA40','MA60']].plot(subplots=False,style=['r','g','b','m'],grid=True)
   # print(f"MA5: {mean_price_5} MA10: {mean_price_10} MA30: {mean_price_30}")
   # plt.show()


   