# coding=utf-8
import os.path
import sys
from configparser import ConfigParser
from iotdb.Session import Session

cf = ConfigParser()
cf.read(os.path.join(sys.path[0], 'config.ini'), encoding='utf-8-sig')


def error():
    count = 'COUNT: count_timeseries | count_storage_group | count_seq | count_unseq | count_all| \n'
    total = 'SUM: sum_seq | sum_unseq | sum_all | sum_resource | sum_wal | \n'

    print('必须且只能指定一个参数，参数可以是:')
    print(count, total)
    exit()


def sql(order):
    ip = '127.0.0.1'
    port_ = cf.get('connect', "port")
    username_ = cf.get('connect', "username")
    password_ = cf.get('connect', "password")
    session = Session(ip, port_, username_, password_)

    session.open(False)
    query = session.execute_query_statement('%s' % order)
    while query.has_next():
        print(query.next().get_fields()[0])
    session.close()


def check_data(path):
    if not cf.get('path', path):
        return os.path.join(cf.get('path', 'iotdb_home'), 'data/data')
    else:
        return cf.get('path', path)


def data_tsfile_count(para):
    results = 0
    datas = check_data('data')
    for data in datas.split(','):
        result = int(os.popen('find %s -name \'*.tsfile\' | wc -l' % os.path.join(data, para)).read())
        results += result
    return results


def data_tsfile_sum(para):
    results = 0
    paths = check_data('data')
    for path in paths.split(','):
        result = int(os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1' % os.path.join(path, para)).read().split('\t')[0])
        results += result
    return results * 1024


def data_tsfile_level_count(para):
    results = 0
    datas = check_data('data')
    for data in datas.split(','):
        result = int(os.popen('find %s -name \'*-*-0-*.tsfile\' | wc -l' % os.path.join(data, para)).read())
        results += result
    return results


def data_resource_sum():
    results = 0
    paths = check_data('data')
    for path in paths.split(','):
        result = int(os.popen('find %s -name \'*.tsfile.resource\' | xargs du -s -c | tail -n 1' % path).read().split('\t')[0])
        results += result
    return results * 1024


def wal_sum():
    if not cf.get('path', 'wal'):
        path = os.path.join(cf.get('path', 'iotdb_home'), 'data/wal')
    else:
        path = cf.get('path', 'wal')
    results = os.popen('du -s %s' % path).read()
    return int(results.split('\t')[0]) * 1024


def monitor_data():
    pass


def main(para):
    if para == "count_timeseries":  # 统计时间序列数量
        sql('count timeseries')

    elif para == 'count_storage_group':  # 统计存储组数量
        sql('count storage group')

    elif para == 'count_seq':  # 统计顺序tsfile数量
        print(data_tsfile_count('sequence'))

    elif para == 'sum_seq':
        print(data_tsfile_sum('sequence'))  # 统计顺序tsfile大小

    elif para == 'count_unseq':
        print(data_tsfile_count('unsequence'))  # 统计乱序tsfile数量

    elif para == 'sum_unseq':
        print(data_tsfile_sum('unsequence'))  # 统计乱序tsfile大小

    elif para == 'count_all':  # 统计全部tsfile数量
        print(data_tsfile_count(''))

    elif para == 'sum_all':  # 统计全部tsfile大小
        print(data_tsfile_sum(''))

    elif para == 'sum_resource':  # 统计全部resource文件大小
        print(data_resource_sum())

    elif para == 'sum_wal':  # 统计wal文件夹大小
        print(wal_sum())

    elif para == 'count_seq_lv0':  # 统计全部顺序0层tsfile大小
        print(data_tsfile_level_count('sequence'))

    elif para == 'count_unseq_lv0':  # 统计全部乱序tsfile大小
        print(data_tsfile_level_count('unsequence'))

    else:
        error()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        error()
    if not cf.get('path', 'iotdb_home'):
        print('must special iotdb home ')
        exit()
    main(sys.argv[1])

