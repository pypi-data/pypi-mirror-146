import matplotlib.pyplot as plt
from Fishconsole import logs


def 单线折线图(x轴范围, x轴数据源, y轴范围, y轴数据源, 网格线=False, x轴名="x", y轴名="y", 线的样式="-", 线的颜色="b", 线的宽度=2, 画布长=6, 画布宽=6, 标题=None,
          绘图标记=None, 网格线样式='-', 网格线方向="both", 网格线RGB="#000", 网格线宽度=0.5):
    # 修复可能出现的负数
    plt.rcParams['axes.unicode_minus'] = False
    # 画布长宽
    plt.figure(figsize=(画布长, 画布宽))
    # 配置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 配置标题
    plt.title(标题)  # 括号当中输入标题的名称
    # x轴坐标轴范围
    plt.xlim(x轴范围)
    # y轴坐标轴范围
    plt.ylim(y轴范围)
    # x轴标签
    plt.xlabel(x轴名)
    # y轴标签
    plt.ylabel(y轴名)
    # 配置x轴和y轴的内容
    if 网格线:
        plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式)
    x = x轴数据源
    y = y轴数据源
    plt.plot(x, y, linestyle=f'{线的样式}', color=f'{线的颜色}', marker=f'{绘图标记}', linewidth=f'{线的宽度}')
    plt.show()


def 双线折线图(x轴范围, x轴数据源, y轴范围, y轴数据源, xa轴范围, xa轴数据源, ya轴范围, ya轴数据源, 网格线=False, ya轴名="ya", xa轴名="xa", y轴名="y", x轴名="x",
          线的样式="-", 线的宽度=2, 画布长=6, 画布宽=6, 标题=None, 绘图标记=None, 网格线方向="both", 网格线样式='-', 网格线RGB="#000", 网格线宽度=0.5):
    # 修复可能出现的负数
    plt.rcParams['axes.unicode_minus'] = False
    # 画布长宽
    plt.figure(figsize=(画布长, 画布宽))
    # 配置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 配置标题
    plt.title(标题)  # 括号当中输入标题的名称
    # x轴坐标轴范围
    plt.xlim(x轴范围)
    # y轴坐标轴范围
    plt.ylim(y轴范围)
    # xa轴标签
    plt.xlabel(x轴名)
    # y轴标签
    plt.ylabel(y轴名)
    # x轴坐标轴范围
    plt.xlim(xa轴范围)
    # y轴坐标轴范围
    plt.ylim(ya轴范围)
    # 标题的名称
    plt.title(标题)
    # x轴标签
    plt.xlabel(xa轴名)
    # y轴标签
    plt.ylabel(ya轴名)
    # 配置x轴和y轴的内容
    x = x轴数据源
    y = y轴数据源
    xa = xa轴数据源
    ya = ya轴数据源
    if 网格线:
        plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式)
    plt.plot(x, y, xa, ya, linestyle=f'{线的样式}', marker=f'{绘图标记}', linewidth=f'{线的宽度}')
    plt.show()


# x轴数据源,y轴数据源,xa轴数据源,ya轴数据源,xb轴数据源,yb轴数据源,xc轴数据源,yc轴数据源,

def 子图(模式, 总标题=None, 子图a标题=None, 子图b标题=None, 子图c标题=None, 子图d标题=None, x轴数据源=None, y轴数据源=None, xa轴数据源=None,
       ya轴数据源=None, xb轴数据源=None, yb轴数据源=None, xc轴数据源=None, yc轴数据源=None, 绘图标记=None,
       网格线方向="both", 网格线样式='-', 网格线RGB="#000", 网格线宽度=0.5, 网格线=False, x轴名="x", y轴名="y", xa轴名="xa", ya轴名="ya",
       xb轴名="xb", yb轴名="yb", xc轴名="xc", yc轴名="yc"):
    模式 = str(模式)
    if 模式 == "2":
        # 子图1
        xpoints = x轴数据源
        ypoints = y轴数据源
        plt.subplot(2, 2, 1)
        plt.plot(xpoints, ypoints)
        plt.title(f"{子图a标题}")
        # x轴标签
        plt.xlabel(x轴名)
        # y轴标签
        plt.ylabel(y轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        # 子图2
        x = xa轴数据源
        y = ya轴数据源
        plt.subplot(2, 2, 2)
        plt.plot(x, y)
        plt.title(f"{子图b标题}")
        # x轴标签
        plt.xlabel(xa轴名)
        # y轴标签
        plt.ylabel(ya轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        plt.suptitle(f"{总标题}")
        plt.show()

    if 模式 == "3":
        # 子图1
        xpoints = x轴数据源
        ypoints = y轴数据源
        plt.subplot(2, 2, 1)
        plt.plot(xpoints, ypoints)
        plt.title(f"{子图a标题}")
        # x轴标签
        plt.xlabel(x轴名)
        # y轴标签
        plt.ylabel(y轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        # 子图2
        x = xa轴数据源
        y = ya轴数据源
        plt.subplot(2, 2, 2)
        plt.plot(x, y)
        plt.title(f"{子图b标题}")
        # x轴标签
        plt.xlabel(xa轴名)
        # y轴标签
        plt.ylabel(ya轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        # 子图3
        x = xb轴数据源
        y = yb轴数据源
        plt.subplot(2, 2, 3)
        plt.plot(x, y)
        plt.title(f"{子图c标题}")
        # x轴标签
        plt.xlabel(xb轴名)
        # y轴标签
        plt.ylabel(yb轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        plt.suptitle(f"{总标题}")
        plt.show()

    if 模式 == "4":
        # 子图1
        xpoints = x轴数据源
        ypoints = y轴数据源
        plt.subplot(2, 2, 1)
        plt.plot(xpoints, ypoints)
        plt.title(f"{子图a标题}")
        # x轴标签
        plt.xlabel(x轴名)
        # y轴标签
        plt.ylabel(y轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        # 子图2
        x = xa轴数据源
        y = ya轴数据源
        plt.subplot(2, 2, 2)
        plt.plot(x, y)
        plt.title(f"{子图b标题}")
        # x轴标签
        plt.xlabel(xa轴名)
        # y轴标签
        plt.ylabel(ya轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        # 子图3
        x = xb轴数据源
        y = yb轴数据源
        plt.subplot(2, 2, 3)
        plt.plot(x, y)
        plt.title(f"{子图c标题}")
        # x轴标签
        plt.xlabel(xb轴名)
        # y轴标签
        plt.ylabel(yb轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        # 子图4
        x = xc轴数据源
        y = yc轴数据源
        plt.subplot(2, 2, 4)
        plt.plot(x, y)
        plt.title(f"{子图d标题}")
        # x轴标签
        plt.xlabel(xc轴名)
        # y轴标签
        plt.ylabel(yc轴名)
        # 修复可能出现的负数
        plt.rcParams['axes.unicode_minus'] = False
        # 配置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        if 网格线:
            plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式, marker=f'{绘图标记}')

        plt.suptitle(f"{总标题}")
        plt.show()


def 柱形图(x轴名数组, y轴数据组, 背景数组=None, 模式="竖", 宽度=0.5, 高度=0.1, 标题=None, 网格线=False, 网格线方向="both", 网格线样式='-', 网格线RGB="#000",
        网格线宽度=0.5):
    if 模式 == "竖":
        plt.bar(x轴名数组, y轴数据组, color=背景数组, width=宽度)
    else:
        plt.barh(x轴名数组, y轴数据组, color=背景数组, height=高度)
    plt.title(f"{标题}")
    # 修复可能出现的负数
    plt.rcParams['axes.unicode_minus'] = False
    # 配置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    if 网格线:
        plt.grid(axis=f"{网格线方向}", color=网格线RGB, linewidth=网格线宽度, linestyle=网格线样式)
    plt.show()


def 饼图(数据组, 数据组标签=None, 数据组颜色=None, 总标题=None, 百分比=False):
    plt.pie(数据组, labels=数据组标签, colors=数据组颜色)
    plt.title(总标题)  # 设置标题
    if 百分比:
        plt.pie(数据组, labels=数据组标签, colors=数据组颜色,autopct = '%.2f%%')

    plt.show()
