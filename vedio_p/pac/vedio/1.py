import yt_dlp
import re

video_url = 'https://www.youtube.com/shorts/vrLuiI9ni1U'

def sanitize_filename(filename):
    # 去除非法字符
    return re.sub(r'[\\/*?:"<>|]', '', filename)

ydl_opts = {
    'format': 'bestvideo+bestaudio[ext=m4a]/best',
    'outtmpl': f'D:/素菜库/输出/0307/{sanitize_filename("%(title)s")}.%(ext)s',
    'merge_output_format': 'mp4',
    # 若需要，可明确指定 FFmpeg 的路径
     'ffmpeg_location': 'D:\浏览器下载\ffmpeg-7.0.1-essentials_build\ffmpeg-7.0.1-essentials_build\bin\ffmpeg.exe'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])