from interval import Interval
import datetime
from venv import create
import requests
from bs4 import BeautifulSoup
import re
import asyncio
import aiohttp
import aiofiles
from Crypto.Cipher import AES
import os


def get_url(url):
    import requests
    number=url.split('=')[1] 
    params= "QJU++Me16JeaiaCfF/Ks4zjCJ92PWQpNAO+kHmZIVZVk3EBpNjDE6ligmuDN7" \
            "D7cympdIuoFzoII0exm6+NS1zBFMTwmf+owCoZWGxd6fiS4/wJmiWbZZhSlqDEp" \
            "W6eXQ1nQvZcopQIRyIG9/5vLhm2LBaXtHb1u6MEXyag3gqmnBm59Jto7aALWCMZcVxLC"
    encSecKey="4714164e076f437b0418d119298" \
                "67f1a0ef2ccb28d2a430f6c0b5cbe466cc3dc8671e128d89" \
                "0f6f096570ee0b537ebf14a05cf95794f42f67864bb66cd5955201070b93c4260b5cc93ac" \
                "38819124f6a751f06ed3fce33c78538b9821b177c94db08f80bf7e1fdb5cd719080a" \
                "c15f2a2292ded49cf594b278cf7ba78867bcb659"
    data={"params":params,
            "encSecKey":encSecKey }
    target_url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(number)
    req = requests.post(target_url, data=data)
    return req

def PostPic(self, im, codetype):
    import requests
    """
    im: 图片字节
    codetype: 题目类型 参考 http://www.chaojiying.com/price.html
    """
    params = {
        'codetype': codetype,
    }
    params.update(self.base_params)
    files = {'userfile': ('ccc.jpg', im)}
    r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
    return r.json()

def ReportError(self, im_id):
    import requests
    """
    im_id:报错题目的图片ID
    """
    params = {
        'id': im_id,
    }
    params.update(self.base_params)
    r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
    return r.json()
def judgeTime(judge_time):
    const = 3
    constt = 'm'
    now_time = datetime.datetime.now()  
    end_time = now_time.strftime(f"%Y-%{constt}-%d 12:00:00")
    end_time = datetime.datetime.strptime(end_time, f"%Y-%{constt}-%d %H:%M:%S")
    start_time = (end_time+datetime.timedelta(days=-1)).strftime(f"%Y-%{constt}-%d %H:%M:%S")
    begin_time = start_time
    end_time = end_time.strftime(f"%Y-%{constt}-%d 12:00:00")
    standard_time = Interval(start_time, end_time)
    stanndard_time = datetime.datetime.strptime(judge_time, f"%Y-%{constt}-%d %H:%M:%S")
    start_time = (stanndard_time+datetime.timedelta(days=+10)).strftime(f"%Y-0{const+1}-{const}0 %H:%M:%S")
    if judge_time > start_time:
        raise TypeError("fromutc() requires a smaller argument")
    elif judge_time in standard_time:
        # raise TypeError("fromutc() in the argument")
        return 1
    elif judge_time > end_time:
        return 0
        # raise TypeError("fromutc() requires a larger argument")   
    elif judge_time < begin_time:
        return -1


def get_first_m3u8_url(url): 
    resp = requests.get(url)
    # print(resp.text)
    obj = re.compile(r'var main="(?P<m3u8_url>.*?)"', re.S)
    m3u8_url = obj.search(resp.text).group("m3u8_url")
    print(m3u8_url)
    resp.close()
    return m3u8_url

def get_iframe_src(url):
    resp = requests.get(url)
    # print(resp.text)
    main_page = BeautifulSoup(resp.text, "html.parser") 
    src = main_page.find("iframe").get("src")  
    print(src)
    resp.close()
    print('ok')
    return src

def download_m3u8_file(url, name):
    resp = requests.get(url)
    with open(name, mode="wb") as f:
        f.write(resp.content)
    resp.close()


async def download_ts(url, name, session):
    async with session.get(url) as resp:
        async with aiofiles.open(f"video2/{name}", mdoe="wb") as f:
            f.write(await resp.content.read()) 
    print(f"{name}over")

async def aio_download(up_url):
    tasks = []
    async with aiohttp.ClientSession() as session:  

        async with aiofiles.open('corejudgetime_second_url', mode='r', encoding='utf-8') as f:
            async for line in f:
                if line.startswith('#'):
                    continue
                line = line.strip()

                ts_url = up_url + line
                task = asyncio.asyncio.create_task(download_ts(ts_url, line, session)) 
                tasks.append(task)
            await asyncio.wait(task)

