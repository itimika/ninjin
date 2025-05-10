import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWai
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self):
        option = Options()
        option.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        
    def run(self, url):
        xpath_list = [
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[1]/span[8]",
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[1]/span[2]",
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[1]/span[5]",
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]",
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/span[2]",
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/span[3]",
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/span[4]",
            "/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/span[5]",
            "/html/body/section[2]/div[1]/h1/div[2]"
        ]
        item_list = []
        yasai_name = ''
        
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        
        for n, xpath in enumerate(xpath_list):
            content = self.driver.find_element(By.XPATH, xpath).text
            if n==1:
                content = int(content.replace(",", ""))
            # 高値、中値、安値
            elif (n==3) or (n==4) or (n==5):
                match = re.search(r'\d{1,3}(?:,\d{3})*', content)
                if match:
                    content = match.group()
                    content = int(content.replace(",", ""))
            # 総入荷量
            elif n==6:
                match = re.search(r'\d+(\.\d+)?', content)
                if match:
                    content = float(match.group())
            # 見通し
            elif n==7:
                content = content.split()[-1]
            elif n==8:
                yasai_name = content[:-3]
            if n != 8:
                item_list.append(content)

        
        return item_list, yasai_name
    
    def close(self):
        self.driver.quit()