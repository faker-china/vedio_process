# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : xff
# @FILE     : 爬b战.py
# @Time     : 2024/10/18 上午9:30
# @Software : PyCharm
import re
import requests
from lxml import etree
import json

if __name__ == '__main__':
    # UA伪装
    head = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
        # 防盗链子
        , "Referer":"https://www.bilibili.com/"
        ,
        "Cookie":"CURRENT_FNVAL=4048; buvid3=BE2D386A-BBCB-E06E-8C2B-F5223B4C8BC517591infoc; b_nut=1721567317; _uuid=67165DF10-7B77-BDE8-3C63-732C2FCAF4D520375infoc; enable_web_push=DISABLE; buvid4=0245F01B-6C4B-CD5A-2EC5-BC060EC0777D18433-024072113-zRTpkL0r94scQqxGfSYKhQ%3D%3D; home_feed_column=5; header_theme_version=CLOSE; rpdid=|(Y|RJRR)Y~0J'u~kulY~Rkk; DedeUserID=1611307689; DedeUserID__ckMd5=b0865dba0b3ced5b; buvid_fp_plain=undefined; is-2022-channel=1; b_lsid=D8542F24_191412D93C0; bsource=search_bing; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; browser_resolution=1659-943; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjM2MzQ1OTMsImlhdCI6MTcyMzM3NTMzMywicGx0IjotMX0.Ox8rnEpQH5i1H_wQfH2z5CzZC0y8PlqQCy1KVa8XEfQ; bili_ticket_expires=1723634533; SESSDATA=f567fef6%2C1738927393%2C5d207%2A82CjAh2pSUKwDLr1XiI6ncU5B6NXEfWKS7ES6mDC8yGxM6aT3-BTdvK0KAlYpMhCXtEXgSVkl2aTlQWUNacTZOZ0ZNXzJwZ21QT2ozMXFXcWtFc1FpNnBIWlNWbml2Y3BxNV80bUNMZTBVN1dyb3h0STU1ZklDM0MwckJvanRmTmNkeTBFcW5qYl9RIIEC; bili_jct=8d788bcb503d69ba2ded7dfbb53f6e58; sid=71po5kkf; fingerprint=0c7279b7c69b9542a76b8d9df9b7872a; buvid_fp=BE2D386A-BBCB-E06E-8C2B-F5223B4C8BC517591infoc; bp_t_offset_1611307689=964382000909647872"
    }

    # 1、指定url
    url = "https://www.bilibili.com/video/BV17w4m1e7PT/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=2a6e427465a2f829272f5863986dfa80"

    # 2、发送请求
    response = requests.get(url, headers = head)

    # 3、获取响应的数据
    res_text = response.text

    # 4、数据解析
    tree = etree.HTML(res_text)

    with open("bili2.html", "w", encoding="utf-8") as f:
        f.write(res_text)

    base_info = "".join(tree.xpath("/html/head/script[4]/text()"))[20:]
    info_dict = json.loads(base_info)

    video_url = info_dict["data"]["dash"]['video'][0]["baseUrl"]
    audio_url = info_dict["data"]["dash"]['audio'][0]["baseUrl"]

    video_content = requests.get(video_url, headers=head).content
    audio_content = requests.get(audio_url, headers=head).content

    with open("video2.wmv", "wb") as f:
        f.write(video_content)
    with open("audio2.mp4", "wb") as fp:
        fp.write(audio_content)


