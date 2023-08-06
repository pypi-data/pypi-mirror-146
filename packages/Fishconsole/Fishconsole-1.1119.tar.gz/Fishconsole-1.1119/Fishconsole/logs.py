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
    if 色选 == "None":
        return text


def 日志(text,色选="Nona"):
    if 色选!="Nona":
        import time
        return 颜色(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + str(f":{text}"),色选=色选)
    else:
        import time
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + str(f":{text}")

def 系统日志(text):
    import time
    return 颜色(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),色选="紫色") + str(f":{text}")



def 分割线(标题, text,色选="Nona"):
    if 色选!="Nona":
        import time
        return "\n\n\n\n\n\n"+颜色(f"- {标题} -",色选=色选)+f"  {text}:\n--------------------------\n"
    else:
        return f"\n\n\n\n\n\n- {标题} -  {text}:\n--------------------------\n"

#print(日志(123, 色选="红色"))
#print(分割线("123","456","红色"))

