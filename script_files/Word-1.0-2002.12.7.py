# UTF-8
# English Words Online Finder ver1.0
# Python verson 3.10
# need requests
# made by zhou-tian-xing on GitHub
import requests
import json
import time
lense = "百度翻译单词 ver1.0\nBy zhou-tian-xing on GitHub\nUsing requests, json, time\n\n"
arg = "特殊语法：\n\tlist[k1,k2,k3,···,kn]  -  查询多个单词\n设置：\n\tprint c  -  改变  是/否  进行相近拼写词输出""\n""\this r  -  查询历史""\n""\this clear  -  清除历史""\n""\thelp  -  语法，关于"
shu = "\n""请输入要翻译的单词(输入q或者Q或者空白退出)："
print(lense,arg,shu,sep='')
sim = True
while True:
    url="https://fanyi.baidu.com/sug"
    s=input(">>> ")
    if s.upper().strip() == "HELP":
        print(lense,arg,shu,sep='')
    if s.upper().strip() in ['Q','']:
        break
    if s.upper().strip() == 'PRINT C':
        sim = not sim
        print("相似项输出规则改变")
        continue
    if s.upper()[:4] == 'LIST':
        l = s[5:-1].split(',')
    else:
        l = s.split()
    if s.upper() == 'HIS R':
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
    if s.upper() == 'HIS CLEAR':
        imp = input("确定？(Y/N): ")
        if imp.upper() == 'Y':
            try:
                with open("fanyi_his.txt",mode='r', encoding='utf-8') as f:
                    k = f.readlines()
                with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
                    f.write('')
                print("清除了"+str(len(k))+"项历史记录。")
            except:
                with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
                    print("未发现历史记录TXT文档，已自动创建")
        continue
    for ss in l:
        print("输入"+ss+"：")
        dat={
                "kw":ss
                }
        resp=requests.post(url,data=dat)#发送post请求，发送的数据必须放在字典中，通过data参数进行传递
        #将服务器返回的内容直接处理成json => dict
        mean = ''
        if not ss.strip() == '':
            if resp.json()['data']:
                for x in resp.json()['data']:
                    if x['k'].upper() == ss.upper() or sim:
                        print('\t找到单词：“'+x['k']+'”  释义:',x['v'])
                        mean += '单词：“'+x['k']+'”  释义: '+x['v']
            else:
                print("\t未找到该词语。")
                mean = '未找到该词语。'
            try:
                with open("fanyi_his.txt",mode='r', encoding='utf-8') as f:
                    j = f.readlines()
            except:
                j = [""]
            with open("fanyi_his.txt",mode='w', encoding='utf-8') as f:
                t = time.localtime()
                j.append(str(t[0])+"年"+str(t[1])+"月"+str(t[2])+"日"+str(t[3])+"时"+str(t[4])+"分"+str(t[5])+"秒"+"    查询单词："+ss+"    结果：<<<"+mean+">>>")
                a = ''
                for n in range(len(j)):
                    if n == len(j)-1:
                        a += j[n]+'\n'
                    else:
                        a += j[n]
                f.write(a)
        else:
            print("请勿输入空白内容")

        resp.close()
