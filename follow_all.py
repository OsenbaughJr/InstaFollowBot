from selenium import webdriver as webdriver
import time
import datetime
import mysql.connector
from get_followers import logIn

#read usernames and passwdz from file "usr pswd"

username = 'okurka_jindrich'
password = 'ragnarokonline'
currentTable= 'androidFollowers'
maxFollowedPerHour = 10
maxFollowedPerDay = 200
range1 = "50"
range2 = range1 + maxFollowedPerDay



chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver', options=chromeOptions)

# logIn(username, password)
driver.save_screenshot("/root/Documents/temp/loggedIn.png")

mydb = mysql.connector.connect(
    host='localhost',
    user='root',    
    passwd='toorr',
    database='Followers'
)
sql = mydb.cursor()

sql.execute("SELECT name FROM " + currentTable + " WHERE id > " + range1 + " AND id <= " + range2)
usedFollowers = sql.fetchall()

followedThisHour = 0
followedToday = 0
totalHoursElapsed = 0

for i in range(range1, range2):
    followerPage = str(usedFollowers[i]).split("'")[1]
    print(followerPage)
    driver.get(followerPage)
    time.sleep(5)
    followButton = driver.find_element_by_xpath("//a[@rel='nofollow']")
    followButton.click()
    time.sleep(2)
    followedToday += 1
    followedThisHour += 1
    if (followedThisHour == maxFollowedPerHour):
        time.sleep(3600)
        followedThisHour = 0
        totalHoursElapsed += 1

    if (followedToday == maxFollowedPerDay):
        print("followed today: " + datetime.date.today() + followedToday)
        time.sleep(86400 - totalHoursElapsed * 3600)
        followedToday = 0
        totalHoursElapsed = 0


# if (followedToday == maxFollowedPerDay):
print('ended at ' +  range1 + followedToday)
exit()


