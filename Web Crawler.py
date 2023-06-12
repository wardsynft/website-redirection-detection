#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import re


# In[2]:


def create_webdriver():
    chromedriver_path = 'Chromedriver/chromedriver'
    return webdriver.Chrome(executable_path=chromedriver_path)

def get_urls(url):
    
    browser = create_webdriver()
    browser.get(url)

    timeout = 5

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'result-list'))
        WebDriverWait(browser, timeout).until(element_present)
        elements = browser.find_elements_by_class_name("result-item-heading")
        return elements
    except TimeoutException:
        print("Timed out waiting for page to load")
        return None

def __main__():
    keywords = pd.read_csv("keywords_list.txt", header=None)[0]
    keywords = [re.sub(r'\s+', '%20', x) for x in keywords]
    url_list = []
    file = open("url_list.txt","w")
    for keyword in keywords:
        url = "https://web.archive.org/web/*/" + keyword
        links = get_urls(url)
        if (links != None):
            for link in links:
                url_list.append(link.text)
                file.write(link.text + "\n")
    file.close()
        
    

if __name__ == "__main__":
    __main__()


# In[ ]:




