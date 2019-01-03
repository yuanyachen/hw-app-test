import random, pymysql, redis, os


class HanweiUtil(object):
    def __init__(self):
        pass

    def get_name(self, len=5):
        '''从网页获取姓名'''
        # result = requests.get('http://zhao.resgain.net/name_list.html')
        # doc = pq(result.text)
        # name_t = doc('div .col-xs-12 a').text()
        # print(type(name_t))

        s = (
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V',
            'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v',
            'w', 'x', 'y', 'z')

        name = ''
        for i in range(len):
            name += s[random.randint(0, 51)]
        return name

    def get_mysql_cursor(self):
        '''
        获取数据库连接
        :return: conn
        '''
        return pymysql.connect(
            #host='rm-uf6o788t14snm5j623o.mysql.rds.aliyuncs.com',
            #port=1666,
            # host='106.14.173.153',
            # port=7001,
            user='byyroot',
            password='v7&#5efr&777',
            db='hvmall'
        )

    def get_result_one(self, sql):
        '''
        查询数据库记录
        :param sql:
        :return: 返回一条数据
        '''
        conn = HanweiUtil.get_mysql_cursor(self)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_result_all(self, sql):
        '''
        查询数据库记录
        :param sql:
        :return: 返回所有满足条件的数据
        '''
        conn = HanweiUtil.get_mysql_cursor(self)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def set_data(self, sql):
        '''
        修改数据库数据
        :param sql:
        :return: 返回影响的行数
        '''
        conn = HanweiUtil.get_mysql_cursor(self)
        cursor = conn.cursor()
        effect_row = cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return effect_row

    def get_total_sum(self, total_tuple):
        '''
        根据数据库返回的结果计算总共德分/积分和可用德分/积分
        :param total_tuple:
        :return: 总共德分/积分和可用德分/积分
        '''
        total_sum = 0
        freezed_point_sum = 0
        total_usable = 0
        if total_tuple:  # 判断结果是否为空，为空则不赋值
            for i in (2, 3, 4, 5, 6, 7):
                point = total_tuple[i]
                total_sum += point
            for i in (3, 5, 7):
                point = total_tuple[i]
                freezed_point_sum += point
            total_usable = total_sum - freezed_point_sum  # 用总共和冻结德分/积分计算可用德分/积分
        return total_sum, total_usable

    def float_equal(self, a, b):
        if ((abs(a) - abs(b)) > -0.000001 and (abs(a) - abs(b)) < 0.000001):
            return True
        else:
            return False

    def get_redis_conn(self):
        pool = redis.ConnectionPool(
            host='139.196.98.61',
            port=6679,
            password='09876!@#$',
            db=1,
            decode_responses=True)  # 创建连接池
        return redis.Redis(connection_pool=pool)

    def str_encode(self, str):
        os.chdir(r'E:\appium_po\common')
        mystr = os.popen('java IdTypeHandler encode %s' % str)
        mystr = mystr.read()
        ret = {'code': True}
        if mystr.find('编码值') != -1:
            ret['msg'] = mystr[4:].strip()
        else:
            ret.setdefault('code',False)
            ret['msg'] = '加密失败: %s' % mystr
        return ret


if __name__ == '__main__':
    h = HanweiUtil()
    # r = h.get_redis_conn()
    # aomunt = r.get('26o0n')
    # print(aomunt)
    # print(h.str_encode('26'))

    l = '立减￥5.7 | 服务积分:0.00 | 净值:5.7'.split(' | ')
    print(l)
    print(type(l))