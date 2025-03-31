import os
import subprocess
import re

# 设置代理（适用于 Clash 代理）
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# 关键词搜索（例如 "搞笑视频"）
SEARCH_QUERY = "搞笑视频"

# 获取链接后保存的文本文件
OUTPUT_FILE = r"D:\素菜库\youtube\link\youtube_funny_links.txt"


def get_video_links(query, max_results=10):
    """使用 yt-dlp 搜索 YouTube 并提取视频链接"""
    try:
        command = [
            "yt-dlp",
            f"ytsearch{max_results}:{query}",  # 搜索指定数量的视频
            "--get-id",  # 获取视频ID
            "--get-title",  # 获取视频标题
            "--get-url"  # 获取视频URL
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")  # 设置UTF-8编码

        if result.returncode == 0:
            # 解析输出结果并提取视频链接
            video_data = result.stdout.strip().splitlines()
            video_links = []

            # 每三行一组，包含ID、标题、URL
            for i in range(0, len(video_data), 3):
                video_links.append(video_data[i + 2])  # 获取视频URL

            # 保存到文件
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(video_links))

            print(f"✅ 成功获取 {len(video_links)} 个搞笑视频链接！")
            return video_links
        else:
            print("⚠️ 获取视频链接失败，请检查网络或代理设置！")
            print(f"详细错误信息：{result.stderr}")
            return []

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return []


if __name__ == "__main__":
    links = get_video_links(SEARCH_QUERY, max_results=10)
    print("🎯 获取并排序后的链接：")
    for link in links:
        print(link)
