import requests
from bs4 import BeautifulSoup
import re
import random
from hashlib import md5
import os
import argparse
import time


def getUrl(url):
    response = requests.get(url)
    pdfUrl = []
    count = 0
    bs = BeautifulSoup(response.text,"html.parser")
    pdfs = bs.find_all(href=re.compile('/content/.*html'))
    names = []
    for tag in pdfs:
        if count < 20: 
            pdfUrl.append("https://openaccess.thecvf.com"+tag.get("href"))
            count = count+1
            names.append(re.split('[./]', tag.get("href"))[-2][:-16].replace("_"," "))
        else: break
    return names,pdfUrl


def getAbstract(paperUrls):
    abstract = []
    for url in paperUrls:
        response = requests.get(url)
        bs = BeautifulSoup(response.text,"html.parser")
        abstract.append(bs.find(id="abstract").text.strip())
    return abstract

def translate_api(input_text, appid, appkey):
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()
    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'en'
    to_lang = 'zh'
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    
    query = input_text
    # Generate salt and sign
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    try:
        res_text = result['trans_result'][0]['dst']
    except:
        print(result)
        sys.exit()
    return res_text

def write2txt(path,title,contents):
    with open(path,"w+") as f:
        for ti,con in zip(title,contents):
            f.write(ti+"\n")
            f.write(con+"\n")
            f.write("\n")

def fromtxt(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    lines = [l.strip('\n') for l in lines]
    return lines[::3], lines[1::3]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--en_path', type=str, default='./homework_5/abstract.txt', help='path to English abstract')
    parser.add_argument('--cn_path', type=str, default='./homework_5/my_abstract.txt', help='path to Chinese abstract')
    parser.add_argument('--appid', type=str, help='appid of Baidu translation')
    parser.add_argument('--appkey', type=str, default=2, help='appkey of Baidu translation')
    args = parser.parse_args()
    web = "https://openaccess.thecvf.com/ICCV2021?day=2021-10-12"
    if os.path.exists(args.en_path):
        name, abstracts = fromtxt(args.en_path)
    else:
        name,pdfurls = getUrl(web)
        abstracts = getAbstract(pdfurls)
        write2txt(args.en_path, name, abstracts)
    ch_abstracts = []
    for ab in abstracts:
        ch_abstracts.append(translate_api(ab, args.appid, args.appkey))
        write2txt(args.cn_path, name, ch_abstracts)
        time.sleep(10)
