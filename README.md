# 移动端app、unity3d游戏自动化测试框架
## 主要三方依赖：airtest、pocoui
## 简介
1. 这个项目是基于网易开源的airtest&poco框架上进行开发的，主要的目的是为自动化测试提供合适的构建方案， 
所以也是支持跨 平台运行的**不依赖于Airtest IDE工具**，加上airtest免费版本不支持多设备批量执行脚本，并提供多设备运行功能，
实际框架结构根据你的项目情况而定，有任何问题请提[issue](https://github.com/leafyin/mobile-u3d-test/issues)
2. 该项目使用了雷电模拟器作为基础模拟器作为测试，模拟器运行目前仅支持windows，mac请用真机

## 如何使用？
`clone`或者`fork`当前仓库地址到你本地然后直接在工程基础上构建你的业务测试代码即可
1. 安装三方依赖库`pip install -r requirements.txt `
2. 在`Base.py`中添加了`gen_py`的函数，调用时会将`ResourceConfig.xlsx`解析成python类对象，作为辅助函数，可选
3. `ResourceConfig.xlsx`文件作为存放测试用例中控件的`name`而存在，以键值对的方式存放，这里只作为一个例子

## 测试示例解释
1. `example`目录下都是测试案例代码&以及项目代码结构
2. 框架结构
   * 基础抽象类`Base`，基类
   * 抽象实现类`AndroidBase`，抽象poco的测试基础方法，airtest可以作为图像识别再次单独抽象实现
   * 测试步骤`ExampleStep`，测试的每个步骤，比如单个点击操作等，一些单一并且重用性较高的代码
   * 测试用例`ExampleCase`，测试步骤拼凑起来就是测试用例，一个完整的测试路径
   * unittest单元测试`ExampleTest`，通过单元测试方法调用每个用例
3. 其他解释
   * `gen`目录是`gen_py`函数生成的python对象代码，方便开发测试用例时调用
   * unittest中用到了其他第三方测试报告
   * 每个tearDown方法中建议调用airtest`siple_report`函数，每次测试结束会生成当前测试用例的测试报告
   * 调用测试用例可以直接运行单元测试
   * `example.apk`测试apk，包名`com.charme.starnote`，测试账号：65432111，密码：yy1234

## todo
1. 测试例子程序开发， 测试报告集成，**doing...**
2. 开发基于本地web端GUI平台化操作

## Android KeyEvent
see [KeyEvent](https://developer.android.com/reference/android/view/KeyEvent)