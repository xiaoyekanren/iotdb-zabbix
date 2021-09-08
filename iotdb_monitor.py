# coding=utf-8
import os
import sys
from configparser import ConfigParser
from iotdb.Session import Session

cf = ConfigParser()
cf.read(os.path.join(sys.path[0], 'config.ini'), encoding='utf-8-sig')

result = 0


def error():
    count = 'COUNT: count_timeseries | count_storage_group | count_seq | count_unseq | count_all | count_seq_lv0 | count_unseq_lv0\n'
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


def get_path(path):
    """
    返回wal路径，返回一个路径字符串；
    返回data路径，返回的是一个需要split(',')的字符串；
    """
    if path == 'wal':
        if not cf.get('path', path):
            return os.path.join(cf.get('path', 'iotdb_home'), 'data/wal')
        else:
            return cf.get('path', path)
    if path == 'data':
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


def merge_path(cur, name):
    return os.path.join(cur, name)


def scan(mode, path, extension_name):
    cur_folder, cur_file, count_cur_file, count_cur_folder, cur_size = [], [], 0, 0, 0
    cur_all_file = os.listdir(path)

    if mode == 'count':
        for i in cur_all_file:
            abs_file = merge_path(path, i)
            if os.path.isfile(abs_file):
                if i.split('.')[-1] == extension_name:
                    count_cur_file += 1
                # cur_file.append(path)  # 文件列表，可打开注释
            else:
                count_cur_folder += 1
                cur_folder.append(abs_file)
        return count_cur_folder, cur_folder, count_cur_file
    elif mode == 'sum':
        for i in cur_all_file:
            abs_file = merge_path(path, i)
            if os.path.isfile(abs_file):
                if i.split('.')[-1] == extension_name:
                    cur_size += os.path.getsize(abs_file)
                    print(cur_size)
            else:
                count_cur_folder += 1
                cur_folder.append(abs_file)
        return count_cur_folder, cur_folder, cur_size


def loop(mode, folders, extension_name):
    global result
    for one_path in list(folders):
        count_cur_folder, cur_folder, mode_result = scan(mode, one_path, extension_name)
        result += mode_result
        if count_cur_folder > 0:
            loop(mode, cur_folder, extension_name)


def master(mode, item, extension_name):
    """
    :param mode: count、sum  # 统计大小，还是统计数量
    :param item: wal、data  # 统计的wal，还是data
    :param extension_name:  # 判断的文件拓展名，tsfile 还是 resource
    :return:
    """
    global result
    if item == 'wal':
        loop(mode, get_path(item), extension_name)
        return result
    elif item == 'data':
        for path in get_path('data').split(','):
            loop(mode, path.split(), extension_name)
    elif item == 'sequence' or item == 'unsequence':
        for path in get_path('data').split(','):
            loop(mode, str(os.path.join(path, item)).split(), extension_name)
    print(result)
    result = 0


def main(para):
    if para == "count_timeseries":  # 统计时间序列数量
        sql('count timeseries')

    elif para == 'count_storage_group':  # 统计存储组数量
        sql('count storage group')

    elif para == 'count_seq':  # 统计顺序tsfile数量
        print(data_tsfile_count('sequence'))
        master('count', 'sequence', 'tsfile')

    elif para == 'sum_seq':  # 统计顺序tsfile大小
        print(data_tsfile_sum('sequence'))
        master('sum', 'sequence', 'tsfile')

    elif para == 'count_unseq':  # 统计乱序tsfile数量
        print(data_tsfile_count('unsequence'))
        master('count', 'unsequence', 'tsfile')

    elif para == 'sum_unseq':  # 统计乱序tsfile大小
        print(data_tsfile_sum('unsequence'))
        master('sum', 'unsequence', 'tsfile')

    elif para == 'count_all':  # 统计全部tsfile数量
        print(data_tsfile_count(''))
        master('count', 'data', 'tsfile')

    elif para == 'sum_all':  # 统计全部tsfile大小
        print(data_tsfile_sum(''))
        master('sum', 'data', 'tsfile')

    elif para == 'sum_resource':  # 统计全部resource文件大小
        print(data_resource_sum())
        master('sum', 'data', 'resource')

    elif para == 'count_resource':  # 统计全部resource数量
        master('count', 'data', 'resource')

    elif para == 'sum_wal':  # 统计wal文件夹大小
        pass
        # print(wal_sum())

    elif para == 'count_seq_lv0':  # 统计全部顺序0层tsfile大小
        pass
        # print(data_tsfile_level_count('sequence'))

    elif para == 'count_unseq_lv0':  # 统计全部乱序tsfile大小
        pass
        # print(data_tsfile_level_count('unsequence'))

    else:
        error()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        error()
    if not cf.get('path', 'iotdb_home'):
        print('must special iotdb home ')
        exit()
    main(sys.argv[1])

