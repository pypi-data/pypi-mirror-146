# coding utf-8
import requests
from lxml import html

etree = html.etree
from Fishconsole import logs
from Fishconsole import window
from Fishconsole import fcv


# 判断设备是否接入网络
def isConnected():
    import requests
    try:
        html = requests.get("http://www.baidu.com", timeout=2)
    except:
        return False
    return True


def 帮助():
    if isConnected():
        print(logs.日志("Fishconsole 检查更新开始。。。"))
        v = fcv.version()
        url = "https://pypi.org/project/Fishconsole/"
        res = requests.get(url).text
        res_html = etree.HTML(res)
        res_v = res_html.xpath("/html/body/main/div[2]/div/div[1]/h1/text()")[0]
        res_v = str(res_v[21:27])
        if res_v != v:
            print(logs.日志("Fishconsole 检查更新结束"))
            window.弹窗(f"检测到最新版本号发生了变化，请在终端键入pip install --upgrade 🦈Fishconsole更新至最新版本",
                      f"警告,🦈Fishconsole {res_v}版本更新", "确定")
        print(logs.日志("Fishconsole 检查更新结束"))
    else:
        print(logs.日志("Fishconsole 检查更新结束"))
        window.弹窗("你的设备没有联网，请检查网络连接", "警告", "确定")

    res = window.列表选择对话框("关于控制台输出模块的帮助文档会显示在命令行中，选中你想查看的内容，我们将会提供相应的窗口", f"Fishconsole {fcv.version()} 帮助文档",
                         ["Matplotlib中文辅助模块", "easygui中文辅助模块", "logs控制台输出辅助模块"])

    if res is not None:
        for a in res:
            if a == "logs控制台输出辅助模块":
                print(
                    "你是不是不知道怎么用的？那就让我来告诉你吧!!\n"
                    "这个函数是一个输出工具的集合，是由鱼鱼有几斤整理的\n"
                    "我整理了这几个项目\n"
                    f"{logs.颜色('这是logs模块当中的', 色选='火粉')}\n"
                    "---------------------\n"
                    "1：‘分割线’，它的作用就是弄出一个分割线，将无关的输出和自己想看到的分割线分割开来，这样就可以在一定层度上降低对头发的消耗啦\n"
                    "2：‘日志’，它的作用就是在前面加一个时间戳，主要是好看和装逼用的，但是用的好的话还是很可以的\n"
                    "3：‘颜色’，更改输出的颜色，目前支持的有：\n"
                    f"{logs.颜色('粉色', 色选='粉色')}，{logs.颜色('红色', 色选='红色')}，{logs.颜色('黄色', 色选='黄色')}，{logs.颜色('蓝色', 色选='蓝色')}，{logs.颜色('火粉', 色选='火粉')}，{logs.颜色('紫色', 色选='紫色')}，{logs.颜色('淡黄', 色选='淡黄')}\n"
                    f' {logs.颜色("测试", 色选="淡蓝背")}{logs.颜色("测试", 色选="紫背")}{logs.颜色("测试", 色选="绿背")}{logs.颜色("测试", 色选="蓝背")}{logs.颜色("测试", 色选="黄背")}{logs.颜色("测试", 色选="红背")}\n'
                    " (注意哦,分割线和日志都是可以和颜色叠加使用的)\n"
                    "---------------------\n"
                    "‘分割线’的语法是:\n"
                    "logs.分割线(输出显示文字,s模式='项目名')\n"
                    "‘日志’的语法是:\n"
                    "logs.日志(输出显示文字)\n"
                    "‘颜色’的语法是:\n"
                    "logs.颜色(输出显示文字)\n"
                    "示例（可以这种方法套）"
                    "print(logs.颜色(logs.分割线('帮助文档',s模式='🦈Fishconsole'),色选='蓝色'))\n"
                    "---------------------\n"
                )
            if a == "easygui中文辅助模块":
                window.弹窗(""
                          "这个东西其实是就是 easygui 的中文《辅助》模块[笑],对于英语不好的人来说这个做法确实是有一点卖相的，但是想深入\n研究，还得去看专门的教程，当然我可能也会持续完善这个的\n"
                          "---------------------\n"
                          "‘弹窗’，这是最基本的弹窗，就是弹出一个窗口，你点击按钮以后获得返回值\n"
                          "‘选择对话框’，就是弹出一个对话框，它可以有很多个选项，而且可以插入图片（这就很棒了），当然点击以后也会有返回值\n"
                          "‘列表选择对话框’，当选项多到离谱的时候，就可以使用列表选择对话框，你可以复选，也可以单选，不能插入图片，但是可以有几乎无限的选项\n"
                          "‘输入框’，就是可以存储你输入数据的窗口，他返回的内容就是你输入的内容 ，没填返回的就是None，\n"
                          "‘密码框’，就是在输入框的基础上对最后一个框使用了隐藏处理，返回的内容也是完整的（废话）\n"
                          "‘文件选择，文件保存’，故名思意，你们懂哈（我是懒虫）\n"
                          "-----------------------\n"
                          "弹窗的示例'\n\n"
                          "弹窗(1,2,3)\n"
                          "选择对话框的示例\n\n"
                          "print(选择对话框(1,2,选项=['ab','cd','ef'],图片地址='h.PNG'))\n"
                          "列表对话框的示例\n\n"
                          "print(列表选择对话框(1,2,选项=['ab','cd']))\n"
                          "输入框的示例\n\n"
                          "print(输入框('显示文字',['内容1','内容2'],'标题'))\n"
                          "密码框的示例\n\n"
                          "print(密码框('显示文字',['内容1','内容2'],'标题'))\n"
                          '文件选择的示例\n\n'
                          "print(文件选择())\n"
                          '文件保存的示例\n\n'
                          "print(文件保存())\n",

                          "easygui中文辅助模块", "ok")
