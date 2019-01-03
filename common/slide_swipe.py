def get_size(driver):
    '''获取手机屏幕大小'''
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


def swipe_up(driver, t, min=0.25, max=0.95):
    '''屏幕向上滑动'''
    l = get_size(driver)
    x1 = int(l[0] * 0.5)  # x坐标
    y1 = int(l[1] * max)  # 起始y坐标
    y2 = int(l[1] * min)  # 终点y坐标
    driver.swipe(x1, y1, x1, y2, t)


def ios_swipe_up(driver, t, mix=0.25, mxa=0.95):
    '''ios屏幕向上滑动'''
    l = get_size(driver)
    fromX = int(l[0] * 0.5)
    fromY = int(l[1] * max)
    toY = int(l[1] * mix)
    driver.execute_script("mobile:dragFromToForDuration", {"duration": 0.5, "element": None, "fromX": fromX, "fromY": fromY, "toX": fromX, "toY": toY})

def swipe_down(driver, t, min=0.25, max=0.95):
    '''屏幕向下滑动'''
    l = get_size(driver)
    x1 = int(l[0] * 0.5)  # x坐标
    y1 = int(l[1] * min)  # 起始y坐标
    y2 = int(l[1] * max)  # 终点y坐标
    driver.swipe(x1, y1, x1, y2, t)


def swipe_left(driver, t, min=0.25, max=0.95, y_ratio=0.5):
    '''屏幕向左滑动'''
    l = get_size(driver)
    x1 = int(l[0] * max)  # 起始x坐标
    x2 = int(l[0] * min)  # 终点x坐标
    y1 = int(l[1] * y_ratio)  # y坐标
    driver.swipe(x1, y1, x2, y1, t)


def swipe_rigth(driver, t, min=0.25, max=0.95):
    '''屏幕向右滑动'''
    l = get_size(driver)
    x1 = int(l[0] * min)  # 起始x坐标
    x2 = int(l[0] * max)  # 终点x坐标
    y1 = int(l[1] * 0.5)  # y坐标
    driver.swipe(x1, y1, x2, y1, t)
