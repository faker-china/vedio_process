import os
import subprocess
import re

# 设置代理（适用于 Clash 代理）
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# 关键词搜索（例如 "搞笑视频"）
SEARCH_QUERY = "搞笑视频"

# 获取链接后保存的文本文件
OUTPUT_FILE = r"D:\pythonProject\vedio_p\pac\vedio\link\youtube_funny_links.txt"


def get_video_links(query, max_results=10):
    """使用 yt-dlp 搜索 YouTube 并提取视频链接"""
    try:
        # 显式指定代理
        command = [
            "yt-dlp",
            "--proxy", "http://127.0.0.1:7890",
            f"ytsearch{max_results}:{query}",
            "--get-id"
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        # 打印详细的命令输出，便于调试
        print(result.stdout)

        if result.returncode == 0:
            video_ids = result.stdout.strip().split("\n")

            if not video_ids:
                print("⚠️ 未能找到任何视频链接！")
                return []

            video_links = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]

            # 获取文件所在目录
            output_dir = os.path.dirname(OUTPUT_FILE)
            # 检查目录是否存在，不存在则创建
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 保存到文件
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(video_links))

            print(f"✅ 成功获取 {len(video_links)} 个搞笑视频链接！")
            return video_links
        else:
            print("⚠️ 获取视频链接失败，请检查网络或代理设置！")
            print(f"错误信息: {result.stderr}")
            return []

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return []


if __name__ == "__main__":
    links = get_video_links(SEARCH_QUERY, max_results=50)
    print("🎯 获取的链接：")
    for link in links:
        print(link)