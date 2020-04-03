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
    
follow_many.py:
  from "follow_all.py" clone - added the ability to run multiple bots in 1 sript thanks to OOP, Threading
  
