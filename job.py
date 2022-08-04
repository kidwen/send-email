from datetime import datetime
import mail
import requests
from lxml import etree
import re

url = "http://www.shiyebian.net/{}/{}/"
url_only_p = "http://www.shiyebian.net/{}"
url_page = "http://www.shiyebian.net/e/action/ListInfo/?classid={}&page={}"
# url="http://www.shiyebian.net/e/action/ListInfo/?classid=228&page={}"
next_page_path = '/html/body//div[@class="fenye"]/a[2]/@href'
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.shiyebian.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
}


def get_class_id():
    pass


def get_requests_data(province_city_list):
    map_list = []
    for p in province_city_list:
        if p["city"] == "":
            requests_url = url_only_p.format(p["privince"])
        else:
            requests_url = url.format(p["privince"], p["city"])
        response = requests.get(requests_url, headers=DEFAULT_REQUEST_HEADERS)
        html = response.content.decode('gb2312')
        doc = etree.HTML(html)
        next_page_url = doc.xpath(next_page_path)[0]  # 0

        # href="http://www.shiyebian.net/e/action/ListInfo/?classid=32&page=1"
        class_id = re.findall("classid=(\d+)&", next_page_url)[0]
        for i in range(5):
            print("page:", i + 1)
            map_list += get_data(i, url_page, class_id, p)
    return map_list


def get_data(page, url_page, class_id, p):
    url_next_page = url_page.format(class_id, page)
    print(url_next_page)
    map_list_ = []
    response = requests.get(url_next_page.format(page), headers=DEFAULT_REQUEST_HEADERS)
    html = response.content.decode('gb2312')
    doc = etree.HTML(html)
    job_list = doc.xpath("/html/body/div//ul[@class='lie1']/li")
    for job_d in job_list:
        job_detail = job_d.xpath('./a//text()')[0]
        job_date = job_d.xpath('./em//text()')[0]
        job_url = job_d.xpath('./a/@href')[0]
        map_data = {
            "job_name": job_detail,
            "update_date": job_date,
            "job_url": job_url
        }
        if p["city"] == "":
            map_data["city"] = p["privince"]
        else:
            map_data["city"] = p["city"]
        if check(job_date):
            map_list_.append(map_data)
    return map_list_


def check(date_str):
    flag = True
    today = datetime.now().strftime("%m-%d")
    flag = date_str.split()[0] == today
    return flag


def main():
    with open("mail_map.txt", 'r', encoding='utf-8') as f:
        for line in f:
            privince_city_list = []
            data = line.replace("\n", "")
            values = data.split(" ")
            p_c = values[1].split("/")
            for pc in p_c:
                p__c = pc.split(",")
                if len(p__c) == 1:
                    privince_city_list.append({"privince": p__c[0], "city": ""})
                else:
                    privince_city_list.append({"privince": p__c[0], "city": p__c[1]})
            print(privince_city_list)
            mail_address = values[0]
            map_list = get_requests_data(privince_city_list)
            if len(map_list):
                mail.mail(mail_address, mail.get_html(map_list))
            else:
                print("no new job")


if __name__ == '__main__':
    main()
    # map_list = []
    # for i in range(10):
    #     map_list_1 = get_data(i)
    #     map_list += map_list_1
    #     if not len(map_list_1):
    #         break
    # print(map_list, len(map_list))
    # if len(map_list):
    #     mail.mail(mail.get_html(map_list))
    # else:
    #     "no new job"
