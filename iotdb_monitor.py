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
    ip = cf.get('connect', 'ip')
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


def monitor_data():
    pass


def main(para):
    if para == "count_timeseries":
        sql('count timeseries')

    elif para == 'count_storage_group':
        sql('count storage group')

    elif para == 'count_seq':
        results = 0
        paths = check_data('data')
        for path in paths.split(','):
            result = int(os.popen('find %s -name \'*.tsfile\' | wc -l' % os.path.join(path, 'sequence')).read())
            results += result
        print(results)

    elif para == 'sum_seq':
        results = 0
        paths = check_data('data')
        for path in paths.split(','):
            result = int(os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1' % os.path.join(path, 'sequence')).read().split('\t')[0])
            results += result
        print(results * 1024)

    elif para == 'count_unseq':
        results = 0
        paths = check_data('data')
        for path in paths.split(','):
            result = int(os.popen('find %s -name \'*.tsfile\' | wc -l' % os.path.join(path, 'unsequence')).read())
            results += result
        print(results)

    elif para == 'sum_unseq':
        results = 0
        paths = check_data('data')
        for path in paths.split(','):
            result = int(os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1' % os.path.join(path, 'unsequence')).read().split('\t')[0])
            results += result
        print(results * 1024)

    elif para == 'count_all':
        results = 0
        paths = check_data('data')
        for path in paths.split(','):
            result = int(os.popen('find %s -name \'*.tsfile\' | wc -l' % path).read())
            results += result
        print(results)

    elif para == 'sum_all':
        results = 0
        paths = check_data('data')
        for path in paths.split(','):
            result = int(os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1' % path).read().split('\t')[0])
            results += result
        print(results * 1024)

    elif para == 'sum_resource':
        results = 0
        paths = check_data('data')
        for path in paths.split(','):
            result = int(os.popen('find %s -name \'*.tsfile.resource\' | xargs du -s -c | tail -n 1' % path).read().split('\t')[0])
            results += result
        print(results * 1024)

    elif para == 'sum_wal':
        if not cf.get('path', 'wal'):
            path = os.path.join(cf.get('path', 'iotdb_home'), 'data/wal')
        else:
            path = cf.get('path', 'wal')
        results = os.popen('du -s %s' % path).read()
        print(int(results.split('\t')[0]) * 1024)

    else:
        error()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        error()
    if not cf.get('path', 'iotdb_home'):
        print('must special iotdb home ')
        exit()
    main(sys.argv[1])

