from selenium import webdriver as webdriver
import time
import datetime
import mysql.connector
from get_followers import logIn
import threading

class BotInstance:

    def __init__(self,username,passwd,currenttable,rangeStart,rangeEnd):
        process = threading.Thread(self.main, args=[self])
        process.start()
        self.username = username
        self.currentTable= currenttable
        self.range1 = rangeStart
        self.range2 = rangeEnd

    def main(self):
    

        username = self.username
        password = 'ragnarokonline'
        currentTable = self.currentTable
        maxFollowedPerHour = 10
        maxFollowedPerDay = 200
        range1 = self.range1
        range2 = self.range2

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('/usr/bin/chromedriver', options=chromeOptions)
        driver = self.driver

        logIn(username, password)
        
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

            following = self.get_following_count()
            
            try:
                followButton.click()
            except:
                print("couldnt click follow button")
                print("POSSIBLE BAN - PAUSING FOR 1 HOUR")
                time.sleep(3600)
                driver.save_screenshot('/root/Documents/temp/couldnt_click_follow.png')
                continue

            time.sleep(2)
            if(following == self.get_following_count()):
                for j in range(1,2):
                    if (j == 2):
                        print("POSSIBLE BAN - PAUSING FOR 1 HOUR")
                        time.sleep(3600)
                    else:
                        time.sleep(3)
                        if (self.get_following_count() != following):
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

    def get_following_count(self):
        prev_site = self.driver.current_url
        self.driver.get('https://www.instagram.com/'+self.username)
        time.sleep(5)
        following = self.driver.find_element_by_partial_link_text('following').find_element_by_tag_name('span').text
        self.driver.get(prev_site)
        return int(following)

print("put instance args in this order: username,passwd,currenttable,rangeStart,rangeEnd:")
instances = []
instance_id = 0
while(True):
    instance_form = input(f"args for instance {instance_id}: ")
    instance_elements = instance_form.split(",")
    if (len(instance_elements) == 5):
        instance = BotInstance(instance_elements[0], instance_elements[1], instance_elements[2], int(instance_elements[3]), int(instance_elements[4]))
        instance_id = instance_id + 1

    elif (instance_elements[0]=="stop"):
        print("creating instances completed:")
        print("     "+instance_elements)
        break

    else:
        print("wrong format")
        continue

#zadavat ve formatu (username,passwd,currenttable,rangeStart,rangeEnd); kdyz neni 5 elem ->  kdyz "start" break / continue i--
