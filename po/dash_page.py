import time
from common.slide_swipe import swipe_up, swipe_left
from common.pub_util import HanweiUtil, MysqlUtil,RedisUtil
from selenium.common.exceptions import TimeoutException
from po.base_page import Base
from selenium.webdriver.common.by import By


class DriverUtil(Base):
    def __init__(self, ):
        super(DriverUtil, self).__init__()
        self.mysql_util = MysqlUtil()  # 实例化数据库工具对象
        self.logging_out = HanweiUtil.logging_out # 获取日志对象
        self.driver.implicitly_wait(10)

        # 进入我的页面，获取cpid name customercareerlevel身份信息 is_lightening是否点亮
        self.me_find_by_id('ll_main_tab_mine').click()
        temporary_cpid = self.me_find_by_id('tv_member_id').text
        if '(' in temporary_cpid:  # 截取cpid
            self.cpid = temporary_cpid[-10:-3]
        else:
            self.cpid = temporary_cpid[-7:]
        self.name = self.me_find_by_id('tv_mine_name').text

        customercareerlevel_tuple = self.mysql_util.get_result_one(
            'select hds_type, hds_subtype, hds_sptype, hds_star,vivilife_type, vivilife_sptype, vivilife_subtype, is_lightening from customercareerlevel where cpId ="%s";' % self.cpid)  # 获取用户身份信息
        is_direct_ret = self.mysql_util.get_result_one('select is_direct from customerprofile where cpId = "%s";' % self.cpid)
        is_direct = lambda: is_direct_ret[0] if is_direct_ret is not None else 1
        if customercareerlevel_tuple is not None:
            if 'DS' == customercareerlevel_tuple[4] or ('SP' == customercareerlevel_tuple[0] and 'RC' == customercareerlevel_tuple[4] and 0 == is_direct()):
                self.customercareerlevel = 'vip'
            elif 'SP' == customercareerlevel_tuple[4] or 1 == customercareerlevel_tuple[7]:
                self.customercareerlevel = 'is_lightening'
        else:
            self.customercareerlevel = 'white'
        self.logging_out.info('cpid=%s name=%s customercareerlevel=%s' % (self.cpid, self.name, self.customercareerlevel))

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         cls.__instance = object.__new__(cls, *args, **kwargs)
    #     return cls.__instance

    def get_goods_info(self, is_collect=False, is_promotion=False):
        '''
        获取商品详情页面的商品信息
        :param is_collect: 是否是收藏页面
        :param customercareerlevel: 是否有身份,默认没有
        :param is_promotion: 是否是秒杀商品，秒杀商品不展示立减等字段
        :return:
        '''
        if is_collect:
            goods_info_id = {
                'name': 'tv_name',  # 商品名称
                'price': 'tv_price',  # 商品原价
                'convert': 'tv_product_exchange_price',  # 商品兑换价
                'time': 'tv_time'  # 收藏时间
            }
        else:
            goods_info_id = {
                'name': 'tv_goods_name',  # 商品名称
                'price': 'tv_goods_price',  # 商品原价
                'convert': 'tv_goods_convert',  # 兑换价
                'minus': 'tv_subtract',  # 立减
                'tv_make': 'tv_make'  # 立赚
            }
        goods_info_id['worth'] = 'tv_worth'  # 净值
        goods_info_id['member_price'] = 'tv_member_price'  # 会员价
        goods_info_id['proxy_price'] = 'tv_proxy_price'  # 代理价
        return_dict = {
            'goods_name': self.me_find_by_id(goods_info_id['name']).text,
            'goods_price': self.me_find_by_id('%s' % goods_info_id['price']).text[4:],
            'goods_convert': self.me_find_by_id(goods_info_id['convert']).text[5:-2].split('+'),
            'member_price': self.me_find_by_id(goods_info_id['member_price']).text[5:]
        }
        if 'white' != self.customercareerlevel and not is_promotion:  # 有身份的用户才会在页面上展示代理价 已减 立赚
            try:
                if not is_collect:  # 详情页面有身份的用户 立减和立赚
                    goods_minus = self.me_find_by_id(goods_info_id['minus']).text[2:]
                    tv_make = self.me_find_by_id(goods_info_id['tv_make']).text[3:]
                    return_dict.setdefault('goods_minus', goods_minus)
                    return_dict.setdefault('tv_make', tv_make)
                tv_worth = self.me_find_by_id(goods_info_id['worth']).text[3:]
                proxy_price = self.me_find_by_id(goods_info_id['proxy_price']).text[3:]
                return_dict.setdefault('tv_worth', tv_worth)
                return_dict.setdefault('proxy_price', proxy_price)
            except TimeoutException:
                self.logging_out.error('有身份的用户获取页面详情页面失败！')
        if is_collect:  # 收藏页面 收藏时间
            tv_time = self.me_find_by_id(goods_info_id['time'])
            return_dict.setdefault('tv_time', tv_time)
        return return_dict

    def place_an_order(self,order_source='info', is_cash=False, pay_type='weixin', is_readdress=False, is_snap_up=False):
        '''
        下单
        :param is_cash: 是否现金支付
        :param pay_type: 支付方式 alipay/weixin  默认weixin
        :param is_readdress: 是否修改地址
        :param order_source: 下单来源 car/购物车  is_classification/分类页  info/详情页
        :param is_snap_up 是否是秒杀商品
        :return: 支付详情 商品金额/立省/德分/收益/其他调整/配送费/配送费减免/总计
        '''
        goods_names = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_name')
        goods_prices = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_price')
        goods_numbers = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_number')
        for i in range(len(goods_names)):
            name = goods_names[i].text
            price = goods_prices[i].text[1:]
            goods_number = goods_numbers[i].text[1:]
            discount_fee = '0'
            if 'white' != self.customercareerlevel and not is_snap_up:  # vip和店主在确认订单页面有以减, 抢购页面没有以减字段
                discount_fees = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_discount_fee')
                discount_fee = discount_fees[i].text[3:-1]
            self.logging_out.info('商品%s购买了%s件, 合计%s元, 以减%s元' % (name, goods_number, price, discount_fee))

        if is_readdress:
            DriverUtil.address_test(self, is_redact=False)
        else:
            time.sleep(1)
        swipe_up(self.driver, 500, max=0.75)
        tv_user_point = self.me_find_by_id('tv_user_point').text[10:]  # 获取德分
        tv_user_commission = self.me_find_by_id('tv_user_commission').text[10:]  # 获取收益
        # 判断收益不为0且不是全收益兑换，将页面取到的收益转换成float，减去0.01后保留两位小数，在转回str
        if '0' != tv_user_commission and is_cash:
            tv_user_commission = str(round(float(tv_user_commission) - 0.01, 2))

        # 输入德分/收益
        for i in ((tv_user_point, 'score_switch', 'et_score'), (tv_user_commission, 'integral_switch', 'et_integral')):
            if '0' != i[0]:
                self.me_find_by_id(i[1]).click()
                self.me_find_by_id(i[2]).clear().send_keys(i[0])

        loc_name = ['goods_fee', 'score_fee', 'integral_fee', 'pay_other', 'logistics_fee',
                    'pay_remission', 'total_price']
        if 'white' != self.customercareerlevel and not is_snap_up:  # vip和店主在确认订单页面有立减, 抢购页面没有以减字段
            loc_name.insert(1, 'discount_fee')
        order_pay_info = {}  # 获取页面支付详情 商品金额/立省/德分/收益/其他调整/配送费/配送费减免/总计
        for i in loc_name:
            if 'total_price' != i:
                order_pay_info.setdefault(i, self.me_find_by_id('tv_%s' % i).text[2:])
            else:
                order_pay_info.setdefault(i, self.me_find_by_id('tv_%s' % i).text[1:])
        self.logging_out.info('确认订单页面结算金额详情： %s' % order_pay_info)
        self.me_find_by_id('cb_%s' % pay_type).click()  # 选择支付方式
        tv_total_price = self.me_find_by_id('tv_total_price').text[1:]  # 获取合计金额
        self.me_find_by_id('tv_confirm').click()  # 提交订单
        if is_cash and 'weixin' == pay_type or not HanweiUtil.float_equal(float(tv_total_price), 0.00):
            self.driver.wait_activity('com.tencent.mm.plugin.wallet.pay.ui.WalletPayUI', 20)
            self.driver.tap([(16, 50), (64, 146)], 100)  # 取消支付
            self.me_find_by_id('iv_back').click()  # 返回上一页，一直到首页
            if 'car' != order_source:  # 不是从购物车下单的需要点击商品详情页面的返回按钮
                self.me_find_by_id('ll_back').click()
                if 'is_classification' == order_source:
                    self.me_find_by_id('iv_back').click()
            # self.driver.tap([(32, 481), (688, 577)], 100)  # 立即支付
            # for i in (
            #         [(40, 730), (200, 800)], [(40, 850), (200, 920)],
            #         [(40, 960), (200, 990)], [(260, 730), (450, 800)],
            #         [(260, 850), (450, 920)],[(260, 900), (450, 990)]):
            #     time.sleep(random.randint(1, 2))
            #     self.driver.tap(i, random.randint(100, 900))
            #
            #
            # time.sleep(5)
            # self.driver.tap([(320,645), (448,705)], 500)  # 重试
            # self.driver.tap([(41,109), (101,169)], 500)  # 支付成功返回商家[41,109][101,169]

    def seek_test(self, entrance, product_name, click=False):
        '''
        搜索,进入商品详情页面
        :param entrance: home/category 首页或分类
        :param click: 分类页面点击键盘搜索/点击页面按钮搜索
        :return:
        '''
        self.me_find_by_id('ll_main_tab_%s' % entrance).click()
        if 'category' == entrance:
            self.me_find_by_id('iv_search').click()
        self.driver.activate_ime_engine('io.appium.android.ime/.UnicodeIME')
        self.me_find_by_id('et_search').clear().send_keys(product_name)
        ret = {'status': True, 'msg': '搜索成功！'}
        if click and 'home' != entrance:
            self.me_find_by_id('tv_search').click()
        else:
            self.driver.activate_ime_engine('com.sohu.inputmethod.sogou/.SogouIME')
            time.sleep(2)
            self.driver.keyevent('66')
        self.driver.activate_ime_engine('io.appium.android.ime/.UnicodeIME')
        try:
            self.me_find_by_id('rl_item').click()
        except Exception:
            re_text = self.driver.find_element_by_xpath('//*[@text="没找到相关的物品"]').text
            self.me_find_by_id('iv_back').click()
            ret['status'] = False
            ret['msg'] = re_text
        finally:
            self.logging_out.info(ret)
            return ret

    def collect_test(self):
        '''
         1.从数据库查询有没有收藏改商品，如有就清除
         2.收藏商品
         3.移除收藏
         4.有身份的有户展示省和净值
        :return:
        '''
        # 清除所有收藏商品
        close_all_sql = 'UPDATE xquark_product_collection set archive = 1 where archive = 0 and user_id in (SELECT id FROM xquark_user where cpid = "%s");' % self.cpid
        # 清除实习医生
        # set_sql_one = 'UPDATE xquark_product_collection set archive = 1 where archive = 0 and user_id in (SELECT id FROM xquark_user where product_id = "2795");'
        get_one_sql = 'select * from xquark_product_collection where archive = 0 and user_id in (SELECT id FROM xquark_user where product_id = "2795");'
        collect_result = self.mysql_util.get_result_one(get_one_sql)
        if collect_result:
            effect_row = self.mysql_util.set_data(close_all_sql)
            self.logging_out.info('取消收藏%s件' % effect_row)

        self.me_find_by_id('ll_collect').click()  # 收藏/取消
        collect_result = self.mysql_util.get_result_one(get_one_sql)
        if collect_result:
            self.logging_out.info('收藏成功！')
        self.me_find_by_id('ll_back').click()
        self.me_find_by_id('iv_back').click()
        self.me_find_by_id('ll_main_tab_mine').click()
        self.me_find_by_id('tl_collect').click()

        collect_goods_info = DriverUtil.get_goods_info(self, True)
        self.logging_out.info(collect_goods_info)

        self.me_find_by_id('iv_delete').click()  # 取消收藏
        collect_result = self.mysql_util.get_result_one(get_one_sql)
        if not collect_result:
            self.logging_out.info('取消收藏成功！')
        self.me_find_by_id('iv_back').click()

    def close_car(self):
        '''
        数据库清空购物车
        :return:
        '''
        get_all_sql = 'select * from xquark_cart_item where archive = 0 and user_id in (SELECT id FROM xquark_user where cpid = "%s");' % self.cpid
        close_all_sql = 'UPDATE xquark_cart_item set archive = 1 where archive = 0 and user_id in (SELECT id FROM xquark_user where cpid = "%s");' % self.cpid
        result_all = self.mysql_util.get_result_all(get_all_sql)
        if len(result_all):
            effect_row = self.mysql_util.set_data(close_all_sql)
            self.logging_out.info('清除购物车%s件商品' % effect_row)
        self.me_find_by_id('ll_main_tab_shopping_car').click()
        t = self.me_find_by_id('tv_empty').text
        self.logging_out.info(t)

    def add_car(self, num):
        '''
        添加购物车
        :param num:添加的数量
        :return:
        '''
        cart_count1 = self.me_find_by_id('tv_cart_count').text
        fun_id = lambda: 'tv_caucasian_add_cart' if 'white' == self.customercareerlevel else 'll_identity_add'  # 判断白人和VIP用户页面的加入购物车按钮
        self.me_find_by_id(fun_id()).click()
        sku_price = self.me_find_by_id('tv_sku_price').text[1:]
        store_count = self.me_find_by_id('tv_cart_count').text[2:-1]
        self.logging_out.info('价格:%s 库存:%s' % (sku_price, store_count))
        for i in range(num):
            self.me_find_by_id('iv_add_amount').click()
        self.me_find_by_id('tv_confirm').click()
        cart_count2 = self.me_find_by_id('tv_cart_count').text
        cart_count = (int(cart_count2) - int(cart_count1))
        self.logging_out.info('添加前:%s 添加后:%s 添加%s件' % (cart_count1, cart_count2, cart_count))
        self.me_find_by_id('ll_back').click()
        self.me_find_by_id('iv_back').click()

    def del_car_product(self, edit, check='all_checkBox'):
        '''
        编辑购物车页面
        :param edit: 编辑/滑动删除
        :param check: 单个删除/全部删除  cb_product/all_checkBox
        :return:
        '''
        self.me_find_by_id('ll_main_tab_shopping_car').click()
        if edit:
            self.me_find_by_id('tv_edit').click()
            self.me_find_by_id(check).click()
            s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_delete')
            for i in range(2, 0, -1):
                s[len(s) - 1].click()  # 每个商品下面都又隐藏的删除按钮，获取页面所有删除按钮，取最后一个按钮
                message = self.driver.find_element_by_id('android:id/message').text
                self.logging_out.info(message)
                self.driver.find_element_by_id('android:id/button%s' % i).click()

        else:
            swipe_left(self.driver, 1000, min=0.3, max=0.8, y_ratio=0.2)
            self.me_find_by_id('tv_delete').click()

    def category_test(self):
        '''
        循环查看全部分类的每一个分类
        :return:
        '''
        self.me_find_by_id('ll_main_tab_category').click()
        sql = 'select name from xquark_category where taxonomy = "GOODS" and parent_id is not null and archive = 0 ORDER BY idx;'
        category_name_tuple = self.mysql_util.get_result_all(self, sql)
        i = 0
        for name_tuple in category_name_tuple:
            if i == 11:
                swipe_up(self.driver, 500, max=0.75)
            self.driver.find_element_by_xpath(
                '//android.widget.TextView[contains(@text, "%s")]' % name_tuple[0]).click()
            self.me_find_by_id('iv_back').click()
            i += 1

    def direct_order(self, is_category=False):
        '''
        直接下单
        :param is_category: 是否从分类页面下单 True是, false搜索下单
        :return:
        '''
        if is_category:
            self.me_find_by_id('ll_main_tab_category').click()
            self.me_find_by_id('ll_right_item').click()
            self.me_find_by_id('rl_item').click()

        goods_info = DriverUtil.get_goods_info(self)
        self.logging_out.info(goods_info)
        if 'white' == self.customercareerlevel:  # 白人下单
            self.me_find_by_id('tv_caucasian_shop_now').click()
        else:  # VIP/店主
            self.me_find_by_id('ll_buy').click()
        self.me_find_by_id('tv_confirm').click()
        yield
        self.logging_out.info('取消支付！')

    def address_test(self, is_redact=True):
        '''
        1.进入我的页面/地址管理页面
        2.添加新地址/判断是否添加成功，信息是否一致
        3.修改地址
        4.删除地址/通过获取修改的名字和最新的第一个的名字对比
        :param is_redact: True 地址管理 / False 确认订单页面修改地址
        :return:
        '''
        self.me_find_by_id('rl_address').click()  # 进入地址管理页面
        new_name = HanweiUtil.get_name()
        self.me_find_by_id('tv_add_new_address').click()
        DriverUtil.set_address(self, new_name, 'new')
        if not is_redact:
            self.me_find_by_id('tv_redact').click()
        self.me_find_by_id('ll_modify_address').click()
        set_name = HanweiUtil.get_name()
        DriverUtil.set_address(self, set_name, 'set')
        self.me_find_by_id('ll_delete_address').click()
        self.driver.find_element_by_id('android:id/button1').click()
        one_name = self.me_find_by_id('tv_addressee').text
        if set != one_name:
            self.logging_out.info('删除地址测试通过！')
        self.me_find_by_id('iv_back').click()  # 返回我的页面

    def set_address(self, name, set_type):
        '''
        新增/修改地址
        :param name: 收货人姓名
        :param type: 新增/修改
        :return:
        '''
        self.driver.activate_ime_engine('io.appium.android.ime/.UnicodeIME')
        self.me_find_by_id('et_addressee').clear().send_keys(name)
        self.me_find_by_id('et_phone').clear().send_keys('13300000000')
        self.me_find_by_id('tv_address').click()
        self.me_find_by_id('tv_confirm').click()
        self.me_find_by_id('et_detail_address').clear().send_keys('啊啊啊啊啊啊啊啊啊')
        self.me_find_by_id('sw_isdefault').click()
        self.me_find_by_id('tv_save').click()
        time.sleep(2)
        ret = '%s失败！' % set_type
        if name == self.me_find_by_id('tv_addressee').text:
            if 'set' == set_type:
                ret = '%s地址测试通过！' % set_type
            elif 'new' == set_type:
                if '[默认地址]' == self.me_find_by_id('tv_default').text:
                    ret = '%s地址测试通过！' % set_type
        self.logging_out.info(ret)

    def car_order(self, num):
        '''
        :param num: 1件/2件/3全部
        :return:
        '''
        self.me_find_by_id('ll_main_tab_shopping_car').click()
        time.sleep(2)
        try:
            self.logging_out.info(self.me_find_by_id('tv_empty').text)
            return False
        except Exception:
            if 3 == num:
                self.me_find_by_id('all_checkBox').click()
            elif 1 == num:
                self.me_find_by_id('cb_product').click()
            elif 2 == num:
                s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/cb_product')
                for i in range(num):
                    s[i].click()
            product_names = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_name')
            goods_prices = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_price')
            cart_counts = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_cart_count')
            total_price_s = 0
            for i in range(len(product_names)):
                product_name = product_names[i].text
                goods_price = goods_prices[i].text[1:]
                cart_count = cart_counts[i].text
                total_price_s += float(goods_price) * int(cart_count)
                self.logging_out.info('商品%s 单价%s 购买%s件 ' % (product_name, goods_price, cart_count))
            while True:
                total_price = self.me_find_by_id('total_price').text[1:]
                if '计算中' in total_price:
                    continue
                elif HanweiUtil.float_equal(total_price_s, float(total_price)):
                    break
                else:
                    self.logging_out.info('商品合计金额%s, 页面显示合计金额%s' % (total_price_s, total_price))
                    break

            pay_value = self.me_find_by_id('go_pay').text[3:-1]
            time.sleep(3)
            self.me_find_by_id('go_pay').click()
            message = self.driver.find_element_by_id('android:id/message').text
            self.driver.find_element_by_id('android:id/button2').click()
            self.me_find_by_id('go_pay').click()
            self.driver.find_element_by_id('android:id/button1').click()
            self.logging_out.info('共计%s %s种商品' % (total_price, pay_value))
            self.logging_out.info(message)
            return True

    def count_order(self):
        '''
        统计订单
        :param cpid:
        :return: 分类订单统计
        '''
        self.me_find_by_id('ll_main_tab_mine').click()
        status_s = (
            ('SUBMITTED', 'tv_obligation_number'), ('PAID","DELIVERY', 'tv_shipments_number'),
            ('SHIPPED', 'tv_receiving_number'),
            ('SUCCESS","COMMENT',), ('REFUNDING', 'tv_sale_number'))
        order_count = []
        for status in status_s:
            sql = 'select count(*) from xquark_order where archive = 0 and status in ("%s") and buyer_id in (select id from xquark_user where cpId = "%s")' \
                  % (status[0], self.cpid)
            result = self.mysql_util.get_result_one(sql)
            if result[0] > 0 and 'SUCCESS","COMMENT' != status[0]:
                order_count.append(
                    [result[0], self.me_find_by_id(status[1]).text])
            else:
                order_count.append([result[0], 0])
        return order_count

    def all_order_test(self):
        '''
        查看全部订单
        :param cpid:
        :return:
        '''

        self.me_find_by_id('look_order').click()

        # sel_order_sum_sql = 'select count(*) from xquark_order where archive = 0 and buyer_id in (select id from xquark_user where cpId = "%s")' % cpid
        # order_sum = self.mysql_util.get_result_one(sel_order_sum_sql)
        # int(order_sum[0] / 2)循环所有 但是在滑动屏幕的时候不好控制，所以只获取每页的第一个
        for i in range(1):
            order_no_s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_order_time')
            goods_name_s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_name')
            goods_price_s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_price')
            order_fee_s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_order_fee')
            goods_number_s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_goods_number')
            order_status_s = self.driver.find_elements_by_id('com.hanweiyx.hanwei:id/tv_order_status')

            try:
                empty_text = self.me_find_by_id('tv_empty').text
                self.logging_out.info(empty_text)
            except Exception:
                for i in range(2):
                    order_no = order_no_s[i].text
                    order_info_sql = 'select xoi.product_name, xoi.market_price,xo.total_fee,xoi.amount,xo.status from xquark_order xo LEFT JOIN xquark_order_item xoi on(xo.id = xoi.order_id) where xo.order_no = "%s";' % order_no[
                                                                                                                                                                                                                             5:]
                    order_info = self.mysql_util.get_result_one(order_info_sql)
                    self.logging_out.info(order_info)
                    if not order_info:
                        self.logging_out.info('查询订单失败！')
                        break
                    self.logging_out.info('%s 商品名称:[%s:%s] 商品原价:[%s:%s] 支付金额:[%s:%s] 购买数量:[%s:%s] 订单状态:[%s:%s]'
                                          % (order_no, goods_name_s[i].text, order_info[0], goods_price_s[i].text, order_info[1],
                                             order_fee_s[i].text, order_info[2], goods_number_s[i].text, order_info[3],
                                             order_status_s[i].text, order_info[4]))
                swipe_up(self.driver, 1000, 0.25, 0.74)
        self.me_find_by_id('iv_back').click()

    def help_test(self):
        '''
        帮助中心测试
        :return:
        '''
        self.me_find_by_id('rl_help').click()
        if '帮助中心' == self.me_find_by_id('tv_title').text:
            directory_name_t = (
                ('com.hanweiyx.hanwei:id/rl_issue', '常见问题'), ('com.hanweiyx.hanwei:id/rl_after_sale', '售后服务'),
                ('com.hanweiyx.hanwei:id/rl_contact', '联系我们'), ('com.hanweiyx.hanwei:id/rl_about', '关于我们'))
            for i in directory_name_t:
                DriverUtil.examine_test(self, i[0], i[1])
        self.me_find_by_id('iv_back').click()

    def integral_test(self):
        '''
        1.获取数据库德分收益数据
        2.德分收益查看
        :return:
        '''
        # 获取数据库德分总计和可用
        point_total_sql = 'select * from pointTotal where cpId = %s and status = "ACTIVE";' % self.cpid
        point_total_tuple = self.mysql_util.get_result_one(point_total_sql)
        point_total_sum, point_total_usable = HanweiUtil.get_total_sum(point_total_tuple)

        # 获取数据库收益总计和可用
        commission_total_sql = 'select * from commissionTotal where cpId = %s and status = "ACTIVE";' % self.cpid
        commission_total_tuple = self.mysql_util.get_result_one(commission_total_sql)
        commission_total_sum, commission_total_usable = HanweiUtil.get_total_sum(commission_total_tuple)

        ll_id = (('com.hanweiyx.hanwei:id/ll_score', '我的德分', (round(point_total_sum, 2), round(point_total_usable, 2))),
                 ('com.hanweiyx.hanwei:id/ll_integral', '我的收益',
                  (round(commission_total_sum, 2), round(commission_total_usable, 2))))
        for i in ll_id:
            DriverUtil.examine_test(self, i[0], i[1], *i[2])

    def examine_test(self, directory_name_id, title, *args):
        '''
        帮助中心和我的德分收益页面测试
        :param directory_name_id: 测试页面入口id
        :param title:测试页面title
        :param args:德分收益专用/总分可用分
        :return:
        '''
        self.driver.find_element_by_id(directory_name_id).click()
        if title == self.me_find_by_id('tv_title').text:
            if title in ('常见问题', '售后服务'):  # 如果是'常见问题', '售后服务' 则上拉
                swipe_up(self.driver, 300)
            elif title in ('我的德分', '我的收益'):  # 如果是'我的德分', '我的收益' 则判断总分和可用分是否和数据库一致
                tv_point_total = self.me_find_by_id('tv_point_total').text[:-1]
                tv_point_usable = self.me_find_by_id('tv_point_usable').text[:-1]

                for i in [(args[0], tv_point_total, '总'), (args[1], tv_point_usable, '可用')]:
                    if HanweiUtil.float_equal(float(i[0]), float(i[1])):
                        self.logging_out.info('%s的%s分正确, [%s:%s]' % (title, i[2], i[0], i[1]))
                    else:
                        self.logging_out.info('%s的%s分错误, [%s:%s]' % (title, i[2], i[0], i[1]))
            self.logging_out.info('%s页打开正常！' % title)
        else:
            self.logging_out.info('%s页打开出错！' % title)
        self.me_find_by_id('iv_back').click()  # 返回我的页面

    def promotion_test(self):
        '''
        秒杀商品测试
        :return:
        '''
        self.click_button((By.ID, 'com.hanweiyx.hanwei:id/ll_main_tab_home'))
        self.click_button((By.ID, 'com.hanweiyx.hanwei:id/tv_buy_amount'))
        page_for_details = self.get_goods_info(is_promotion=True)

        # 获取秒杀商品数据
        sql = 'select pos.promotion_id,pos.amount,p.name ' \
            'from xquark_promotion_flash_sale pos LEFT JOIN xquark_product p on (pos.product_id = p.id) ' \
            'LEFT JOIN xquark_promotion xp on (pos.promotion_id = xp.id) ' \
            'where NOW() BETWEEN xp.valid_from and xp.valid_to and  xp.closed = 0 ' \
            'ORDER BY pos.created_at desc'
        promotion_info = self.mysql_util.get_result_one(sql)
        self.logging_out.info('页面商品名称: %s, 数据库: %s' % (page_for_details.get('goods_name'), promotion_info[2]))
        promotion_ciphertext = HanweiUtil.str_encode(promotion_info[0])
        self.logging_out.info(promotion_ciphertext)

        # 获取user_id,在获取改用户是否还可以购买该秒杀商品
        sql = 'select id from xquark_user where cpid = "%s";' % self.cpid
        user_id_ret = self.mysql_util.get_result_one(sql)
        user_id_tuple = lambda: user_id_ret if user_id_ret is not None else (0,)
        user_id_encode_info = HanweiUtil.str_encode(user_id_tuple()[0])

        r = RedisUtil()
        is_success = False
        if not promotion_ciphertext.get('code', None) or not user_id_encode_info.get('code', None):
            self.logging_out.info('key混淆加密失败！')
        else:
            promotion_id = promotion_ciphertext['msg']
            amount = r.get_redis_ret('%s:amount' % promotion_id)  # 剩余可购买件数
            limit_amount = r.get_redis_ret('%s:limitAmount' % promotion_id)  # 单个人购买限制数量
            r_result = r.get_redis_ret('%s:%s' % (user_id_encode_info['msg'], promotion_id))  # 用户已经购买的数量，空为没有购买
            lambda_fun = lambda: r_result if r_result else '0'
            purchase_num = lambda_fun()
            if int(amount) < 0 or int(limit_amount) <= int(purchase_num):
                self.logging_out.info('剩余可购买件数:%s 单个人购买限制数量:%s 用户已经购买的数量%s' % (amount, limit_amount, purchase_num))
                self.me_find_by_id('ll_back').click()
            else:
                self.click_button((By.ID, 'com.hanweiyx.hanwei:id/tv_caucasian_shop_now'))
                self.click_button((By.ID, 'com.hanweiyx.hanwei:id/tv_confirm'))
                self.driver.save_screenshot(HanweiUtil.get_file_name('商品详情', 'png'))  # 获取屏幕截图
                is_success = True
        return is_success


if __name__ == '__main__':
    # hu = HanweiUtil()
    # name = hu.get_name()
    # self.logging_out.info(name)

    # sql = 'select name from xquark_category where taxonomy = "GOODS";'
    # product_name = hu.get_result_all(sql)
    # for i in product_name:
    #     self.logging_out.info(i[0])

    # tv_user_commission = str(round(float('0.1') - 0.01, 2))
    # self.logging_out.info('%s : %s' % (type(tv_user_commission), tv_user_commission))
    # self.logging_out.info(random.randint(100, 400))

    # get_sql_all = 'select * from xquark_cart_item where archive = 0 and user_id in (SELECT id FROM xquark_user where cpid = "3000178");'
    # result_all = hu.get_result_all(get_sql_all)
    # self.logging_out.info(result_all)
    # self.logging_out.info(len(result_all))

    # status_s = ('SUBMITTED', 'PAID', 'SHIPPED', 'SUCCESS","COMMENT', 'REFUNDING') #","DELIVERY
    # order_count = []
    # for status in status_s:
    #     sql = 'select count(*) from xquark_order where archive = 0 and status in ("%s") and buyer_id in (select id from xquark_user where cpId = "%s")' % (
    #         status, '3000178')
    #     result = hu.get_result_one(sql)
    #     order_count.append(result[0])M2dHV8%YWMJi
    # self.logging_out.info(order_count)

    # exp1 = lambda: 1 if 1 == 1 else 0
    # self.logging_out.info(exp1())
    # fun_id = lambda: 'tv_add_cart' if 'white' == 'white' else 'll_identity_add'
    # print(fun_id())
    user_id_ret = (1,)
    user_id_tuple = lambda: user_id_ret if user_id_ret is not None else (0,)
    print(user_id_tuple()[0])
