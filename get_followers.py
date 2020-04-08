#!/usr/bin/env python3
	
# https://www.instagram.com/accounts/login/?source=auth_switcher

from selenium import webdriver as webdriver
from selenium.webdriver.common.keys import Keys as Keys
import time
import mysql.connector
import sys
import threading

victim_page = 'justinbieber'
number_of_followers_wanted = 54000
username = 'okurka_jindrich'
password = 'ragnarokonline'
namesList = []

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chromeOptions)

global searchForFollowers
searchForFollowers = True

def logIn(usr, psw):
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    while (True):
        while (True):
            if (str(driver.current_url) == 'https://www.instagram.com/'):
                break
            try:
                logInElement = driver.find_element_by_name('username')
                passwordElement = driver.find_element_by_name('password')
                logInElement.send_keys(usr)
                passwordElement.send_keys(psw)
                passwordElement.send_keys(Keys.ENTER)
                passwordElement
                break
            except:
                time.sleep(1)
                continue
        time.sleep(1)
        if (str(driver.current_url) == 'https://www.instagram.com/'):
            break
        else:
            print('else')
            driver.save_screenshot('/root/Documents/temp/not_logged.png')    
    print('attempted to log in, url: ' + driver.current_url)

def loadFollowersPage():
    followSubPage = '/' + victim_page
    driver.get('https://www.instagram.com'+followSubPage)
    print('attempted to load victim page, url: ' + driver.current_url)
    while (True):
        try:
            # followBtnElement = driver.find_element_by_link_text(followSubPage+'/followers/')
            driver.find_element_by_xpath('//a[@href="' + followSubPage + '/followers/"]').click()
            break
        except:
            time.sleep(1)
            continue

    print('attempted to load followers pgae, url: '+driver.current_url)
    time.sleep(2)

def wrtieUsernames():
    step = 50
    time.sleep(2)
    driver.save_screenshot('/root/Documents/temp/bP.png')
    ul = driver.find_elements_by_tag_name('ul')[3]
    div = ul.find_element_by_xpath('..')
    lastId = 0
    #t1 = time.perf_counter()
    #t2 = 0
    scrollEnd = number_of_followers_wanted * 54
    scroll = driver.execute_script('return arguments[0].scrollTop;', div)
    prevScroll = 0
    while (scroll < scrollEnd and searchForFollowers): #(lastId < number_of_followers_wanted):
        try:
            scroll = driver.execute_script('return arguments[0].scrollTop;', div)
        # driver.save_screenshot('/root/Documents/temp/check.png')
            driver.execute_script('arguments[0].scrollTop += arguments[1];', div, step)
           # ul.send_keys(Keys.PAGE_DOWN)
           # time.sleep(1)
            print(f'{scroll} / {scrollEnd}', end = '\r')
            if (prevScroll == scroll):
               # pri
               # driver.save_screenshot('/root/sameSroll.png')
                time.sleep(1)
                driver.execute_script('arguments[0].scrollTop+= arguments[1];', div, step)
                scroll = driver.execute_script('return arguments[0].scrollTop;', div)
                if (prevScroll == scroll):
                    driver.execute_script('arguments[0].scrollTop -= 158;', div)
                    driver.save_screenshot('/root/sameSroll.png')
                    print('not loaded, revamping\n')
            prevScroll = scroll
        except:
            driver.save_screenshot('/root/Documents/temp/KeyboardInterrupt.png')
            print('while interrupted, continuing..')
            driver.quit()
            break

    # driver.save_screenshot('/root/Documents/temp/check2.png')
    followersList = ul.find_elements_by_tag_name('li')
    flwrListLength = len(followersList)
    if (lastId == flwrListLength):
        driver.save_screenshot('/root/Documents/temp/same_follower_count_list.png')
        driver.execute_script('arguments[0].scrollTop -= 999', div)
        driver.save_screenshot('/root/Documents/temp/same_follower_count_list-new_scroll.png')
                # scrollTop = 0 / -=
        # else:
                #lastId = flwrListLength
               # t2 = time.perf_counter() - t1
              #  print(str(lastId) + ", time elapsed: " + str(t2))
             #   t1 = time.perf_counter()
            #if (lastId > number_of_followers_wanted):
    for follower in followersList:
        aList = follower.find_elements_by_tag_name('a')
        namesList.append(aList[0].get_property('href'))
    print("completed")

def stopScraping():
    input()
    global searchForFollowers
    searchForFollowers = False

def main():
    #try:
    followLoop = threading.Thread(target=wrtieUsernames)
    stopper = threading.Thread(target=stopScraping)
    logIn(username, password)
    loadFollowersPage()
    #followLoop.start()
    stopper.start()
    wrtieUsernames()
    #except Exception as f:
     #   driver.save_screenshot("whatthefuckisgoingon.png")

    tableName = victim_page + 'Followers'
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='toorr',
        database='Followers'
    )
    sql = mydb.cursor()

    while True:
        try:
            for item in namesList:
                expression = ("INSERT INTO " + tableName + " (name) VALUES (%s)")
                sql.execute(expression, (item,))
        except Exception as e:
            sql.execute("CREATE TABLE "+ tableName +" (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
            continue
        break

    mydb.commit()
    driver.quit()


if (__name__ == "__main__"):
    main()

# ul[3]:
# find all li, write last index, load next, start from last
# foreach save profile name to db_pgname(changed -> if url not username, skip) -7.5k ea-
# 