from selenium import webdriver as webdriver
import time
import datetime
import mysql.connector
from get_followers import logIn

def get_following_count():
    prev_site = driver.current_url
    driver.get('https://www.instagram.com/'+username)
    time.sleep(5)
    following = driver.find_element_by_partial_link_text('following').find_element_by_tag_name('span').text
    driver.get(prev_site)
    return int(following)


username = 'okurka_jindrich'
password = 'ragnarokonline'
currentTable= 'androidFollowers'
maxFollowedPerHour = 10
maxFollowedPerDay = 200
range1 = 50
range2 = 100



chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver', options=chromeOptions)

logIn(username, password)
print(get_following_count())
driver.save_screenshot("/root/Documents/temp/loggedIn.png")

mydb = mysql.connector.connect(
    host='localhost',
    user='root',    
    passwd='toorr',
    database='Followers'
)
sql = mydb.cursor()

sql.execute("SELECT name FROM " + currentTable + " WHERE id >= " + str(range1) + " AND id < " + str(range2))
# time.sleep(2)
usedFollowers = sql.fetchall()

followedThisHour = 0
followedToday = 0
totalHoursElapsed = 0

for i in range(0, range2 - range1):
    followerPage = str(usedFollowers[i]).split("'")[1]
    driver.get(followerPage)
    time.sleep(5)
    try:
        followButton = driver.find_element_by_xpath("//a[@rel='nofollow']")
        print(followerPage + "  OK")
    except: 
        print(followerPage + "  NOT FOUND")
        continue

    following = get_following_count()
    
    try:
        followButton.click()
    except:
        print("couldnt click follow button")
        print("POSSIBLE BAN - PAUSING FOR 1 HOUR")
        time.sleep(3600)
        driver.save_screenshot('/root/Documents/temp/couldnt_click_follow.png')
        continue

    time.sleep(2)
    if(following == get_following_count()):
        for j in range(1,2):
            if (j == 2):
                print("POSSIBLE BAN - PAUSING FOR 1 HOUR")
                time.sleep(3600)
            else:
                time.sleep(3)
                if (get_following_count() != following):
                    break

    followedToday += 1
    followedThisHour += 1
    if (followedThisHour == maxFollowedPerHour):
        time.sleep(3600)
        followedThisHour = 0
        totalHoursElapsed += 1

    if (followedToday == maxFollowedPerDay):
        print("followed today: " + datetime.date.today() + followedToday)
        time.sleep(60 * 60 * 24 - totalHoursElapsed * 3600)
        followedToday = 0
        totalHoursElapsed = 0


# if (followedToday == maxFollowedPerDay):
print('ended at ' +  range1 + followedToday)
exit()


