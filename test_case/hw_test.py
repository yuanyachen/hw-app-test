from selenium.common.exceptions import TimeoutException
from po.dash_page import DriverUtil

du = DriverUtil()
# driver.find_element_by_id('com.hanweiyx.hanwei:id/iv_wx_login').click()
# is_displayed = WebDriverWait(driver, 3, 1, (TimeoutException)).until_not(
#     lambda driver: driver.find_element_by_id('com.hanweiyx.hanwei:id/iv_wx_login').is_displayed())
# print(is_displayed)

if du.driver.is_app_installed('com.hanweiyx.hanwei'):
    try:
        # WebDriverWait(driver, 10, 1).until(
        #     lambda driver: driver.find_element_by_id('com.hanweiyx.hanwei:id/ll_main_tab_mine').click())
        # WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_id('com.hanweiyx.hanwei:id/rl_address').click())

        ''' 
        
            新增/修改/删除收货地址
        '''
        du.address_test()

        '''
            1.进入帮助中心页面
            2.查看常见问题/把页面拉到最下面
            3.查看售后服务/把页面拉到最下面
            4.查看联系我们
            5.查看关于我们
        '''
        du.help_test()

        '''
            1.获取数据库德分积分数据
            2.德分积分查看
        '''
        du.integral_test()

        '''
            1.统计订单
            2.查看全部订单
        '''
        du.count_order()
        du.all_order_test()

        '''
            未搜索到商品
        '''
        du.seek_test('home', '伊夫敢死队风格')

        '''
            统计订单
        '''
        order_front3 = du.count_order()

        '''
            搜索/立即购买/提交订单
            下单成功
        # '''
        seek_ret1 = du.seek_test('home', '伊夫')
        if seek_ret1['status']:
            do3 = du.direct_order()
            do3.__next__()
            du.place_an_order(order_source='is_classification')
            order_behind3 = du.count_order()
            du.logging_out.info('下单前%s  下单后%s' % (order_front3, order_behind3))

        '''
            搜索/立即购买/提交订单
            取消支付
            seek_ret搜索结果
            direct_order是生成器，执行完下单后在返回
        '''
        order_front = du.count_order()
        seek_ret = du.seek_test('home', '伊夫')
        if seek_ret['status']:
            do = du.direct_order()
            do.__next__()
            du.place_an_order(order_source='is_classification')
            try:
                do.__next__()
            except StopIteration:
                pass
            order_behind = du.count_order()

            du.logging_out.info('下单前%s  下单后%s' % (order_front, order_behind))
        # 下单前[[1, '1'], [27, '25'], [1, '1'], [4, 0], [1, '1']]  下单后[[2, '2'], [27, '25'], [1, '1'], [4, 0], [1, '1']]

        '''
            分类页面/立即购买/提交订单
            下单成功
        '''
        rder_front1 = du.count_order()
        do1 = du.direct_order(True)
        do1.__next__()
        du.place_an_order(order_source='is_classification')
        order_behind1 = du.count_order()

        du.logging_out.info('下单前%s  下单后%s' % (rder_front1, order_behind1))

        '''
            分类页面/立即购买/提交订单
            下单成功
        '''
        rder_front2 = du.count_order()
        do2 = du.direct_order(True)
        do2.__next__()
        du.place_an_order(order_source='is_classification', is_cash=True)
        try:
            do2.__next__()
        except StopIteration:
            pass
        order_behind2 = du.count_order()

        du.logging_out.info('下单前%s  下单后%s' % (rder_front2, order_behind2))
        # '''
        #     收藏
        # '''
        seek_ret2 = du.seek_test('category', '伊夫')
        if seek_ret2['status']:
            du.collect_test()

        '''
            搜索商品/加入购物车/编辑
        '''
        seek_ret3 = du.seek_test('home', '伊夫')
        if seek_ret3['status']:
            du.add_car(0)
            du.del_car_product(True)

        '''
            购物车/单件/多件/全部下单
        '''

        for i in ('伊夫', '猫罐头(11种口味任选)70G*12罐', '9月11号上海正初仓'):
            seek_ret4 = du.seek_test('home', i)
            if seek_ret4['status']:
                du.add_car(0)
        car_ret = du.car_order(3)
        if car_ret:  # 判断购物车是否有商品，有商品则下单
            du.place_an_order(order_source='car')

        '''
            1.获取首页秒杀商品信息，抢购进度
            2.获取详情页面秒杀商品信息，抢购进度
            3.获取数据库秒杀商品数据
            4.下单
        '''
        # is_success = du.promotion_test()
        # if is_success:
        #     du.place_an_order(is_readdress=True, is_snap_up=True)

        # SUBMITTED(false), // 已提交 ，未付款
        # CANCELLED(false), // 取消
        # PAID(true), // 已付款 未发货
        # DELIVERY(true), // 发货中
        # SHIPPED(true), // 已发货
        # SUCCESS(true), // 交易成功
        # REFUNDING(false), // 退款申请中
        # COMMENT(true), // 待评价
        # CLOSED(false); // 交易关闭
    except TimeoutException as e:
        du.logging_out.error('等待超时!')
    except Exception as e:
        du.logging_out.exception(e)
    finally:
        du.driver.activate_ime_engine('com.sohu.inputmethod.sogou/.SogouIME')
        du.mysql_util.conn_close()
        du.logging_out.info('end')
        # driver.close_app()
