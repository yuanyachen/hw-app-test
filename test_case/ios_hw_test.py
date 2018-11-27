from appium import webdriver

desired_caps = {
    'platformName': 'iOS',
    'platformVersion': '11.4.1',
    'deviceName': 'iphone 6s',
    'udid': '90bd972239d3674315fcf4bb50a3923a07c24539',
    # 'realDeviceLogger': '/usr/local/lib/node_modules/deviceconsole/deviceconsole',
    'bundleId': 'com.hanweiyx.hanweishopping',
    'newCommandTimeout': 60,
    'automationName': 'appium',
    'noReset': True,
    "xcodeOrgId": "<Team ID>",
    "xcodeSigningId": "iPhone Developer"

}

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
driver.implicitly_wait(10)

ele = driver.find_element_by_ios_predicate("name = '一起拼'")
ele1 = driver.find_element_by_accessibility_id('我的')
ele.click()
ele1.click()
print(ele.text)
print(ele)
print(type(ele))
print(ele1)
print(type(ele))