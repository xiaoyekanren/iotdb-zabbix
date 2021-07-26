# coding=utf-8
import os.path
import sys
from configparser import ConfigParser
from iotdb.Session import Session

cf = ConfigParser()
cf.read('config.ini', encoding='utf-8-sig')


def error():
    monitor = 'count_timeseries | count_storage_group | '

    print('必须且只能指定一个参数，参数可以是:')
    print(monitor)
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


def shell():
    iotdb_path = cf.get('path', 'path')

    pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        error()
    para = sys.argv[1]
    if para == "count_timeseries":
        sql('count timeseries')
    elif para == 'count_storage_group':
        sql('count storage group')
    elif para == 'count_seq':
        if not cf.get('path', 'data'):
            seq = os.path.join(cf.get('path', 'home'), 'data/data/sequence')
            print(os.popen('find %s -name \'*.tsfile\' | wc -l' % seq).read())
    elif para == 'sum_seq':
        if not cf.get('path', 'data'):
            seq = os.path.join(cf.get('path', 'home'), 'data/data/sequence')
            print(os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1'.split('\t')[0] % seq).read())
    elif para == 'count_unseq':
        pass
    elif para == 'sum_unseq':
        pass
    elif para == '':
        pass
    else:
        error()
