from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from common.pub_util import HanweiUtil,LoggingUtil
from common.slide_swipe import swipe_up

class Base(object):
    driver = None
    android_desired_caps = {
        'platformName': 'Android',
        'platformVersion': '5.1',
        'deviceName': 'HUAWEI TAG-AL00',
        'appPackage': 'com.hanweiyx.hanwei',
        'appActivity': '.activity.SplashActivity',
        'unicodeKeyboard': True,  # 此两行是为了解决字符输入不正确的问题
        'resetKeyboard': True,  # 运行完成后重置软键盘的状态
        'noReset': True}  # 不需要再次安装

    ios_desired_caps = {
        'platformName': 'iOS',
        'platformVersion': '12.1',
        'deviceName': 'iphone 5s',
        'udid': '994359ed0027816a7c265006209365ea78dc15d1',
        # 'realDeviceLogger': '/usr/local/lib/node_modules/deviceconsole/deviceconsole',
        'bundleId': 'com.hanweiyx.hanweishopping',
        'newCommandTimeout': 60,
        'automationName': 'appium',
        'noReset': True,
        "xcodeOrgId": "<Team ID>",
        "xcodeSigningId": "iPhone Developer"
    }

    def __init__(self,system):
        if Base.driver is None:
            if LoggingUtil.logging_out is None:
                LoggingUtil.logging_out = LoggingUtil.out_file_log(system)
            caps = lambda: Base.android_desired_caps if "ANDROID" == system else Base.ios_desired_caps
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', caps())
            self.driver.implicitly_wait(10)

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
            LoggingUtil.logging_out.info('%s 页面中未找到 %s 元素' % (self, loc[1]))
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
            LoggingUtil.logging_out.info('%s 页面中未找到 %s 元素' % (self, loc[1]))

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
            LoggingUtil.logging_out.info('%s 页面中未找到 %s 元素' % (self, loc[1]))

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
            LoggingUtil.logging_out.info('%s 页面未能找到 %s 按钮' % (self, loc[1]))

    def ios_ele(self,**loc):
        '''
         获取页面元素
        :param loc: 封装了获取页面元素方法key  和value
        :return: ele元素，可直接操作
        '''
        try:
            if loc.get('predicate'):
                return self.driver.find_element_by_ios_predicate(loc.get('predicate'))
            elif loc.get('accessibility_id'):
                return self.driver.find_element_by_accessibility_id(loc.get('accessibility_id'))
            elif loc.get('class_name'):
                return self.driver.find_element_by_class_name(loc.get('class_name'))
            elif loc.get('xpath'):
                return self.driver.find_element_by_xpath(loc.get('xpath'))
        except:
            LoggingUtil.logging_out.info('%s 页面中未找到 %s 元素' % (self, loc))

    def ios_eles(self,**loc):
        '''
        获取页面元素列表
        :param loc: 封装了获取页面元素方法key  和value
        :return: ele元素列表
        '''
        try:
            if loc.get('elements_by_ios_predicate'):
                return self.driver.find_elements_by_ios_predicate(loc.get('elements_by_ios_predicate'))
            elif loc.get('elements_by_accessibility_id'):
                return self.driver.find_elements_by_accessibility_id(loc.get('elements_by_accessibility_id'))
            elif loc.get('elements_by_class_name'):
                return self.driver.find_elements_by_class_name(loc.get('elements_by_class_name'))
        except:
            LoggingUtil.logging_out.info('%s 页面中未找到 %s 元素' % (self, loc))
