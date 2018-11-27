from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from common.pub_util import HanweiUtil
from common.slide_swipe import swipe_up

class Base(object):
    driver = None
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '5.1',
        'deviceName': 'HUAWEI TAG-AL00',
        'appPackage': 'com.hanweiyx.hanwei',
        'appActivity': '.activity.SplashActivity',
        'unicodeKeyboard': True,  # 此两行是为了解决字符输入不正确的问题
        'resetKeyboard': True,  # 运行完成后重置软键盘的状态
        'noReset': True}  # 不需要再次安装

    def __init__(self):
        if Base.driver is None:
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.desired_caps)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def me_find_by_id(self, id):
        '''
             重新封装定位方法，添加汉薇元素
        :param id: id
        :return:
        '''
        try:
            web_ele = self.driver.find_element_by_id('com.hanweiyx.hanwei:id/%s' % id)
            return web_ele
        except NoSuchElementException:
            self.driver.save_screenshot(HanweiUtil.get_file_name(id,'png'))

    def find_element(self, loc):
        '''
        重新封装单个元素定位方法
        :param loc:
        :return:
        '''
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except:
            print('%s 页面中未找到 %s 元素' % (self, loc[1]))
            swipe_up(self.driver, 1000, max=0.6)

    def find_elements(self, loc):
        '''
        重新封装一组元素定位方法
        :param loc:
        :return:
        '''
        try:
            if len(self.driver.find_elements(*loc)):
                return self.driver.find_elements(*loc)
        except:
            print('%s 页面中未找到 %s 元素' % (self, loc[1]))

    def send_keys(self, loc, value, clear_first=True, click_first=True):
        '''
        重新封装输入方法
        :param loc:
        :param value:
        :param clear_first:
        :param click_first:
        :return:
        '''
        try:
            if clear_first:
                self.find_element(loc).clear()
            if click_first:
                self.find_element(loc).click()
            self.find_element(loc).send_keys(value)
        except AttributeError:
            print('%s 页面中未找到 %s 元素' % (self, loc[1]))

    def click_button(self, loc, find_first=True):
        '''
        重新封装按钮点击方法
        :param loc:
        :param find_first:
        :return:
        '''
        try:
            if find_first:
                self.find_element(loc)
            self.find_element(loc).click()
        except:
            print('%s 页面未能找到 %s 按钮' % (self, loc[1]))
