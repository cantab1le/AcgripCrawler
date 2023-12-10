import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def run():
    print("请选择要进行的操作：")
    print("1. 指定总页数顺序爬取")
    print("2. 指定页码范围爬取")
    print("3. 合并数据")
    choice = input("请输入你的选择（1,2或3）：")
    if choice == '1':
        target_page = int(input("请输入："))
        for page in range(1, target_page + 1):
            crawl(page)
            rest()
    elif choice == '2':
        start_page = int(input("开始页码："))
        end_page = int(input("结束页码："))
        for page in range(start_page, end_page + 1):
            crawl(page)
            rest()
    elif choice == '3':
        integrate()
    else:
        print("无效输入，请重新输入")

def integrate():
    # 获取当前目录下的所有xlsx文件
    files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    # 按文件名升序排列
    files.sort()

    # 创建一个空的DataFrame用于存储所有数据
    all_data = pd.DataFrame()

    for file in files:
        df = pd.read_excel(file)
        # 跳过第一行
        df = df.iloc[1:]
        all_data = all_data._append(df, ignore_index=True)

        # 把整合后的数据写入新的Excel文件，命名为data.xlsx
    all_data.to_excel('data.xlsx', index=False)

def rest():
    pause_time = random.randint(2, 5)  # 随机生成1到5秒的暂停时间
    print("[暂停] " + str(pause_time) + "秒后爬取下一页")
    time.sleep(pause_time)

def crawl(page):
    print("---------- 正在检索第 "+ str(page) + " 页 ----------")
    url = "https://acgrip.waaa.moe/1/page/"
    res = requests.get(url + str(page))
    res.encoding = "utf8"
    file_name = str(page) + ".xlsx"
    ##print(res.text)
    soup = BeautifulSoup(res.text, 'lxml')

    group = getGroup(soup)
    bangumi = getBangumi(soup)
    size = getSize(soup)
    download = getDownload(soup)

    df = pd.DataFrame({'制作组': group, '标题': bangumi, '大小': size, '下载完成': download})
    # 将DataFrame保存为Excel文件
    print("-----------------------------------\n" +
          "正在保存第 " + str(page) + " 页 ...")
    df.to_excel(file_name, index=False)
    print(file_name + "保存成功")

def getGroup(soup):
    # 查找所有<td class="date hidden-xs hidden-sm">下的第一个<div>标签
    td_tags = soup.find_all('td', class_='date hidden-xs hidden-sm')
    div_tags = [tag.find('div') for tag in td_tags]  # 查找每个<td class="date hidden-xs hidden-sm">下的<div>标签
    # 提取<div>标签内的<a>标签文本内容，并保存为列表
    a_tags = [div_tag.find('a') for div_tag in div_tags if div_tag]  # 过滤掉没有<div>标签的情况，再查找<a>标签
    texts = [a_tag.text for a_tag in a_tags]  # 提取<a>标签的文本内容
    print(str(len(texts))+" 发布者已找到")
    return texts

def getBangumi(soup):
    span_tags = soup.find_all('span', class_='title')
    #print(span_tags)
    a_tags = [tag.find('a') for tag in span_tags]  # 查找每个<span class="title">下的a标签
    # 提取a标签的文本内容，并保存为列表
    texts = [a_tag.text for a_tag in a_tags if a_tag]  # 过滤掉没有a标签的情况
    print(str(len(texts))+" 标题已找到")
    return texts

def getSize(soup):
    td_tags = soup.find_all('td', class_='size')
    texts = [td_tag.text for td_tag in td_tags]  # 提取<td class="size">标签的文本内容
    print(str(len(texts))+" 文件大小已找到")
    return texts

def getDownload(soup):
    done_divs = soup.find_all('div', class_='done')
    data = []
    for div in done_divs:
        inner_divs = div.find_all('span')  # 找到最下级的span标签
        for inner_div in inner_divs:
            data.append(inner_div.text)  # 提取文本内容并添加到数据列表中
    print(str(len(data)) + " 下载完成次数已找到")
    return data

run()