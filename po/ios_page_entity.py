class TabBarPage(object):
    '''底部标签'''
    home_loc = {'accessibility_id': '首页'}  # 首页
    category_loc = {'accessibility_id': '分类'}  # 分类
    hb_loc = {'accessibility_id': '汉宝社区'}  # 汉宝社区
    car_loc = {'accessibility_id': '购物车'}  # 购物车
    my_loc = {'accessibility_id': '我的'}  # 我的


class SearchPage(TabBarPage):
    '''搜索页面'''
    other_back_loc = {'predicate': "type == 'XCUIElementTypeButton' AND label == 'other back'"}  # 返回
    search_box_loc = {'elements_by_class_name': 'XCUIElementTypeTextField'}  # 搜索框
    search_button_loc = {'accessibility_id': '搜索'}  # 搜索按钮
    search_trash_loc = {'predicate': "type == 'XCUIElementTypeButton' and label == 'search trash'"}  # 删除搜索记录
    search_eye_loc = {'predicate': "type == 'XCUIElementTypeButton' and label == 'search eye'"}  # 搜索的眼睛 功能没有实现
    search_list_loc = \
        {'elements_by_ios_predicate': "type == 'XCUIElementTypeButton' and label != 'other back' and label != 'search trash' and label != 'search eye'"}  # 历史记录和热门搜索


class HomePage(TabBarPage):
    '''首页'''
    search_box_loc = {'predicate': "type == 'XCUIElementTypeTextField' and value == '伊夫黎雪'"}  # 搜索框
    buy_now_loc = {'predicate': "type == 'XCUIElementTypeButton' and label = '立即购买"}  # 立即购买
    to_view_all_loc = {'predicate': "type == 'XCUIElementTypeButton' and label = '查看全部"}  # 查看全部
    product_list_loc = {'elements_by_ios_predicate': 'value BEGINSWITH "兑换价:" and value ENDSWITH "德分"'}  # 首页商品列表


class MyPage(TabBarPage):
    '''我的'''
    members_id_loc = {'predicate': 'value BEGINSWITH "会员ID："'}  # cpid
    name_loc = {'xpath': '//XCUIElementTypeStaticText[2]'}  # 用户名
    total_loc = {'elements_by_ios_predicate': "type == XCUIElementTypeStaticText and value ENDSWITH '分'"}  # 德分列表
    earnings_loc = {'elements_by_ios_predicate': "type == XCUIElementTypeStaticText and value ENDSWITH '元'"}  # 收益列表
    all_order_loc = {'accessibility_id': '全部订单'}  # 全部订单
    pay_order_loc = {'accessibility_id': '待付款'}  # 待付款
    delivery_loc = {'accessibility_id': '待发货'}  # 待发货
    receiving_loc = {'accessibility_id': '待收货'}  # 待收货
    completed_loc = {'accessibility_id': '已完成'}  # 已完成
    after_sales_loc = {'accessibility_id': '售后中'}  # 售后中
    spell_loc = {'accessibility_id': '我的拼团'}  # 我的拼团
    address_loc = {'accessibility_id': '地址管理'}  # 地址管理
    collection_loc = {'accessibility_id': '我的收藏'}  # 我的收藏
    results_loc = {'accessibility_id': '我的业绩'}  # 我的业绩
    help_loc = {'accessibility_id': '帮助中心'}  # 帮助中心
    tourists_loc = {'accessibility_id': '游客足迹'}  # 游客足迹
    out_loc = {'accessibility_id': '退出登录'}  # 退出登录
