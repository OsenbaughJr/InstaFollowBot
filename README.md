# InstaFollowBot
Python3 Selenium Instagram Follow Bot

get_followers.py:
  Saves followers to mysql db.
  Required actions before launching:
    fully working python3, selenium, mariadb
    need to start mysql service
    create database, set mysql login in code
    set instagram username, password in code
    set instagram page name/alias from which to get followers in code
    

follow_all.py:
  Follows all users of set range from database
  Required actions before launching:
    successfully launch get_followers.py
    same preparation
  //*[@id="react-root"]/section/main/div/header/section/div[1]/button
