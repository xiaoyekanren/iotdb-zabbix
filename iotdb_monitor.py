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
    system = 'SYSTEM: io_tps | io_read_kb_s | io_write_kb_s '

    print('必须且只能指定一个参数，参数可以是:')
    print(count, total, system)
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
            path = os.path.join(cf.get('path', 'home'), 'data/data/sequence')
        else:
            path = cf.get('path', 'data')
        result = os.popen('find %s -name \'*.tsfile\' | wc -l' % path).read()
        print(int(result))
    elif para == 'sum_seq':
        if not cf.get('path', 'data'):
            path = os.path.join(cf.get('path', 'home'), 'data/data/sequence')
        else:
            path = cf.get('path', 'data')
        results = os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1' % path).read()
        print(int(results.split('\t')[0]))
    elif para == 'count_unseq':
        if not cf.get('path', 'data'):
            path = os.path.join(cf.get('path', 'home'), 'data/data/unsequence')
        else:
            path = cf.get('path', 'data')
        result = os.popen('find %s -name \'*.tsfile\' | wc -l' % path).read()
        print(int(result))
    elif para == 'sum_unseq':
        if not cf.get('path', 'data'):
            path = os.path.join(cf.get('path', 'home'), 'data/data/unsequence')
        else:
            path = cf.get('path', 'data')
        results = os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1' % path).read()
        print(int(results.split('\t')[0]))
    elif para == 'count_all':
        if not cf.get('path', 'data'):
            path = os.path.join(cf.get('path', 'home'), 'data/data')
        else:
            path = cf.get('path', 'data')
        result = os.popen('find %s -name \'*.tsfile\' | wc -l' % path).read()
        print(int(result))
    elif para == 'sum_all':
        if not cf.get('path', 'data'):
            path = os.path.join(cf.get('path', 'home'), 'data/data')
        else:
            path = cf.get('path', 'data')
        results = os.popen('find %s -name \'*.tsfile\' | xargs du -s -c | tail -n 1' % path).read()
        print(int(results.split('\t')[0]))
    elif para == 'sum_resource':
        if not cf.get('path', 'data'):
            path = os.path.join(cf.get('path', 'home'), 'data/data')
        else:
            path = cf.get('path', 'data')
        results = os.popen('find %s -name \'*.tsfile.resource\' | xargs du -s -c | tail -n 1' % path).read()
        print(int(results.split('\t')[0]))
    elif para == 'sum_wal':
        if not cf.get('path', 'wal'):
            path = os.path.join(cf.get('path', 'home'), 'data/wal')
        else:
            path = cf.get('path', 'wal')
        results = os.popen('du -s %s' % path).read()
        print(int(results.split('\t')[0]))
    elif para == 'io_tps':
        disk = cf.get('system', 'disk')
        results = os.popen('iostat |grep \'%s\' |awk \'{print $2}\'' % disk).read()
        print(int(results))
    elif para == 'io_read_kb_s':
        disk = cf.get('system', 'disk')
        results = os.popen('iostat |grep \'%s\' |awk \'{print $3}\'' % disk).read()
        print(int(results))
    elif para == 'io_write_kb_s':
        disk = cf.get('system', 'disk')
        results = os.popen('iostat |grep \'%s\' |awk \'{print $4}\'' % disk).read()
        print(int(results))
    elif para == '':
        pass
    else:
        error()
