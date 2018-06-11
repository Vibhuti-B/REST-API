# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:59:53 2018

@author: ACER-PC
"""

from flask import Flask, request,render_template
from flask_restful import Resource, Api,reqparse
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import sqlite3
import datetime
from iexfinance import get_historical_data
import pandas as pd


app = Flask(__name__)
api = Api(app)

@app.route('/')
def index_form():
    return render_template('index.html')

@app.route('/GetAvailableTicker',endpoint='GetAvailableTicker')
def showSymbols():
    connection=sqlite3.connect('G:/Zenalytics/Stock Market.db')
    cursor=connection.cursor()
    query=cursor.execute("Select distinct Ticker from Historical_Data")
    symbols={'Available Symbols: ':[i for i in query.fetchall()]}
    connection.close
    return  jsonify(symbols)   


@app.route('/',methods=['POST'])
def index_form_post():
    ticker=request.form['ticker']
    start_date=request.form['start_date']
    end_date=request.form['end_date']
    connection = sqlite3.connect('G:/Zenalytics/Stock Market.db')
    cursor = connection.cursor()
    ticker="'"+str(ticker)+"'"
    start_date="'"+str(start_date)+"'"
    end_date="'"+str(end_date)+"'"
    
    q="select * from Historical_Data where Ticker="+ticker+" and date between "+start_date+" and "+end_date
    query = cursor.execute(q) 
    rows=query.fetchall()
    if rows:
        stringStock={'Stock Value: ': [i for i in rows]} 
    else:
        stringStock={'Ticker Unavailable': ticker}
    connection.close  
    return jsonify(stringStock) 

@app.route('/pnl/<string:ticker>',methods=['GET'])
def PNL(ticker):
    #ticker='MSFT'
    connection=sqlite3.connect('G:/Zenalytics/Stock Market.db')
    ticker="'"+str(ticker)+"'"
    query="Select * from Historical_Data where Ticker="+ticker
    data=pd.read_sql(query,connection)
    connection.close
    if not data.empty:
        data=data.drop(columns=['Ticker','Index','date'])
        data['ewma26']=pd.ewma(data['close'],26)
        data['ewma12']=pd.ewma(data['close'],12)
        data['macd']=data['ewma12']-data['ewma26']
    #    data.plot(y='close',color='blue')
    #    data.plot(y='macd',color='yellow')
        multiplier=2/13
        ewma12=float((data['close'].tail(1)-data['ewma12'].tail(1))*multiplier + data['ewma12'].tail(1))
        pnl=float(ewma12-data['close'].tail(1))
        if pnl>0:
            return jsonify({"Buy stock PNL: ":str(pnl),"Price tomorrow: ":ewma12})
        return jsonify({"Sell stock PNL: ":str(-pnl),"Price tomorrow: ":ewma12})
    else:
        return showSymbols()
    

def insertToDatabase(ticker):
    connection = sqlite3.connect('G:/Zenalytics/Stock Market.db')
    cursor=connection.cursor()
    ticker1="'"+ticker+"'"
    query=cursor.execute("Select max(date) from Historical_Data where Ticker="+ticker1)
    max_date=query.fetchall()
    end = datetime.date.today() 
    
    if max_date:
        last_date=''.join(max_date[0])
        year,month,day=last_date.split("-")    
        last_date=datetime.date(int(year),int(month),int(day))
        start=last_date+datetime.timedelta(days=1)
    else:
        start = end-datetime.timedelta(days=365)
    data = get_historical_data(ticker, start=start, end=end, output_format='pandas')
    data.reset_index(inplace=True)
    data['Ticker']=ticker
    data=data[['Ticker','date','open','high','low','close','volume']]
    data.to_sql('Historical_Data', con=connection, if_exists='append')
    connection.commit
    print("Database Updated")
    
if __name__ == '__main__':
    ticker='MSFT'
    insertToDatabase(ticker) 
    app.run(debug=True,
             host='127.0.0.1',
             port=5002)