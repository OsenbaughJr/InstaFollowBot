from selenium import webdriver as webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import mysql.connector
from get_followers import logIn
import threading
from random import randint

# threads = []
class BotInstance:

    def __init__(self,username,passwd,currenttable,rangeStart,rangeEnd):
        self.username = username
        self.currentTable= currenttable
        self.range1 = rangeStart
        self.range2 = rangeEnd
        process = threading.Thread(target=self.main)#, args=[self])
        # threads.extend(process)
        process.start()

    def main(self):
    

        username = self.username
        password = 'ragnarokonline'
        currentTable = self.currentTable
        maxFollowedPerHour = randint(9, 19)
        maxFollowedPerDay = randint(150, 200)
        range1 = self.range1
        range2 = self.range2

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('/usr/bin/chromedriver', options=chromeOptions)
        driver = self.driver

        driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        while (True):
            driver.save_screenshot(f"/root/Documents/temp/{username}_outer_loop.png")
            while (True):
                driver.save_screenshot(f"/root/Documents/temp/{username}_inner_loop.png")
                if (str(driver.current_url) == 'https://www.instagram.com/'):
                    break
                try:
                    logInElement = driver.find_element_by_name('username')
                    passwordElement = driver.find_element_by_name('password')
                    logInElement.send_keys(username)
                    passwordElement.send_keys(password)
                    passwordElement.send_keys(Keys.ENTER)
                    #passwordElement
                    break
                except:
                    time.sleep(1)
                    continue
            time.sleep(1)
            if (str(driver.current_url) == 'https://www.instagram.com/'):
                break
        
        print(f"{username} logged in, daily: {maxFollowedPerDay}, hourly: {maxFollowedPerHour}")

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

        for i in range(1, range2 - range1):
            following = self.get_following_count()
            followerPage = str(usedFollowers[i]).split("'")[1]
            driver.get(followerPage)
            time.sleep(5)
            try:
                followButton = driver.find_element_by_xpath("//*[text()='Follow']")
                # print(followerPage + "  OK")
            except Exception as e: 
                print(followerPage + "  NOT FOUND/n" + e)
                driver.save_screenshot(f'/root/Documents/temp/{username}_followbtn_404.png')
                continue

            
            try:
                followButton.click()
                # time.sleep(1)
                # driver.save_screenshot(f'/root/Documents/temp/{username}_clicked.png')
            except Exception as e:
                print(e)
                print(f"{username}: POSSIBLE BAN - COULDNT CLICK FOLLOW")
                driver.save_screenshot(f'/root/Documents/temp/{username}_couldnt_click_follow.png')
                time.sleep(2)
                continue

            time.sleep(2)
            if(following == self.get_following_count()):
                for j in range(1,2):
                    if (j == 2):
                        print(f"{username}: POSSIBLE BAN - PAUSING FOR 1 HOUR")
                        time.sleep(3600)
                    else:
                        time.sleep(3)
                        if (self.get_following_count() != following):
                            break

            followedToday += 1
            followedThisHour += 1
            if (followedThisHour == maxFollowedPerHour):
                print(f"{username}: compoleted this hour max, sleeping")
                time.sleep(3600)
                followedThisHour = 0
                totalHoursElapsed += 1

            if (followedToday == maxFollowedPerDay):
                print(f"{username}: followed today: " + datetime.date.today() + followedToday)
                time.sleep(60 * 60 * 24 - totalHoursElapsed * 3600)
                followedToday = 0
                totalHoursElapsed = 0

        print(f"{username}: completed, currently following: " + str(self.get_following_count))

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
        # print(instance_form)
        # instances.append(str(instance_form))
        instance_id = instance_id + 1

    elif (instance_elements[0]=="stop"):
        print("creating instances completed:")
        # print("     "+instance_elements)
        break

    else:
        print("wrong format")
        continue

# for i in instances:
#     print(instances)
#     print(i)
#     instance_prq = i.split(",")
#     print(instance_prq)
#     instance = BotInstance(instance_prq[0], instance_prq[1], instance_prq[2], int(instance_prq[3]), int(instance_prq[4]))
    # instance = BotInstance(i[0],i[1],i[2],i[3],i[4])
    # instance_id = instance_id + 1
    
    

#zadavat ve formatu (username,passwd,currenttable,rangeStart,rangeEnd); kdyz neni 5 elem ->  kdyz "start" break / continue i--