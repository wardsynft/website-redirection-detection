import link_follower
from pyvirtualdisplay import Display
from selenium import webdriver
import os

## Function that imports a list of URLs and saves them in a list
def import_urls():
    with open('url_list.txt') as f:
        url_list = [url.strip() for url in f.readlines()]
    return url_list

def follow_links(url_list):
    for url in url_list:
        try:
            follower = link_follower.LinkFollow(url=url)
            #print "Following Search Result : " + str(l[0]) + " as normal direct link"
            #print l[6]
            result_direct = follower.follow_link(url)
            print("Followed Search Result: " + str(url))
            continue
        except Exception as e:
            print(e)
            print("Error Following Search Result: " + str(url) + " as direct link")

            # remove d
            continue


def main():
    url_list = import_urls()
    follow_links(url_list)



if __name__ == '__main__':
    main()