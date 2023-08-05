# ecoding=utf-8



def 颜色(text, 色选):
    if 色选 == "粉色":
        return f"\033[0;35;40m{text}\033[0m"
    if 色选 == "红色":
        return f"\033[0;31;40m{text}\033[0m"
    if 色选 == "黄色":
        return f"\033[0;33;40m{text}\033[0m"
    if 色选 == "蓝色":
        return f"\033[0;34;40m{text}\033[0m"
    if 色选 == "火粉":
        return f"\033[0;35;40m{text}\033[0m"
    if 色选 == "紫色":
        return f"\033[0;36;40m{text}\033[0m"
    if 色选 == "淡黄":
        return f"\033[0;37;40m{text}\033[0m"
    if 色选 == "红背":
        return f'\033[41m{text}1\033[0m'
    if 色选 == "黄背":
        return f'\033[43m{text}\033[0m'
    if 色选 == "蓝背":
        return f'\033[44m{text}\033[0m'
    if 色选 == "绿背":
        return f'\033[42m{text}\033[0m'
    if 色选 == "紫背":
        return f'\033[45m{text}\033[0m'
    if 色选 == "淡蓝背":
        return f'\033[46m{text}6\033[0m'








def 日志(text, 色选=None):
    import time
    if 色选 is not None:
        text = (str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f":{text}"))
        textok=颜色(text, 色选)
        return textok
    else:
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f":{text}")


def 分割线(text, s模式, 颜色a=False):
    if 颜色a:
        text = f"\n\n\n\n\n\n- {text} -  {s模式} :\n-------------------------\n"
        textok = 颜色(text, s模式)
        return(textok)
    else:
        return f"\n\n\n\n\n\n- {text} -  {s模式}:\n--------------------------\n"









