# 安装 pip install selenium 依赖
# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 安装浏览器驱动
# Chromedriver的下载地址如下：
# 官方下载地址为https://chromedriver.storage.googleapis.com/index.html
# 其他下载地址为http://npm.taobao.org/mirrors/chromedriver/
# pip install webdriver-manager

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.suning.com/")
input = driver.find_element(by=By.ID, value="searchKeywords")   # 查找输入框
input.clear()   # 清除输入框默认文字
input.send_keys("茅台")
input.send_keys(Keys.RETURN)    # 回车
wait = WebDriverWait(driver, 10)    # 等待时间 10s
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'root990')))  # 等待最多10s，直到某个标签被加载
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
print(driver.page_source)