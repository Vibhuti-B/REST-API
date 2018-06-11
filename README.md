# REST-API
Python Code to receive Ticker and return historical stocks and next day prediction

The code is available in StockData.py file.

create a database -Stock Market.db
The database consists of 1 table- Historical_Data:
CREATE TABLE "Historical_Data" ( `Index` INTEGER, `Ticker` TEXT, `date` REAL, `open` NUMERIC, `high` NUMERIC, `low` INTEGER, `close` NUMERIC, `volume` NUMERIC )

1. def insertToDatabase(): The function receives the ticker and adds it to the database. If the ticker info is already available, it adds on to new data from IEExchange.

2. The localhost is "http://127.0.0.1:5002".

3. def  index_form(): Redirects to the Index Page

4. def index_form_post(): Receives Ticker, Start Date and End Date from Index Page and generates a JSON response to filter the historical prices form database for the specified criteria.

5. def PNL(): To obtain the next day's prediction using Moving Average Convergence Divergence(MACD) for Exponential Moving Average- 12 and 26, type: "http://127.0.0.1:5002/pnl/<ticker>" in the URL( Eg: http://127.0.0.1:5002/pnl/MSFT). It redirects to this method which displays the next day's Predicted Close Price and whether to buy or sell the stock based on the Profit and Loss. In case the ticker is unavaialble in the database, the function redirects to a page to display available Tickers.
  
  
