from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import os
import requests
import sys
import boto3
import yfinance as yf
import pandas as pd

def get_data(ticker="AAPL"):
    data = yf.download(ticker, timeout=120)
    df = pd.DataFrame(data['Adj Close'][ticker])
    df.rename(columns={ticker: "Close"}, inplace=True)
    # The strategy only uses Adjusted Close, but the library requires Open, High, and Low
    df['Open'] = df['High'] = df['Low'] = df['Close']
    df = df.reindex(['Open', 'High', 'Low', 'Close'], axis=1)
    return df

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

def upload_file(file_path,bucket_name,s3_key):
    s3 = boto3.resource('s3', region_name='us-east-1')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(file_path,s3_key,ExtraArgs = { "ContentType" : "text/html"})

    # Print a shortcut to the S3 location (the link is temporary)
    temp_url = s3.meta.client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name,
                'Key': s3_key},
        ExpiresIn=1440
        )
    print(temp_url)

if __name__ == "__main__":
    bucket_name = os.environ['BUCKET']
    ticker = os.environ['TICKER']

    print(f"Getting data for {ticker}...")
    data = get_data(ticker)
    bt = Backtest(data, SmaCross,
                cash=10000, commission=.002,
                exclusive_orders=True)

    output = bt.run()

    print(output)

    # Upload the output to Amazon S3
    output_file = '{ticker}-output.txt'
    output_path = '/tmp/' + output_file
    with open(output_path, 'w') as f:
        print(output, file=f)
    print("===Output===")
    upload_file(output_path, bucket_name, 'reports/' + output_file)

    # Save the backtest results
    plot_file = '{ticker}-plot.html'
    plot_path = '/tmp/' + plot_file
    bt.plot(filename=plot_path)
    print("===Plot===")
    upload_file(plot_path, bucket_name, 'reports/' + plot_file)