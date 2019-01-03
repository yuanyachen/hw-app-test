import random, redis, os, logging, time, platform, pymysql, threading


class LoggingUtil(object):
    _instance_lock = threading.Lock()
    logging_out = None
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def get_file_name(name, type):
        '''
        创建截屏文件夹
        判断文件夹是否存在，不存在则创建，生成图片的名字
        :param name:
        :return:
        '''
        separator = HanweiUtil.get_separator()
        root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))  # 获取项目目录
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 生成日期目录
        if 'log' != type:
            file_page = root_path + separator + 'result' + separator + day + separator + type
        else:
            file_page = root_path + separator + 'log' + separator + day + separator + type
        ts = HanweiUtil.get_lcaol_time_str()
        if not os.path.exists(file_page):
            os.makedirs(file_page)
        file_name = file_page + separator + ts + '_' + name + '.' + type
        return file_name

    @staticmethod
    def out_file_log(system_name='app'):
        ''' Output log to file and console '''
        # Define a Handler and set a format which output to file
        logging.basicConfig(
            level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
            format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
            datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
            filename=LoggingUtil.get_file_name(system_name, 'log'),  # log文件名
            filemode='w')  # 写入模式“w”或“a”
        # Define a Handler and set a format which output to console
        console = logging.StreamHandler()  # 定义console handler
        console.setLevel(logging.INFO)  # 定义该handler级别
        formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
        console.setFormatter(formatter)
        # Create an instance
        logging.getLogger().addHandler(console)  # 实例化添加handler
        return logging
        # Print information              # 输出日志级别
        # logging.debug('logger debug message')
        # logging.info('logger info message')
        # logging.warning('logger warning message')
        # logging.error('logger error message')
        # logging.critical('logger critical message')


class RedisUtil(LoggingUtil):
    '''
        redis工具类
    '''
    redis_conn = None

    def __init__(self):
        super(RedisUtil, self).__init__()
        if RedisUtil.redis_conn is None:
            pool = redis.ConnectionPool(
                host='139.196.98.61',
                port=6679,
                password='09876!@#$',
                db=1,
                decode_responses=True)  # 创建连接池
            RedisUtil.redis_conn = redis.Redis(connection_pool=pool)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            if not hasattr(cls, '_instance'):
                cls._instance = super(RedisUtil, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_redis_conn(cls):
        '''  获取链接 '''
        return cls.redis_conn

    @classmethod
    def get_redis_ret(cls, key):
        '''
        获取redis的value
        :param key: key
        :return:
        '''
        super().logging_out.info(key)
        return cls.redis_conn.get(key)


class MysqlUtil(LoggingUtil):
    '''
        数据库工具类
    '''
    cursor = None
    conn = None

    def __init__(self):
        '''
        获取数据库连接
        :return: conn
        '''
        super(MysqlUtil, self).__init__()
        if MysqlUtil.cursor is None:
            MysqlUtil.conn = pymysql.connect(
                # host='rm-uf6o788t14snm5j623o.mysql.rds.aliyuncs.com', port=1666,
                host='106.14.15.46', port=7001,
                user='byyroot',
                password='v7&#5efr&777',

                # host='120.26.162.39', port=3306, user='root', password='ouB8LyxL',
                db='hvmall'
            )
            MysqlUtil.cursor = MysqlUtil.conn.cursor()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            if not hasattr(cls, '_instance'):
                cls._instance = super(MysqlUtil, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_result_one(cls, sql):
        '''
        查询数据库记录
        :param sql:
        :return: 返回一条数据
        '''
        cls.cursor.execute(sql)
        result = cls.cursor.fetchone()
        super().logging_out.info('sql : %s ---> result : %s' % (sql, result))
        return result

    @classmethod
    def get_result_all(cls, sql):
        '''
        查询数据库记录
        :param sql:
        :return: 返回所有满足条件的数据
        '''
        cls.cursor.execute(sql)
        result = cls.cursor.fetchall()
        super().logging_out.info('sql : %s ---> result : %s' % (sql, result))
        return result

    @classmethod
    def set_data(cls, sql):
        '''
        修改数据库数据
        :param sql:
        :return: 返回影响的行数
        '''
        effect_row = cls.cursor.execute(sql)
        cls.conn.commit()
        super().logging_out.info('sql : %s ---> effect_row : %s' % (sql, effect_row))
        return effect_row

    @classmethod
    def conn_close(cls):
        cls.cursor.close()
        cls.conn.close()


class HanweiUtil(MysqlUtil, RedisUtil):
    '''
        工具类
    '''

    def __init__(self):
        super().__init__()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with super()._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(HanweiUtil, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def get_name(len=5):
        '''从网页获取姓名'''
        # result = requests.get('http://zhao.resgain.net/name_list.html')
        # doc = pq(result.text)
        # name_t = doc('div .col-xs-12 a').text()
        # print(type(name_t))

        s = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z')

        name = ''
        for i in range(len):
            name += s[random.randint(0, 51)]
        return name

    @staticmethod
    def float_equal(a, b):
        if ((abs(a) - abs(b)) > -0.000001 and (abs(a) - abs(b)) < 0.000001):
            return True
        else:
            return False

    @staticmethod
    def str_encode(str):
        os.chdir(r'/Users/huangjianbo/py_workspace/appium_po/common')
        mystr = os.popen('java IdTypeHandler encode %s' % str)
        mystr = mystr.read()
        ret = {'code': True}
        if mystr.find('编码值') != -1:
            ret['msg'] = mystr[4:].strip()
        else:
            ret.setdefault('code', False)
            ret['msg'] = '加密失败: %s' % mystr
        return ret

    @staticmethod
    def get_separator():
        '''根据系统获取目录分隔符'''
        if 'Windows' in platform.system():
            separator = '\\'
        else:
            separator = '/'
        return separator

    @staticmethod
    def get_lcaol_time_str():
        '''
        获取系统当前时间的str
        :return:
        '''
        return time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))

    @staticmethod
    def get_total_sum(total_tuple):
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

    def get_cpid(self, ele_text):
        '''
        根据不同的用户来源截取cpid
        :param ele_text: 页面会员id
        :return: 截取的cpid
        '''
        if '(' in ele_text:  # 截取cpid
            return ele_text[-10:-3]
        else:
            return ele_text[-7:]

    def get_customercareerlevel(self, cpid):
        '''
        获取用户身份
        :param cpid: cpid
        :return: 返回用户身份
        '''
        customercareerlevel_tuple = MysqlUtil.get_result_one(
            'select hds_type, hds_subtype, hds_sptype, hds_star,vivilife_type, vivilife_sptype, vivilife_subtype, is_lightening from customercareerlevel where cpId ="%s";' % cpid)  # 获取用户身份信息
        is_direct_ret = MysqlUtil.get_result_one('select is_direct from customerprofile where cpId = "%s";' % cpid)
        is_direct = lambda: is_direct_ret[0] if is_direct_ret is not None else 1
        if customercareerlevel_tuple is not None and (customercareerlevel_tuple[0] in ('RC','DS','SP') or customercareerlevel_tuple[4] in ('RC','DS','SP')):
            if 'SP' == customercareerlevel_tuple[4] or 1 == customercareerlevel_tuple[7]:
                return 'is_lightening'
            elif 'DS' == customercareerlevel_tuple[4] or ('SP' == customercareerlevel_tuple[0] and 'RC' == customercareerlevel_tuple[4] and 0 == is_direct()):
                return 'vip'
        else:
            return 'white'


if __name__ == '__main__':
    h = HanweiUtil()
    m = MysqlUtil()
    print(m.get_result_one('select * from xquark_user'))
    # r = h.get_redis_conn()
    # aomunt = r.get('26o0n')
    # print(aomunt)
    # print(h.str_encode('26'))

    # l = '立减￥5.7 | 服务积分:0.00 | 净值:5.7'.split(' | ')
    # print(l)
    # print(type(l))
    # s = h.str_encode('17535150')
    # print(s)
