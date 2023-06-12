from pyvirtualdisplay import Display
from selenium import webdriver
import time
import nltk
import re
import string
import csv
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os


#HEADLESS: 0 = Not headless, 1 = headless mode
HEADLESS = 0
display = 0

#Maximum number of times to retry loading a page
MAX_RETRY = 5

#Not sure if the local dir changes for some strange reason
har_folder = "./har_files/"
har_folder = "/data/projects/redirects-sandbox/search_redirect/har_files/"

#Folder to store screenshots in
screenshot_folder = "./screenshots/"

#Folder to store extensions in
extensions_folder = "./extensions/"

class LinkFollow:

    browser = 0
    display = 1
    har_folder = ""
    screenshot_folder = ""
    headless = 1	
    max_retry = 5
    timeout = 10
    
    
    def __init__(self, url, max_retry = 2, headless = 0, timeout = 120, referer = "", user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"):
        self.max_retry = max_retry
        self.headless = headless
        self.timeout = timeout
        
        #Generate random number and use that to create unique folders for har files and screnhots
        self.har_folder = "./source_files/" + str(url) + "/"
        self.screenshot_folder = "./screenshots/" + str(url) + "/"
    
        if not os.path.exists(self.har_folder):
            os.makedirs(self.har_folder)
        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)
        
        opts = webdriver.FirefoxOptions()
        opts.add_argument("--headless")

        fp = webdriver.FirefoxProfile()
        fp.set_preference("app.update.auto", False)
        fp.set_preference("app.update.enabled", False)
        fp.set_preference("browser.search.update", False)
        fp.set_preference("extension.logging.enabled", True)
        fp.set_preference("extension.update.enabled", False)
        fp.set_preference("javascript.option.showInconsole", True)

        #If headless mode is selected, emululate a display so the browser can run
        if self.headless:
            self.display = Display(visible = 0, size = (800, 600))
            self.display.start()


        #Create the browser object
        self.browser = webdriver.Firefox(executable_path=r"./extensions/geckodriver", firefox_options=opts, firefox_profile=fp)
        self.browser.set_page_load_timeout(self.timeout)

        
        #Wait for things to init before we return
        time.sleep(2)

    def __del__(self):
        #Check in case the browser variable was never set, dont want to throw exception
        if type(self.browser) is int:
            return

        try:
            self.browser.quit()
        except:
            pass
        #self.browser.quit()


    # Get heading and paragraph elements.
    # Tokenize and remove stopwords
    def get_page_content(self, filename):
        contents = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
        
        # for each elements -> save text to file
        # Pre-processing steps
        # 1. convert to lowercase
        # 2. remove numbers
        # 3. remove special characters
        # 4. remove white spaces
        # 5. expand abbreviations
        # 6. remove stop words
        # 7. tokenize text
        # 8. stemming / lemmatization (maybe?) -> could be another script
        with open('%s/%s.txt' % (self.har_folder, filename), "w") as source_file:
            for content in contents:
                page_source = self.browser.find_elements_by_tag_name(content)
                for elem in page_source:
                    result = elem.text
                    # convert to lowercase
                    result = result.lower()

                    # remove numbers
                    result = re.sub(r'\d+', '', result)

                    # remove special characters / punctuation
                    result = result.translate(str.maketrans('','',string.punctuation))
                    result = result.replace('"', "")
                    result = result.replace("'", "")

                    # remove leading / trailing whitespace
                    result = result.strip()

                    # tokenize and remove stopwords
                    text_tokens = word_tokenize(result)
                    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
                    filtered_sentence = (" ").join(tokens_without_sw)
                    source_file.write(filtered_sentence + "\n")
        source_file.close()


    def follow_link(self, url, depth=1):
        #print "Following redirection chain of " + url
        print(url)

        ## Search initial URL -> save links and screenshot
        self.browser.get(url)
        links = []

        print("-----saving screenshot-----")
        self.browser.save_screenshot('%s/original.png' % self.screenshot_folder)
        print("Finished collecting the screenshot")

        print("-----saving source code-----")
        self.get_page_content('original')
        print("Finished saving the source code")

        row = [url, url, "original"]

        # Write links to csv
        with open("redirections.csv", "a+") as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(row)


        print("-----Getting links from URL-----")
        elems = self.browser.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                # print('saving screenshot of' + href)
                links.append(href)

        # remove duplicate links from href values
        links = list(dict.fromkeys(links))

        i = 0 # naming index
        for link in links:
            try:
                self.browser.get(link)
                i += 1
                self.browser.save_screenshot('%s/%d.png' % (self.screenshot_folder, i))
                self.get_page_content(str(i))

                row = [url, link, str(i)]

                with open("redirections.csv", "a+") as fp:
                    wr = csv.writer(fp, dialect='excel')
                    wr.writerow(row)

                print(link + " --> successful")
            except Exception as e:
                print(link + " --> failed")
                continue

        return (int(time.time()))
            

                    