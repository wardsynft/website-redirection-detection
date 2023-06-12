# This script is designed to use the google api to produce a set number of top search results
# for a list of given keywords.
from googlesearch import search

def import_keywords():
    with open('keywords_v2.txt') as f:
        keywords = [keyword.strip() for keyword in f.readlines()]
    return keywords

def get_urls(keywords):
    f = open("url_list.txt", "a")
    for keyword in keywords:
        for url in search(keyword, tld="com", safe='off', num=25, stop=50, pause=20):
            f.write(url + '\n')
    f.close()
    return "Success"

def main():
    keywords = import_keywords()
    returnState = get_urls(keywords)
    print(returnState)

if __name__ == '__main__':
    main()