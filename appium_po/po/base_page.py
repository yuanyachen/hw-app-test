from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
import time, os, platform


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
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', Base.desired_caps)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

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

    def get_separator(self):
        '''根据系统获取目录分隔符'''
        if 'Windows' in platform.system():
            separator = '\\'
        else:
            separator = '/'
        return separator

    def get_lcaol_time_str(self):
        '''
        获取系统当前时间的str
        :return:
        '''
        return time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))

    def get_png_name(self, name):
        '''
        判断文件夹是否存在，不存在则创建，生成图片的名字
        :param name:
        :return:
        '''
        separator = self.get_separator()
        root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file_page = root_path + separator + 'result' + separator + day + separator + 'image' + separator + day
        ts = self.get_lcaol_time_str()
        type = '.png'
        if not os.path.exists(file_page):
            os.makedirs(file_page)
        file_name = file_page + separator + ts + '_' + name + type
        print(file_name)
        return file_name

    def save_screenshot(self, name):
        '''
        保存截图
        :param name: 图片名称
        :return: image
        '''
        return self.driver.save_screenshot(self.get_png_name(name))
