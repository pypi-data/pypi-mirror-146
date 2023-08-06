from Fishconsole import logs


# 模式,加密密码,内容
def 密码(模式, id_protect, password_a):
    import re
    import base64
    password = str(password_a)
    password_a = str(password_a)
    id_protect = str(id_protect)

    def encrypt(en_str):
        en_str = base64.b64encode(bytes(en_str, "utf-8"))
        return en_str.decode("utf-8")

    def decrypt(de_str):
        de_str = base64.b64decode(de_str.encode("utf-8"))
        return de_str.decode("utf-8")

    模式 = str(模式)
    if 模式 == "1":

        print(logs.系统日志("判断用户输入的值有没有致命问题,顺便拼接一下内容"))
        res_a = ""
        res_b = ""
        res_c = ""
        for a in password:
            res_a = res_a + a
            if a == "@":
                print(logs.颜色(logs.日志("你的密码中不允许有@符号，请重新输入"), 色选="红色"))
                exit()

        for b in id_protect:
            res_b = res_b + b
            if b == "@":
                print(logs.颜色(logs.日志("你的原文中不允许有@符号，请重新输入"), 色选="红色"))
                exit()


        else:
            print(logs.系统日志("确认成功"))
        print(logs.系统日志("转移变量的数据"))
        password = res_b
        id_protect = res_a
        print(logs.系统日志("拼接用户输入的内容"))
        res = password + "@" + id_protect
        print(logs.系统日志("对用户输入的内容进行加密"))
        jiami_last = ""
        count = 0
        counta = 0
        for a in res:
            counta = counta + 1
            if a == "1":
                jiami_last = jiami_last + "aaa"
                count = count + 1
            if a == "2":
                jiami_last = jiami_last + "aab"
                count = count + 1
            if a == "3":
                jiami_last = jiami_last + "aac"
                count = count + 1
            if a == "4":
                jiami_last = jiami_last + "aad"
                count = count + 1
            if a == "5":
                jiami_last = jiami_last + "aae"
                count = count + 1
            if a == "6":
                jiami_last = jiami_last + "aaf"
                count = count + 1
            if a == "7":
                jiami_last = jiami_last + "aba"
                count = count + 1
            if a == "8":
                jiami_last = jiami_last + "abb"
                count = count + 1
            if a == "9":
                jiami_last = jiami_last + "abc"
                count = count + 1
            if a == "0":
                jiami_last = jiami_last + "abd"
                count = count + 1
            if a == "a":
                jiami_last = jiami_last + "abe"
                count = count + 1
            if a == "b":
                jiami_last = jiami_last + "abf"
                count = count + 1
            if a == "c":
                jiami_last = jiami_last + "aca"
                count = count + 1
            if a == "d":
                jiami_last = jiami_last + "acb"
                count = count + 1
            if a == "e":
                jiami_last = jiami_last + "acc"
                count = count + 1
            if a == "f":
                jiami_last = jiami_last + "acd"
                count = count + 1
            if a == "g":
                jiami_last = jiami_last + "ace"
                count = count + 1
            if a == "h":
                jiami_last = jiami_last + "acf"
                count = count + 1
            if a == "i":
                jiami_last = jiami_last + "ada"
                count = count + 1
            if a == "j":
                jiami_last = jiami_last + "adb"
                count = count + 1
            if a == "k":
                jiami_last = jiami_last + "adc"
                count = count + 1
            if a == "l":
                jiami_last = jiami_last + "add"
                count = count + 1
            if a == "m":
                jiami_last = jiami_last + "ade"
                count = count + 1
            if a == "n":
                jiami_last = jiami_last + "adf"
                count = count + 1
            if a == "o":
                jiami_last = jiami_last + "aea"
                count = count + 1
            if a == "p":
                jiami_last = jiami_last + "aeb"
                count = count + 1
            if a == "q":
                jiami_last = jiami_last + "aec"
                count = count + 1
            if a == "r":
                jiami_last = jiami_last + "aed"
                count = count + 1
            if a == "s":
                jiami_last = jiami_last + "aee"
                count = count + 1
            if a == "t":
                jiami_last = jiami_last + "aef"
                count = count + 1
            if a == "u":
                jiami_last = jiami_last + "afa"
                count = count + 1
            if a == "v":
                jiami_last = jiami_last + "afb"
                count = count + 1
            if a == "w":
                jiami_last = jiami_last + "afc"
                count = count + 1
            if a == "x":
                jiami_last = jiami_last + "afd"
                count = count + 1
            if a == "y":
                jiami_last = jiami_last + "afe"
                count = count + 1
            if a == "z":
                jiami_last = jiami_last + "aff"
                count = count + 1
            if a == "A":
                jiami_last = jiami_last + "baa"
                count = count + 1
            if a == "B":
                jiami_last = jiami_last + "bab"
                count = count + 1
            if a == "C":
                jiami_last = jiami_last + "bac"
                count = count + 1
            if a == "D":
                jiami_last = jiami_last + "bad"
                count = count + 1
            if a == "E":
                jiami_last = jiami_last + "bae"
                count = count + 1
            if a == "F":
                jiami_last = jiami_last + "baf"
                count = count + 1
            if a == "G":
                jiami_last = jiami_last + "bba"
                count = count + 1
            if a == "H":
                jiami_last = jiami_last + "bbb"
                count = count + 1
            if a == "I":
                jiami_last = jiami_last + "bbc"
                count = count + 1
            if a == "J":
                jiami_last = jiami_last + "bbd"
                count = count + 1
            if a == "K":
                jiami_last = jiami_last + "bbe"
                count = count + 1
            if a == "L":
                jiami_last = jiami_last + "bbf"
                count = count + 1
            if a == "M":
                jiami_last = jiami_last + "bca"
                count = count + 1
            if a == "N":
                jiami_last = jiami_last + "bcb"
                count = count + 1
            if a == "O":
                jiami_last = jiami_last + "bcc"
                count = count + 1
            if a == "P":
                jiami_last = jiami_last + "bcd"
                count = count + 1
            if a == "Q":
                jiami_last = jiami_last + "bce"
                count = count + 1
            if a == "R":
                jiami_last = jiami_last + "bcf"
                count = count + 1
            if a == "S":
                jiami_last = jiami_last + "bda"
                count = count + 1
            if a == "T":
                jiami_last = jiami_last + "bdb"
                count = count + 1
            if a == "U":
                jiami_last = jiami_last + "bdc"
                count = count + 1
            if a == "V":
                jiami_last = jiami_last + "bdd"
                count = count + 1
            if a == "W":
                jiami_last = jiami_last + "bce"
                count = count + 1
            if a == "X":
                jiami_last = jiami_last + "dbf"
                count = count + 1
            if a == "Y":
                jiami_last = jiami_last + "bea"
                count = count + 1
            if a == "Z":
                jiami_last = jiami_last + "beb"
                count = count + 1
            if a == "@":
                jiami_last = jiami_last + "bec"
                count = count + 1
            if a == " ":
                jiami_last = jiami_last + "bed"
                count = count + 1
        if count == 1:
            print(logs.颜色(logs.日志("你没有输入任何内容"), 色选="红色"))
            print(logs.颜色(logs.日志("你输入了非法字符（除1-0，a-z，空格以外其他全是），请检查后重新开始，加密失败"), 色选="红色"))
            exit()

        if counta == count:
            print(logs.系统日志("通过检查"))
        else:
            print(logs.颜色(logs.日志("你输入了非法字符（除1-0，a-z,空格以外其他全是），请检查后重新开始，加密失败"), 色选="红色"))
            exit()

        print(logs.系统日志("查看加密后的内容"))

        jiami_last = encrypt(jiami_last)
        print(jiami_last)
        logs.系统日志(f"加密成功")
        return jiami_last
    else:
        # 解密

        print(logs.系统日志("验证密码"))
        password_res = [f"{id_protect}"] + [f"{password_a}"]
        if password_res is None:
            print(logs.颜色(logs.日志("用户取消了操作"), 色选="红色"))
            exit()
        p_res = ""
        t_res = ""
        for a in password_res[0]:
            p_res = p_res + a
        for a in password_res[1]:
            t_res = t_res + a
        jiemi_last = decrypt(t_res)
        print(f"jiemi_last is {jiemi_last}")

        print(logs.系统日志("查看解密加密的内容"))
        pattern = re.compile('.{3}')
        a = str(' '.join(pattern.findall(jiemi_last)))
        print(a)

        # 重新合并加密后的内容
        print(logs.系统日志("重新合并数据"))
        print(logs.系统日志("先将每个转化后的值进行拆分"))
        pattern_jiemi = (' '.join(pattern.findall(jiemi_last)))
        pattern_jiemi = pattern_jiemi.split(' ')
        print(pattern_jiemi)
        pattern_resa = ""
        for a in pattern_jiemi:
            if a == "aaa":
                pattern_resa = pattern_resa + "1"
            if a == "aab":
                pattern_resa = pattern_resa + "2"
            if a == "aac":
                pattern_resa = pattern_resa + "3"
            if a == "aad":
                pattern_resa = pattern_resa + "4"
            if a == "aae":
                pattern_resa = pattern_resa + "5"
            if a == "aaf":
                pattern_resa = pattern_resa + "6"
            if a == "aba":
                pattern_resa = pattern_resa + "7"
            if a == "abb":
                pattern_resa = pattern_resa + "8"
            if a == "abc":
                pattern_resa = pattern_resa + "9"
            if a == "abd":
                pattern_resa = pattern_resa + "0"
            if a == "abe":
                pattern_resa = pattern_resa + "a"
            if a == "abf":
                pattern_resa = pattern_resa + "b"
            if a == "aca":
                pattern_resa = pattern_resa + "c"
            if a == "acb":
                pattern_resa = pattern_resa + "d"
            if a == "acc":
                pattern_resa = pattern_resa + "e"
            if a == "acd":
                pattern_resa = pattern_resa + "f"
            if a == "ace":
                pattern_resa = pattern_resa + "g"
            if a == "acf":
                pattern_resa = pattern_resa + "h"
            if a == "ada":
                pattern_resa = pattern_resa + "i"
            if a == "adb":
                pattern_resa = pattern_resa + "j"
            if a == "adc":
                pattern_resa = pattern_resa + "k"
            if a == "add":
                pattern_resa = pattern_resa + "l"
            if a == "ade":
                pattern_resa = pattern_resa + "m"
            if a == "adf":
                pattern_resa = pattern_resa + "n"
            if a == "aea":
                pattern_resa = pattern_resa + "o"
            if a == "aeb":
                pattern_resa = pattern_resa + "p"
            if a == "aec":
                pattern_resa = pattern_resa + "q"
            if a == "aed":
                pattern_resa = pattern_resa + "r"
            if a == "aee":
                pattern_resa = pattern_resa + "s"
            if a == "aef":
                pattern_resa = pattern_resa + "t"
            if a == "afa":
                pattern_resa = pattern_resa + "u"
            if a == "afb":
                pattern_resa = pattern_resa + "v"
            if a == "afc":
                pattern_resa = pattern_resa + "w"
            if a == "afd":
                pattern_resa = pattern_resa + "x"
            if a == "afe":
                pattern_resa = pattern_resa + "y"
            if a == "aff":
                pattern_resa = pattern_resa + "z"
            if a == "baa":
                pattern_resa = pattern_resa + "A"
            if a == "bab":
                pattern_resa = pattern_resa + "B"
            if a == "bac":
                pattern_resa = pattern_resa + "C"
            if a == "bad":
                pattern_resa = pattern_resa + "D"
            if a == "bae":
                pattern_resa = pattern_resa + "E"
            if a == "baf":
                pattern_resa = pattern_resa + "F"
            if a == "bba":
                pattern_resa = pattern_resa + "G"
            if a == "bbb":
                pattern_resa = pattern_resa + "H"
            if a == "bbc":
                pattern_resa = pattern_resa + "I"
            if a == "ddb":
                pattern_resa = pattern_resa + "J"
            if a == "bbe":
                pattern_resa = pattern_resa + "K"
            if a == "bbf":
                pattern_resa = pattern_resa + "L"
            if a == "bca":
                pattern_resa = pattern_resa + "M"
            if a == "bcb":
                pattern_resa = pattern_resa + "N"
            if a == "bcc":
                pattern_resa = pattern_resa + "O"
            if a == "bcd":
                pattern_resa = pattern_resa + "P"
            if a == "bce":
                pattern_resa = pattern_resa + "Q"
            if a == "bcf":
                pattern_resa = pattern_resa + "R"
            if a == "bda":
                pattern_resa = pattern_resa + "S"
            if a == "bdb":
                pattern_resa = pattern_resa + "T"
            if a == "bdc":
                pattern_resa = pattern_resa + "U"
            if a == "bdd":
                pattern_resa = pattern_resa + "V"
            if a == "bce":
                pattern_resa = pattern_resa + "W"
            if a == "bdf":
                pattern_resa = pattern_resa + "X"
            if a == "bea":
                pattern_resa = pattern_resa + "Y"
            if a == "beb":
                pattern_resa = pattern_resa + "Z"
            if a == "bed":
                pattern_resa = pattern_resa + " "
            if a == "bec":
                pattern_resa = pattern_resa + "@"

        print(logs.系统日志("读取加密信息"))
        text = pattern_resa.split("@", 1)[0]
        password = pattern_resa.split("@", 1)[1]
        if password == p_res:
            print(logs.颜色(logs.系统日志("密码验证成功"), 色选="蓝色"))
            return (f"{text}")
        else:
            print(logs.颜色(logs.日志("您的密码是错误的，请核对后重新输入"), 色选="红色"))
            exit()


# 模式,加密密码,内容
# a = password(1, 3, "1234567890")
# b = password(2, 3, a)


def 网易云音乐(歌单链接列表):
    import requests
    from lxml import html
    etree = html.etree

    urllist = 歌单链接列表
    base_url = 'https://link.hhtjim.com/163/'
    count = 0
    for url in urllist:
        count = count + 1
        print(logs.颜色(logs.分割线(f"开始第{count}次爬取", "Spider"), 色选="红色"))
        result = requests.get(url).text
        dom = etree.HTML(result)
        # //a[@contains内容(@href指定查找的内容,'song?'含有的)]/@href里面的链接文字
        ids = dom.xpath('//a[contains(@href,"song?")]/@href')
        names = dom.xpath('//a[contains(@href,"song?")]/text()')
        print(ids)
        a = -1
        for name in names:
            a = a + 1
            if ('$' in name) == False:
                if name != "{if x.album}":
                    if name != "{/if}":
                        count_id = ids[a].strip("/song?id=")
                        if ('$' in count_id) == False:
                            song_url = (f"{base_url}{count_id}.mp3")
                            print(logs.系统日志(f'存储文件：{name}.mp3'))
                            music = requests.get(song_url).content
                            with open(f'{name}.mp3', "wb") as file:
                                file.write(music)
                                file.close()
def 排名(数据源,第几个):
    第几个=int(第几个)
    a = 数据源
    for i in range(len(a)):
        for j in range(0, len(a) - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a[第几个]
