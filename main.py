from calendar import c
from email import message
from itertools import count
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import socket


from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
import pyautogui
import pyperclip
import csv
import pandas as pd
from glob import glob
import os 
import random
import pickle
import re, itertools
from lxml import etree
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-notifications")


insta_email = input("Enter your instagram email: ")
insta_password = input("Enter your  instagram password: ")
f = open("message.txt", "r", encoding="utf-8")
my_message = f.read()



already_sent_message = []
count = 0

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

with open('already_send_message.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        if "/" in row[0]:
            already_sent_message.append(row[0])


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(10)


driver.find_element(By.NAME, 'username').send_keys(insta_email)
driver.find_element(By.NAME, 'password').send_keys(insta_password)

        
driver.find_element(By.XPATH, "//button[@type='submit']").click()

time.sleep(10)
WebDriverWait(driver, 60000).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@id,'mount')]")))
driver.get("https://www.instagram.com")
time.sleep(3)
with open('profile_links.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        if '/' in row[0] and row[0] not in already_sent_message:
            print(row[0])
            driver.get("https://www.instagram.com"+row[0])
            time.sleep(15)
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")

            buttons = soup.find_all('button')

            time.sleep(2)

            for i in buttons:
                print(i.text)
                if i.text == 'Message':
                    my_xpath = str(xpath_soup(i))
                    driver.find_element(By.XPATH, my_xpath).click()
                    time.sleep(10)
                    try:
                        driver.find_element(By.TAG_NAME, "textarea").send_keys(my_message)
                        time.sleep(10)
                        # pyautogui.press('enter')
                        driver.find_element(By.TAG_NAME, "textarea").send_keys(Keys.RETURN)

                        time.sleep(3)
                        already_sent_message.append(row[0])
                        already_sent_message_np = np.array(already_sent_message)
                        already_sent_message_pamdas = pd.DataFrame({"Profile Link" : already_sent_message_np})
                        already_sent_message_pamdas.to_csv("already_send_message.csv", index=False)  
                        count = count +1

                        break
                    except:
                        print("Error occured----")
                else:
                    already_sent_message.append(row[0])
                    already_sent_message_np = np.array(already_sent_message)
                    already_sent_message_pamdas = pd.DataFrame({"Profile Link" : already_sent_message_np})
                    already_sent_message_pamdas.to_csv("already_send_message.csv", index=False)  

        print(count)    
        if count == 40:
            break







