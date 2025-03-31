import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time
import random
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# 代理设置，添加了端口
USE_PROXY = True  # 设置是否使用代理
PROXY = {
    "http": "http://127.0.0.1:7890",  # 替换为你的代理地址和端口
    "https": "http://127.0.0.1:7890",  # 替换为你的代理地址和端口
}


# 通用的图片抓取函数
def get_image_urls(url):
    """
    获取网页中所有图片的 URL。
    如果页面是动态加载的，可以考虑使用 Requests-HTML 或 Selenium 进行渲染。
    """
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64 Safari/537.36"
        ])
    }

    # 使用代理
    proxies = PROXY if USE_PROXY else None

    # 请求网页内容
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code != 200:
        print(f"❌ 页面加载失败: {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # 查找所有图片的 src 属性
    img_tags = soup.find_all("img")
    img_urls = [img["src"] for img in img_tags if "src" in img.attrs]

    # 处理相对路径
    img_urls = [urljoin(url, img_url) for img_url in img_urls]

    return img_urls


# 判断图片类型
def get_image_extension(img_url):
    """
    判断图片类型。
    """
    try:
        response = requests.get(img_url, stream=True, proxies=PROXY if USE_PROXY else None)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if "image" in content_type:
                img = Image.open(BytesIO(response.content))
                return img.format.lower()  # 返回图片格式 (jpg, png, gif 等)
    except Exception as e:
        print(f"❌ 获取图片格式错误: {e}")
    return None


# 下载单张图片
def download_image(img_url, output_dir, retries=3):
    """
    下载单张图片并保存到本地。
    """
    try:
        # 获取图片格式
        img_extension = get_image_extension(img_url)
        if img_extension:
            img_name = os.path.join(output_dir, f"{random.randint(1000, 9999)}.{img_extension}")

            for attempt in range(retries):
                try:
                    response = requests.get(img_url, stream=True, proxies=PROXY if USE_PROXY else None)
                    if response.status_code == 200:
                        with open(img_name, "wb") as f:
                            f.write(response.content)
                        print(f"✅ 下载成功: {img_name}")
                        break  # 成功后跳出重试循环
                    else:
                        print(f"⚠️ 下载失败: {img_url}")
                        break
                except Exception as e:
                    print(f"❌ 请求错误，第 {attempt + 1} 次重试: {e}")
                    time.sleep(2)  # 重试前等待
        else:
            print(f"⚠️ 无法确定图片格式: {img_url}")
    except Exception as e:
        print(f"❌ 下载图片错误: {e}")


# 下载所有图片
def download_images(image_urls, output_dir):
    """
    下载所有图片，并使用线程池加速下载。
    """
    max_threads = min(20, len(image_urls))  # 根据图片数量调整线程数
    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for img_url in image_urls:
            executor.submit(download_image, img_url, output_dir)

    print("🎉 所有图片下载完成！")


# 主程序
def main(url, output_dir):
    """
    主程序：抓取网页中的所有图片并下载。
    """
    print("🚀 开始抓取网页中的图片...")
    image_urls = get_image_urls(url)
    if image_urls:
        print(f"🎯 找到 {len(image_urls)} 张图片，开始下载...")
        download_images(image_urls, output_dir)
    else:
        print("❌ 没有找到图片，或者页面加载失败")


# 运行示例
if __name__ == "__main__":
    URL = "https://x.com/xiaoqing6666/media"  # 目标网站 URL
    OUTPUT_DIR = r"D:\素菜库\youtube\image\X\新建文件夹"  # 本地保存目录
    main(URL, OUTPUT_DIR)
