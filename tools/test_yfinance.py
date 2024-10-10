import yfinance as yf

stockData = yf.download('601318.ss', '2024-10-08', '2024-10-09')

print(stockData)