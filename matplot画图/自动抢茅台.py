#调用
import time

import win32com.client

speaker=win32com.client.Dispatch("SAPI.Spvoice")

times='2023-09-12 18:49:10'


driver=webdriver.Edge()

driver.get("https://taobao.com")

time.sleep(3)


driver.find_element()