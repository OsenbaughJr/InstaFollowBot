# https://www.instagram.com/accounts/login/?source=auth_switcher

from selenium import webdriver as webdriver
from selenium.webdriver.common.keys import Keys as Keys
import time
import mysql.connector
import sys
    
victim_page = 'android'
number_of_followers_wanted = 10000
username = 'okurka_jindrich'
password = 'ragnarokonline'
namesList = []

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver', options=chromeOptions)

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
    step = 10
    ul = driver.find_elements_by_tag_name('ul')[3]
    div = ul.find_element_by_xpath('..')
    lastId = 0
    scroll = driver.execute_script('return arguments[0].scrollTop;', div)
    while (lastId < number_of_followers_wanted):
        scroll += step
        # driver.save_screenshot('/root/Documents/temp/check.png')
        driver.execute_script('arguments[0].scrollTop += arguments[1];', div, step)
        if (scroll % 1000 == 0):
            # driver.save_screenshot('/root/Documents/temp/check2.png')
            followersList = ul.find_elements_by_tag_name('li')
            flwrListLength = len(followersList)
            if (lastId == flwrListLength):
                driver.save_screenshot('/root/Documents/temp/same_follower_count_list.png')
                driver.execute_script('arguments[0].scrollTop -= 999', div)
                driver.save_screenshot('/root/Documents/temp/same_follower_count_list-new_scroll.png')
                # scrollTop = 0 / -=
            else:
                lastId = flwrListLength
                print(lastId)
            if (lastId > number_of_followers_wanted):
                for follower in followersList:
                    aList = follower.find_elements_by_tag_name('a')
                    namesList.append(aList[0].get_property('href'))
                break

def main():
    logIn(username, password)
    loadFollowersPage()
    wrtieUsernames() #doing nothing bug

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


if (__name__ == "__main__"):
    main()

# ul[3]:
# find all li, write last index, load next, start from last
# foreach save profile name to db_pgname(changed -> if url not username, skip) -7.5k ea-
# 

