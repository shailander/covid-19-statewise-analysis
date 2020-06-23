import sys
import os
from datetime import date
os.environ['SPARK_HOME'] = "/home/nineleaps/.local/lib/python3.8/site-packages/pyspark"
sys.path.append("/home/nineleaps/.local/lib/python3.8/site-packages/pyspark/python")
sys.path.append("/home/nineleaps/.local/lib/python3.8/site-packages/pyspark/python/lib")

from pyspark.sql import SparkSession


today = date.today().strftime("%Y-%d-%m")

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL Hive integration OO") \
    .enableHiveSupport().getOrCreate()

def main():
    spark.sql("""create table if not exists data_partition
                (active string,confirmed string,deaths string,recovered string,state string)
                PARTITIONED BY (date STRING)
                ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'""")
    spark.sql("""load data inpath
                'hdfs://localhost:9000/user/nineleaps/covid_data.csv'
                into table data_partition PARTITION(date='{}')""".format(today, today))