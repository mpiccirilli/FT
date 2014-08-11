from sys import exit

from lxml import html
import requests

import selenium
from selenium import webdriver

company = raw_input("What would you like to search FT.com? ")

beg_url = "http://search.ft.com/search?q=%r" % company
end_url = '&t=all&rpp=100&fa=people%2Corganisations%2Cregions%2Csections%2Ctopics%2Ccategory%2Cbrand&s=-initialPublishDateTime&f=category%5B"article"%5D%5B"Articles"%5D&ftsearchType=on&curations=ARTICLES%2CBLOGS%2CVIDEOS%2CPODCASTS&highlight=true'

page = requests.get(beg_url+end_url)
tree = html.fromstring(page.text)

titles = tree.xpath("//ol/li/h3/a/text()")
links = tree.xpath("//ol/li/h3/a/@href")
date = tree.xpath("//ol/li/div/div/p/text()")


browser = webdriver.Firefox()

browser.get('http://registration.ft.com/registration/barrier')

login = raw_input("Have you logged in yet? (y/n) ")

if login != "y":
    sys.exit()



browser.get('http://www.ft.com/intl/cms/s/0/c0a930ae-1408-11e4-b46f-00144feabdc0.html')
browser.get('http://www.ft.com/intl/cms/s/0/2e758a3c-1d6a-11e4-8b03-00144feabdc0.html')

body = []
for i in df_short['links']: 
    browser.get(i)
    body.append(browser.find_element_by_id("storyContent").text)

    
    

element = browser.find_element_by_id("storyContent").text


