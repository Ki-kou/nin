import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import psycopg2

host= "ec2-44-194-6-121.compute-1.amazonaws.com"
port= 5432
users= "crawueupldowsl"
dbnames= "dbsb7u2apfi5h7"
passwords = "f5db4ae256ae2d2284e35d5cfecb6e5f51ba4fd0cefe3781efc997b54e79674c"

# class Book(object):
#     def __init__(self, author, title, publish_date):
#         self.author = author
#         self.title = title
#         self.publish_date = publish_date

def get_connection(): 
    return psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'
        .format( 
            user=users, password=passwords, host=host, port=port, dbname=dbnames
        ))

def insert_execute(con, slq):
    with con.cursor() as cur:
        cur.execute(slq, (2,'Z'))

    con.commit()

conn = get_connection() 


options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)
driver.get('https://www.nintendo.co.jp/software/campaign/index.html')

soft_name_list = ["test"]
while True:
    for element in driver.find_elements_by_class_name("nc3-c-softCard__name"):
        soft_name_list.append(element.text)
    try:
        next_page = driver.find_element_by_class_name("nc3-c-pagination__next")
        next_page.click()
        time.sleep(3)
    except ElementNotInteractableException:
        driver.quit()
        break
if __name__ == '__main__':

    sql =  """insert
                into test(id,
                          name)
                      values(%s,
                             %s)"""

    # データ登録
    insert_execute(conn, sql)