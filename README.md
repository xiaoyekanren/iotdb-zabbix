## 不清楚
1. memtable 大小
2. 刷的频率  
3. 刷的单个花费时间  
avg points, avg time series  
4. 一分钟查询的个数
5. 一分钟session登录的数量  
    //这个代表客户端创建client的数量么？  
6. 数据趋势  
    --用来观测数据在不同时间下的趋势变化，总结行业经验
7. 日志中新出现的error数量  
8. 日志中新出现的warn数量  


## 完成的：  
1. 统计时间序列数量，count_timeseries,int  
2. 统计存储组数量，count_storage_group,int  
3. 统计顺序文件数量，count_seq,int  
4. 统计顺序文件大小，sum_seq,int
5. 统计乱序文件数量，count_unseq,int
6. 统计乱序文件大小，sum_unseq,int
7. 统计全部tsfile文件数量，count_all,int
8. 统计全部tsfile文件大小，sum_all,int
9. 统计全部resource文件大小，sum_resource,int
10. 统计wal目录大小，sum_wal,int
11. 监控磁盘io  
    tps: io_tps,float;  
    read: io_read_kb_s,float;  
    write: io_write_kb_s,float  

## 依赖
### python依赖
python>=3.8  
apache-iotdb  

## tips
1. 注意用户权限，在普通用户下安装的pip依赖，在root用户下不能使用
2. cf.get的路径有问题