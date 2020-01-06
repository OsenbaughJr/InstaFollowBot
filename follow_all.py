from selenium import webdriver as webdriver
import time
import mysql.connector
from get_followers import logIn

username = 'okurka_jindrich'
password = 'ragnarokonline'
currentTable= 'androidFollowers'
range1 = "50"
range2 = "60"

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver', options=chromeOptions)

# logIn(username, password)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',    
    passwd='toorr',
    database='Followers'
)
sql = mydb.cursor()

sql.execute("SELECT name FROM " + currentTable + " WHERE id > " + range1 + " AND id <= " + range2)
usedFollowers = sql.fetchall()

for i in range(range2 - range1):
    followerPage = str(usedFollowers[i]).split("'")[1]
    print(followerPage)

driver.get(followerPage)
time.sleep(5)

followButton = driver.find_element_by_xpath("//a[@rel='nofollow']")
followButton.click()
time.sleep(2)
driver.save_screenshot("/root/Documents/temp/isPageLoaded.png")
