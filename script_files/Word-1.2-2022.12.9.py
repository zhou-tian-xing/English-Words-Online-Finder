# coding: utf-8
# English Words Online Finder ver1.1
# Python verson 3.10
# need requests
# made by zhou-tian-xing on GitHub
import requests
import json
import time
lense = "百度翻译单词 ver1.0\nBy zhou-tian-xing on GitHub\nUsing requests, json, time\n\n"
arg = "特殊语法：\n\tlist[k1,k2,k3,···,kn]或者k1 k2 k3 ... kn  -  查询多个单词\n设置：\n\tprint c  -  改变  是/否  进行相近拼写词输出\n\this c  -  改变 是/否 记录历史\n\this r  -  查询历史\n\this clear  -  清除历史""\n""\thelp  -  语法，关于"
shu = "\n""请输入要翻译的单词(输入q或者Q或者空白退出)："
print(lense,arg,shu,sep='')
sim = True
hisc = True
while True:
    url="https://fanyi.baidu.com/sug"  # 百度查词API
    s=input(">>> ")   # 获取输入内容

    # 如果输入的是 设置、帮助、历史操作、退出
    if s.upper().strip() == "HELP":  # 帮助
        print(lense,arg,shu,sep='')
        continue
    elif s.upper().strip("\n\t qQ") == '':  # 退出
        break
    elif s.upper().strip() == 'PRINT C':  # 相似输出规则
        sim = not sim
        print("是否输出相似项规则改变为："+str(sim))
        continue
    elif s.upper().strip() == "HIS C": # 是否记录历史
        hisc = not hisc
        print("是否记录历史规则改变为："+str(hisc))
        # 读历史，方便后面再存回去
        try:
            with open("fanyi_his.txt",mode='r', encoding='utf-8') as f:
                j = f.read()
        except:
            j = ""
        # 存历史
        with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
            t = time.localtime()
            if hisc:
                mm = "开启"
            else:
                mm = "关闭"
            j += str(t[0])+"年"+str(t[1])+"月"+str(t[2])+"日"+str(t[3])+"时"+str(t[4])+"分"+str(t[5])+"秒"+"    "+mm+"历史记录"
            f.write(j)
        continue
    elif s.upper() == 'HIS R':  # 读历史
        try:
            with open("fanyi_his.txt",mode='r', encoding='utf-8') as f:
                jw = f.readlines()
                for m in jw:
                    print(m,end='')
                print()
        except:
            with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
                print("未发现历史记录TXT文档，已自动创建")
        continue
    elif s.upper() == 'HIS CLEAR':  # 清除历史
        imp = input("确定？(Y/N): ")
        if imp.upper() == 'Y':
            try:
                with open("fanyi_his.txt",mode='r', encoding='utf-8') as f:
                    k = f.readlines()
                with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
                    f.write('')
            except:
                with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
                    print("未发现历史记录TXT文档，已自动创建")
                k=[]
            print("清除了"+str(len(k))+"项历史记录。")
        continue

    # 如果输入是单词，分1.list 2.一个单词/空格隔开的单词 两种情况处理
    if s.upper()[:4] == 'LIST':
        l = [wss.strip(" ~`!@#$%^&*()_-+={[}]|\\:;\"'?/>.<,·！￥…（）——【】、：；“’”‘《》，。？") for wss in s[5:-1].split(',')]
    else:
        l = [wss.strip(" ~`!@#$%^&*()_-+={[}]|\\:;\"'?/>.<,·！￥…（）——【】、：；“’”‘《》，。？") for wss in s.split()]
    
    for ss in l:
        print("输入"+ss+"：")
        dat={"kw":ss}  # 发送给API的信息
        resp=requests.post(url,data=dat)  # 发送post请求，发送的数据必须放在字典中，通过data参数进行传递
        # 将服务器返回的内容直接处理成json => dict
        mean = ''
        # 解析返回内容
        if not ss.strip() == '':
            if resp.json()['data']:
                for x in resp.json()['data']:
                    ps = 0
                    if x['k'].upper() == ss.upper() or sim:
                        ps += 1
                        print('\t找到单词：“'+x['k']+'”  释义:',x['v'])
                        mean += '单词：“'+x['k']+'”  释义: '+x['v']
                if ps == 0:
                    # 如果查到东西了但没有一个是完全匹配的(ps=0)
                    print("未找到完全匹配的单词")
            else:
                # 没查到任何东西
                print("\t未找到该词语。")
                mean = '未找到该词语。'

            # 存历史
            if hisc:
                # 读历史，方便后面再存回去
                try:
                    with open("fanyi_his.txt",mode='r', encoding='utf-8') as f:
                        j = f.read()
                except:
                    j = ""
                # 加入新的历史记录
                with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
                    t = time.localtime()
                    j += str(t[0])+"年"+str(t[1])+"月"+str(t[2])+"日"+str(t[3])+"时"+str(t[4])+"分"+str(t[5])+"秒"+"    查询单词："+ss+"    结果：<<<"+mean+">>>\n"
                    f.write(j)
        else:
            # 如果当前此项是空白的
            print("请勿输入空白内容")
