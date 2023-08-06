#!/bin/bash
if [[ ! -d $data_dir ]];then
   echo "data dir $data_dir"
   mkdir -p $data_dir
fi

if [[ ! -d $log_dir ]];then
   echo "data dir $log_dir"
   mkdir -p $log_dir
fi

if [[ ! -d $monitor_log_dir ]]; then
   echo "monitor logs dir: $monitor_log_dir"
   mkdir -p $monitor_log_dir
fi

eval $custom_host

#python3.8 -u ensure_indexes_mongo.py &
#python3.8 -u ensure_kafka_topic.py &