## This script will take a csv containing a series of urls as input.
## It will then visit each url, storing the webpage text and translating to english using the googtrans api.
## This will then be added to the original csv containing all results manually.
import os
import time
import re
import csv
import pandas as pd

from selenium import webdriver
from google_trans_new import google_translator  

def get_page_content(browser, translator):
    contents = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
    output = []

    for content in contents:
        page_source = browser.find_elements_by_tag_name(content)
        for elem in page_source:
            result = elem.text
            if (len(result) != 0):
                result.strip()
                output.append(result)
    
    out = ''.join(output)
    out = out.replace("\n", " ")
    out = re.sub(r' +', ' ', out)
    out = out[:4999]

    return out

def follow_url(url, translator):
    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")

    fp = webdriver.FirefoxProfile()
    fp.set_preference("app.update.auto", False)
    fp.set_preference("app.update.enabled", False)
    fp.set_preference("browser.search.update", False)
    fp.set_preference("extension.logging.enabled", True)
    fp.set_preference("extension.update.enabled", False)
    fp.set_preference("javascript.option.showInconsole", True)

    # display = Display(visible = 0, size = (800, 600))
    # display.start()

    browser = webdriver.Firefox(executable_path=r"./extensions/geckodriver", firefox_options=opts, firefox_profile=fp)
    browser.set_page_load_timeout(60)

    time.sleep(1)

    print(url)

    try:
        browser.get(url)

        # Get and format text
        text = get_page_content(browser, translator)

        # Translate text
        trans = translator.translate(text)

        out = [url, trans]

        with open('translations_2.csv', 'a+') as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(out)

        browser.close()
        browser.quit()

    except Exception as e:
        browser.close()
        browser.quit()

    try:
        browser.close()
        browser.quit()
    except:
        return 1

    return 1

def main():  
    translator = google_translator()  

    results = []
    with open('init_translations_2.csv', newline='') as inputfile: 
        for row in csv.reader(inputfile):
            results.append(row[0])

    translator = google_translator() 

    for url in results:
        try:
            follow_url(url, translator)
        except Exception as e:
            print("error following " + str(url))

    print('done')    


if __name__ == '__main__':
    main()