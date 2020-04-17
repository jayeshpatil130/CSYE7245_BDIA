#Final
import boto3
import pandas as pd
import io
import csv
import time
import boto3
import json
import config as cfg
from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key = cfg.stock['api'])
ACCESS_KEY = cfg.aws[0]['access_key']
SECRET_KEY = cfg.aws[0]['secret_key']
BUCKET = cfg.aws[0]['bucket_name']
s3 = boto3.client('s3', aws_access_key_id = ACCESS_KEY,
                      aws_secret_access_key = SECRET_KEY)
obj = s3.get_object(Bucket = BUCKET, Key = 'input.csv')
df = pd.read_csv(io.BytesIO(obj['Body'].read()))

for i,j in df.iterrows():
    data, meta_data = ts.get_weekly(j['Ticker'])
    meta_data["5. Category"] = j['Category']
    meta_data["6. Company Name"] = j['Company']
    meta_data["7. Market Sector"] = j['Market']
    s3.put_object(Body = json.dumps(data), Bucket = BUCKET, Key = 'StockAPI/' + j['Category'].replace(" ","") + '/' + j['Company'].replace(" ","") + '/' + j['Company'].lower().replace(" ", "") + '.json')
    s3.put_object(Body = json.dumps(meta_data), Bucket = BUCKET, Key = 'StockAPI/' + j['Category'].replace(" ","") + '/' + j['Company'].replace(" ","") + '/' + j['Company'].lower().replace(" ", "") + '_metadata.json')