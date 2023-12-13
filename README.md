# 移动端app、unity3d游戏自动化测试框架
## 主要三方依赖：airtest、pocoui
## 简介
这个项目是基于网易开源的airtest&poco框架上进行开发的，主要的目的是为自动化测试提供合适的构建方案，
**不依赖于Airtest IDE工具**，加上airtest免费版本不支持多设备批量执行脚本，并提供多设备运行功能，
实际框架结构根据你的项目情况而定，有任何问题请提[issue](https://github.com/leafyin/mobile-u3d-test/issues)
## 如何使用？
`clone`或者`fork`当前仓库地址到你本地然后直接在工程基础上构建你的业务测试代码即可
 - 在Base.py中添加了gen_py的函数，调用时会将ResourceConfig.xlsx解析成python类对象，作为辅助函数，可选
 - ResourceConfig.xlsx文件作为存放测试用例中控件的name而存在，以键值对的方式存放，这里只作为一个例子
## Android KeyEvent
see [KeyEvent](https://developer.android.com/reference/android/view/KeyEvent)