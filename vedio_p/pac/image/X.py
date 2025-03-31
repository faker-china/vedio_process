#只需要根据不同网站的页面结构和图片的 URL 特征修改 XPath 或 CSS selector，就可以抓取任何网站的图片。
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
import random
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from io import BytesIO
from datetime import datetime

# 配置目标页面和本地保存目录
URL = "https://x.com/yuepaosex/media"  # 替换为目标主页
OUTPUT_DIR = r"D:\素菜库\youtube\image\X\做你的女朋友"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # 创建目录

# 随机选择 User-Agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64 Safari/537.36"
]

# 初始化 Selenium 配置
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")  # 随机选择 User-Agent
    chrome_options.add_argument(
        r"--user-data-dir=C:\Users\bilingbiling\AppData\Local\Google\Chrome\User Data")  # 本地登录会话路径
    chrome_options.add_argument("--profile-directory=Default")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


# 获取完整图片 URL
def get_full_image_url(img_element):
    img_url = img_element.get_attribute("src")
    if not img_url:
        img_url = img_element.get_attribute("data-src")  # 针对懒加载的情况
    if img_url and not img_url.startswith("http"):
        # 如果是相对路径，拼接为完整 URL
        img_url = f"https://x.com{img_url}"
    return img_url


# 滚动加载页面并等待图片加载
def scroll_page(driver, max_scrolls=30):  # 增加滚动次数
    previous_count = 0
    scroll_count = 0
    img_elements = []

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(3, 7))  # 增加等待时间，确保图片有时间加载
        try:
            # 使用显式等待等待图片元素加载完成
            WebDriverWait(driver, 20).until(  # 增加等待时间
                EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@src, 'twimg.com/media')]"))
            )
            img_elements = driver.find_elements(By.XPATH, "//img[contains(@src, 'twimg.com/media')]")
        except Exception as e:
            print(f"❌ 页面加载时出现错误：{e}")
            break

        current_count = len(img_elements)
        if current_count == previous_count:  # 无新内容加载
            print("🚩 无新图片加载，停止滚动")
            break
        previous_count = current_count
        scroll_count += 1
        print(f"📜 已滚动 {scroll_count} 次，找到 {current_count} 张图片")

    # 提取完整的图片 URL
    return [get_full_image_url(img) for img in img_elements if get_full_image_url(img)]


# 判断图片类型
def get_image_extension(img_url):
    try:
        response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, stream=True)
        if response.status_code == 200:
            # 使用Pillow判断图片类型
            img = Image.open(BytesIO(response.content))
            img_format = img.format.lower()  # 获取图片格式，转换为小写
            return img_format
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求错误: {e}")
    except Exception as e:
        print(f"❌ 获取图片格式错误: {e}")
    return None


# 下载单张图片
def download_image(img_url, output_dir, index, retries=3):
    try:
        # 获取图片格式
        img_extension = get_image_extension(img_url)
        if img_extension:
            # 添加时间戳来避免覆盖
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_name = f"image_{index}_{timestamp}.{img_extension}"
            img_path = os.path.join(output_dir, img_name)

            for attempt in range(retries):
                try:
                    response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
                    if response.status_code == 200:
                        with open(img_path, "wb") as f:
                            f.write(response.content)
                        print(f"✅ 下载成功: {img_path}")
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


# 下载图片并保存到本地
def download_images(image_urls, output_dir):
    # 动态调整最大线程数
    max_threads = min(20, len(image_urls))  # 根据图片数量调整线程数，最多不超过20个线程
    failed_urls = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for i, img_url in enumerate(image_urls):
            future = executor.submit(download_image, img_url, output_dir, i)
            result = future.result()  # 等待线程执行结果
            if not result:
                failed_urls.append(img_url)

    # 记录下载失败的 URL
    if failed_urls:
        with open(os.path.join(output_dir, "failed_urls.txt"), "w") as f:
            f.write("\n".join(failed_urls))
        print(f"⚠️ 下载失败的图片 URL 已保存到: {os.path.join(output_dir, 'failed_urls.txt')}")


# 主程序
if __name__ == "__main__":
    driver = init_driver()
    try:
        print("🚀 正在打开目标页面...")
        driver.get(URL)
        time.sleep(5)  # 初始加载等待
        print("🔄 开始滚动页面加载图片...")
        image_urls = scroll_page(driver)
        print(f"🎯 共找到 {len(image_urls)} 张图片")
    except Exception as e:
        print(f"❌ 页面加载或爬取出错: {e}")
    finally:
        driver.quit()  # 确保浏览器关闭
        print("🌐 浏览器已关闭")

    if image_urls:
        print("📥 开始下载图片...")
        download_images(image_urls, OUTPUT_DIR)
        print("🎉 图片爬取完成！")
