import urllib.request as request
import json
import pandas as pd
from datetime import date
from cerberus import Validator

from hive_upload import *
from mysql_upload import DbConnector

import sys
import os
os.environ['SPARK_HOME'] = "/home/nineleaps/.local/lib/python3.8/site-packages/pyspark"
sys.path.append("/home/nineleaps/.local/lib/python3.8/site-packages/pyspark/python")
sys.path.append("/home/nineleaps/.local/lib/python3.8/site-packages/pyspark/python/lib")
from pyspark import  SparkConf
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").config(conf=SparkConf()).getOrCreate()


today = date.today()
today_str = date.today().strftime("%Y-%d-%m")

def get_data(**args):
    with request.urlopen('https://api.covid19india.org/data.json') as response:
        source = response.read()
        data = json.loads(source)

    statewise_dict = data['statewise']
    v = Validator()
    v.schema = {'active': {'required': True, 'type': 'string'},
                'confirmed': {'required': True, 'type': 'string'},
                'deaths': {'required': True, 'type': 'string'},
                'recovered': {'required': True, 'type': 'string'},
                'deltaconfirmed': {'required': True, 'type': 'string'},
                'deltadeaths': {'required': True, 'type': 'string'},
                'deltarecovered': {'required': True, 'type': 'string'},
                'lastupdatedtime': {'required': True, 'type': 'string'},
                'migratedother': {'required': True, 'type': 'string'},
                'statecode': {'required': True, 'type': 'string'},
                'statenotes': {'required': True, 'type': 'string'},
                'state': {'required': True, 'type': 'string'},
                }
    for item in statewise_dict:
        if not v.validate(item):
            print(v.errors)
            raise ValueError('API Data Not Valid')
    print('API Data is valid')

    df = pd.DataFrame(statewise_dict,
                  columns=['active', 'confirmed', 'deaths', 'recovered', 'state'])
    date = []
    for i in range(len(df.index)):
        date.append(today)
    df['date'] = date
    sdf = spark.createDataFrame(df)
    sdf.write.mode("overwrite").csv("hdfs://localhost:9000/user/nineleaps/covid_data.csv")
    print("Covid Statewise Data CSV is uploaded to HDFS")

def upload_data_to_hive(**args):
    main()
    print('Data uploaded to Hive')

def create_mysql(**args):
    db = DbConnector()
    db.table_creation()
    print('Connected to MySQL')