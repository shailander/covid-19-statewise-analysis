## Introduction
```
Airflow pipeline to fetch daily new covid cases data for indian states and store them into hive partition table and genreate graphs for same using grafana.
​
```
​
## Setup Grafana
1. Download the Grafana GPG key with wget, then pipe the output to apt-key. This will add the key to your APT installation’s list of trusted keys, which will allow you to download and verify the GPG-signed Grafana package.
  
    `wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -`
2. Next, add the Grafana repository to your APT sources:
    
    `sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"`
3. Refresh your APT cache to update your package lists:
    
    `sudo apt update`
4. Next, make sure Grafana will be installed from the Grafana repository:
    
    `apt-cache policy grafana`
​
5. You can now proceed with the installation:
​
    `sudo apt install grafana`
6. Once Grafana is installed, use systemctl to start the Grafana server:
​
    `sudo systemctl start grafana-server`
    
    now grafana server is running on `http://localhost:3000/` (default address)
​
​
* #### Elasticsearch Setup
​
1. Downloadinh and extracting elasticsearch tar file:
​
    `wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.0-linux-x86_64.tar.gz
     wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.0-linux-x86_64.tar.gz.sha512
     shasum -a 512 -c elasticsearch-7.8.0-linux-x86_64.tar.gz.sha512 
     tar -xzf elasticsearch-7.8.0-linux-x86_64.tar.gz
     cd elasticsearch-7.8.0/`
     
2. Starting elasticsearch:
​
    `./bin/elasticsearch`
    
​
*   #### Kibana Setup
1. Download Kibana tar file:
​
    `wget https://dl.grafana.com/oss/release/grafana-7.0.6.linux-amd64.tar.gz`
2. Extract the .tar file:
    
    `tar -zxvf grafana-7.0.6.linux-amd64.tar.gz`
3. Start Kibana server:
​
    `cd kibana-7.8.0-linux-x86_64`  
    `./bin/kibana`
​
*   ## Filebeat Setup
  1. use the below command to install filebeat:
        
        `curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.8.0-amd64.deb`
        
        `sudo dpkg -i filebeat-7.8.0-amd64.deb`
    
  2. go to filebeat directory
        `cd filebeat-7.8.0-linux-x86_64`
    
  3. start filebeat
        `sudo ./filebeat -e`
    
*  ## AmazonS3Bucket Setup for storing Airflow logs(Remote logging)
1. Follow this tutorial for storing logs to S3 bucket.
        `https://www.youtube.com/watch?v=DKsWEmoqwZY`
        
* ## Getting AWS logs from S3 to Kibana
1. Follow this tutorial for getting AWS logs from S3 using Filebeat and Elasticsearch.
        `https://www.elastic.co/blog/getting-aws-logs-from-s3-using-filebeat-and-the-elastic-stack`
​
​
​
​
## How to run project on local laptop
*   install remaining packages for airflow tasks using:
    
    `pip install -r requirements.txt`
    
*   start haddop fs using:
        
        `$HADOOP_HOME/sbin/start-yarn.sh`
        `$HADOOP_HOME/sbin/start-dfs.sh`
        
*   start airflow using commands below:
       
        `airflow webserver`
        `airflow scheduler`
​
*   then go to address `localhost:8080` and resume the `covid_data` dag
​
* start elasticsearch, kibana, filebeats server to see logs visualization on Kibana UI.
        1. Go to `localhost:5601`.
        2. Under Observability/logs select `Add log data`.
        3. Select `AWS S3 based logs` as the data source.
        4. Select `AWS S3 server access log dashboard` to see the dashboard if all requirement is setup.
        
* start datadog server to fetch airflow metrics data:
        
        1. go to datadog site and login to your account.
        2. Under Dashboards section select Apache Airflow.
        2. datadog will automatically fetch logs from the Airflow dag and will show real time updated visualization.
         
         
            