
import urllib.request
import re
import os

# python教程的首页地址
python_class_HOST = 'http://www.liaoxuefeng.com'
python_class_home = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
dirName = 'python/'

# 获取未decode的html文件
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'}
    r = urllib.request.urlopen(url).read()
    return r

# 分析html页面并获取URL字典
def get_analyzed_urlComponetList(html):
    rRule = '(<a href="/wiki/.*?/.*?">.*?</a>)'
    rcompile = re.compile(rRule)
    rRulst = re.findall(rcompile, html)
    # print(rRulst)

    rKey = '(>.*?</a>)'
    rKeyCompile = re.compile(rKey)

    rURLCompo = 'href=".*?"'
    rURLCompoCompile = re.compile(rURLCompo)

    list = {}
    for item in rRulst:
        # print(item)
        keyBuffer = re.findall(rKeyCompile, item)[0]
        key = keyBuffer[1:-4]
        # print(key)

        keyURLBuffer = re.findall(rURLCompoCompile, item)[0]
        keyURL = keyURLBuffer[6:-1]
        # print(keyURL)

        list[key] = keyURL

    # print(list)
    # print(len(rRulst))
    return list

# 获取并下载保存css文件
def get_save_css_file(html,filePath):
    rule = '/static/themes/default/css/.*?\.css'
    css_list = re.findall(re.compile(rule),html)
    for url in css_list:
        # print(url)
        css_file = get_html(python_class_HOST+url)
        # print(css_file[0:100])
        # print(url[27:-4])
        with open(filePath+url[27:-4]+'.css','wb') as f:
            f.write(css_file)

# 改变css文件路径
def change_css_file_path(html,absolutelyPath):
    html = html.replace('/static/themes/default/css',absolutelyPath)
    return html
#

# 如果文件夹不存在就创建一个
def create_dir_if_not_exists(dir):
    # os.listdir()
    if os.path.exists(dirName) == False:
        os.mkdir(dirName)

create_dir_if_not_exists(dirName)
h = get_html(python_class_home).decode('utf-8')
get_save_css_file(h,dirName)
list = get_analyzed_urlComponetList(h)


for k, u in list.items():
    html = get_html(python_class_HOST + u)
    html = html.decode('utf-8')
    html = change_css_file_path(html,os.path.abspath(dirName))
    html = html.encode('utf-8')

    k = k.replace('/','-')
    print(k)
    path = dirName + k + '.html'
    print(path)

    with open(path,'wb') as f:
        if os.path.exists(path) == False:
            os.makedirs(path)
        f.write(html)

# print(os.path.abspath('python'))





