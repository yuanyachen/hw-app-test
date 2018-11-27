# hw-app-test
hw_appium_po
	common
		pub_util
			HanweiUtil . 工具类，封装基本方法，方法都是静态方法
			MysqlUtil . mysql工具类，封装操作mysql方法，方法都是类方法，继承HanweiUtil
			RedisUtil . redis工具类，封装操作redis方法，方法都是类方法，继承HanweiUtil	
		silde_swipe . 屏幕滑动方法		
	po
		base_page . 页面操作基本类，用于初始化appium，封装定位方法
		bash_page  页面业务操作类，用户页面具体操作实现，继承Base类
	test_case
		hw_test . 测试入口
	log . 记录日志
	result . 测试报告和截图
	data . 测试数据(没有用到)
