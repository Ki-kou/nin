# -*- coding: utf-8 -*-
import time
import os
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import psycopg2
from psycopg2 import extras
# import pandas as pd


# DATABASE_URL = os.environ.get("postgres://crawueupldowsl:f5db4ae256ae2d2284e35d5cfecb6e5f51ba4fd0cefe3781efc997b54e79674c@ec2-44-194-6-121.compute-1.amazonaws.com:5432/dbsb7u2apfi5h7")

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('/app/.chromedriver/bin/chromedriver', options=options)
# driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)
driver.get('https://www.nintendo.co.jp/software/campaign/index.html')

soft_name_list = ["test"]
while True:
    for element in driver.find_elements_by_class_name("nc3-c-softCard__name"):
        soft_name_list.append(element.text)
    try:
        next_page = driver.find_element_by_class_name("nc3-c-pagination__next")
        next_page.click()
        time.sleep(1)
    except ElementNotInteractableException:
        driver.quit()
        break
with conn.cursor() as cur:
    # テーブルを作成する SQL を準備
    sql = '''
          CREATE TABLE test(
            title   TEXT Not Null 
            
          );
          '''

    # SQL を実行し、テーブル作成
    extras.execute_values(cur, "INSERT INTO data (title) VALUES %s", soft_name_list)
conn.commit()
cur.close()
conn.close()
