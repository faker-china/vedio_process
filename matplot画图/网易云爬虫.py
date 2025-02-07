"""
    思路：
    1，根据歌手链接地址获取页面源码
    2，解析页面源码获取所有歌曲列表
    3，遍历，下载每首歌曲
    python爬虫前置基础视频教程：http://python222.com/post/7
    备注：网易云音乐开放接口：http://music.163.com/song/media/outer/url?id=歌曲ID  （VIP音乐下载不了）
    测试：https://music.163.com/#/artist?id=7763
    仅供学习测试
"""

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

# 获取用户输入的歌手链接页面
singer_url = input("请输入您要下载的歌手页面链接：")
# 格式化下载链接
url = singer_url.replace("/#", '')
response = requests.get(url=url, headers=headers)
# print(response.text)

# 实例化bs4
soup = BeautifulSoup(response.text, 'lxml')

# 获取歌曲列表
song_list = soup.select("ul.f-hide li a")
print(song_list)


def download_song(song_name, song_id):
    """
    下载歌曲
    :param song_name: 歌曲名称
    :param song_id: 歌曲ID
    :return:
    """
    music_open_api = "http://music.163.com/song/media/outer/url?id=" + song_id
    music = requests.get(url=music_open_api, headers=headers)
    # 下载歌曲
    try:
        with open(f"./music/{song_name}.mp3", 'wb') as file:
            file.write(music.content)
            print(f"《{song_name}》下载成功")
    except:
        print(song_name, "下载异常")


for song in song_list:
    # 获取歌曲名称
    song_name = song.text
    # print(song_name)
    # 获取歌曲ID
    song_id = song['href'].split("=")[1]
    # 下载歌曲
    download_song(song_name, song_id)