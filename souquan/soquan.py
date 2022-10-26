import csv
import time
from bs4 import BeautifulSoup #网页解析 获取数据
import re #正则表达式 进行文字匹配
import urllib.request,urllib.error #制定url 获取网页数据
import sqlite3 #进行数据库操作
from pandas._libs import json
import requests


def main(page,save_file):
    time.sleep(2)
    baseurl = "https://so.quandashi.com/search/search/search-list"
    # 爬取网页
    response = askurl(baseurl,page)
    # 解析数据
    dataList = getdata(response)
    # 保存数据
    savepath(dataList,save_file)
    print(f'成功爬取第{page+1}页')

#爬取网页
#得到一个指定的url的网页内容
def askurl(baseurl,page):
    #模拟浏览器头部信息 向服务器端发送信息
    head = {
        # 'authority':'so.quandashi.com',
        # 'method':'POST',
        # 'path':'/search/search/search-list',
        # 'scheme':'https',
        # 'accept':'application/json, text/javascript, */*; q=0.01',
        # 'accept-encoding':'gzip, deflate, br',
        # 'accept-language':'zh-CN,zh;q=0.9',
        # 'connection':'keep-alive',
        # 'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        # 'referer':'https://so.quandashi.com/index/search?key=%E9%98%BF%E9%87%8C&param=2',
        # 'host':'so.quandashi.com',
        # 'origin':'https://so.quandashi.com',
        # 'sec-ch-ua':'"Not A;Brand";v="99", "Chromium";v="101", "Google Chrome"; v="101"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
        'cookie':'user_1885253057=36c2a5f1165cc35d3861b6d5ab2266c0; NTKF_T2D_CLIENTID=guest778BBF86-E828-3795-D241-39F4DBFED3C1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218339f52f34ae-0fab5c449a2b2c-26021851-1327104-18339f52f35c0b%22%2C%22%24device_id%22%3A%2218339f52f34ae-0fab5c449a2b2c-26021851-1327104-18339f52f35c0b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; QDS_LOGIN_INFO_OFFICE=%7B%22operatorId%22%3A%22795761%22%2C%22operatorName%22%3Anull%2C%22userId%22%3A%22466152347a324d645a44316d784374774f6a696d58513d3d%22%2C%22userName%22%3Anull%2C%22userImg%22%3Anull%2C%22agentOrWriter%22%3A2%7D; QDS_AGENT_ORGAN_INFO=%7B%22agentIde%22%3A%22466152347a324d645a44316d784374774f6a696d58513d3d%22%2C%22account%22%3A%2218924230825%22%2C%22agentName%22%3Anull%2C%22agentOrganId%22%3Anull%2C%22agentOrganName%22%3Anull%2C%22agentOrganConName%22%3A%22%5Cu533f%5Cu540d%22%7D; INGRESSCOOKIE=1663140682.855.16227.222710; Hm_lvt_df2da21ec003ed3f44bbde6cbef22d1c=1663124693,1663140682; PHPSESSID=d26c11a088ef235552271dce9569753e; _csrf=93e0b059aeae397b003ca437e1f098fa827e2421edf4a291514876d244899b03a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%222_7tik4-Fs0xvvVrfrrzYHepReM8TXR4%22%3B%7D; nTalk_CACHE_DATA={uid:kf_9479_ISME9754_guest778BBF86-E828-37,tid:1663164098061241}; Hm_lpvt_df2da21ec003ed3f44bbde6cbef22d1c=1663164213; QDS_COOKIE=8EA66ED9-CB41-0C30-B572-D3BA64805F66; QDS_LOGIN_INFO=%7B%22userName%22%3A%22qds8313609%22%2C%22avtar%22%3A%22%22%7D',
        # 'X-Requested-With': 'XMLHttpRequest'
    }
    #构造请求参数
    params = {
        'key':'阿里',
        'param':2,
        'page':page,
        'pageSize':20
    }
    # 用户代理
    try:
        response = requests.get(baseurl,headers=head,params=params)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return response


#解析数据
def getdata(response):
    dataList = []
    # 逐一解析数据
    response.encoding='utf-8'
    data_json = json.loads(response.text)  # 通过 json 解析数据
    items_list = data_json['data']['items']
    for i in range(len(items_list)):
        items = {
            'regNo':items_list[i]['regNo'],
            'year':items_list[i]['year'],
            'detailId':items_list[i]['detailId'],
            'regDate':items_list[i]['regDate'],
            'appDate':items_list[i]['appDate'],
            'imageUrl': items_list[i]['imageUrl'],
            'statusName': items_list[i]['statusName'],
            'statusZh': items_list[i]['statusZh'],
            'addressEn': items_list[i]['addressEn'],
            'wenshuTag': items_list[i]['评审文书标识'],
            'privateEndDate': items_list[i]['privateEndDate'],
            'group': items_list[i]['group'],
            'privateStartDate': items_list[i]['privateStartDate'],
            'announcementIssue':items_list[i]['announcementIssue'],
            'address': items_list[i]['address'],
            'agency': items_list[i]['agency'],
            'applicantShare': items_list[i]['applicantShare'],
            'announcementDate':items_list[i]['announcementDate'],
            'applicantCn': items_list[i]['applicantCn'],
            'typeFlag': items_list[i]['typeFlag'],
            'enApplicant': items_list[i]['enApplicant'],
            'tmName': items_list[i]['tmName'],
            'regIssue': items_list[i]['regIssue'],
            'chizhu': items_list[i]['驰著地']
        }
        dataList.append(items)
    return dataList


def savepath(dataList,save_file):
    print(dataList)
    with open(save_file,'a',newline='',encoding='utf-8') as fp:
        # 设置表头，列名
        csv_header = ['regNo','year','tmName','detailId','regDate','appDate','imageUrl','statusName','statusZh',
                      'addressEn','评审文书标识','privateEndDate','group','privateStartDate',
                      'announcementIssue','applicantCn','typeFlag','enApplicant','regIssue','announcementDate','applicantShare','address','wenshuTag','agency','chizhu']
        csv_writer = csv.DictWriter(fp, csv_header)
        # 如果文件不存在，则写入表头；如果文件已经存在，则直接追加数据不再次写入表头
        if fp.tell() == 0:
            csv_writer.writeheader()
        csv_writer.writerows(dataList)  # 写入数据
if __name__ == '__main__':
    save_file = 'souquan.csv'  # 保存路径
    total_counts = 9184  # 爬取全部9184
    for p in range(total_counts//20 + 1):
        main(p, save_file)