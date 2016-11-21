#!/usr/bin/python

import urllib2
import json
import sys
import os
import logging

from bs4 import BeautifulSoup

logging.basicConfig(level='DEBUG')

BASE_URL = "http://docs.hortonworks.com"

TARGET_DIR = "target"

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

class Downloader:

    def __init__(self, url):
        self.url = url
        logging.info("Init URL: [%s]" % url)
        self.target = CURR_DIR + "/../" + TARGET_DIR

    def parse(self):
        #html = urllib2.urlopen(self.url, timeout=30).read()
        parsed_html = BeautifulSoup(open(self.url), "html.parser") 
        content = parsed_html.body.find_all('div', class_="title")
        
        def extract_name(href):
            return href[href.rfind('/') + 1:]
            
        def extract_href(href):
            if href.find('..') > 0:
                ary = href.split("/")
                index = ary.index("..")
                num = 0
                for i in ary:
                    if i == "..":
                        num = num + 1
                del ary[(index - num):(index + num)]
                return '/'.join(ary)
            else:
                return href
            
        for item in content:
            href = item.find('a').find_next('a')['href']
            name = extract_name(href)
            yield (name, BASE_URL + extract_href(href))
                    
        
    def download(self, item): 
        logging.info("Downloading [name=%s, url=%s]" % item)
        p = self.target + "/" + item[0]
        with open(p, 'w') as file:
            logging.info("Saving at [%s]" % p)
            file.write(urllib2.urlopen(item[1]).read())
    
    def main(self):
        # clear
        if os.path.exists(self.target) and os.path.isdir(self.target):
            os.system('rm -rf ' + self.target)
            
        os.mkdir(self.target)
        
        for item in self.parse():
            if os.path.isfile(item[0]) > 0 and os.path.getsize(item[0]) > 0: continue
            self.download(item)        
    
if __name__ == '__main__':

    if len(sys.argv) != 2:
        logging.info("Please giving url which should download.")     
        sys.exit(1)
    
    downloader = Downloader(sys.argv[1])
    downloader.main()
    