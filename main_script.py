import os
import re
from sys import exit

import pandas as pd

from selenium import webdriver

from lxml import html
import requests

os.chdir("/Users/michaelpiccirilli/Documents/GitHub/FT/")

def open_browser():
    
    global browser
    browser = webdriver.Firefox()
    browser.get('http://registration.ft.com/registration/barrier')
    
    username_input = raw_input("Please enter your username (email address): ")
    username_submit = browser.find_element_by_id("username")
    username_submit.send_keys(username_input)
    
    password_input = raw_input("Please enter your password: ")
    password_submit = browser.find_element_by_id("password")
    password_submit.send_keys(password_input)
    
    browser.find_element_by_id("loginButton").click() #submit

    
    confirmation = raw_input("Have you logged in yet? (y/n): ")
        
    if confirmation == "y":
        article_search()
    else:
        exit()


def article_search():
    
    global company
    company = raw_input("What company would you like to search for on www.FT.com? ")
    
    beg_url = "http://search.ft.com/search?q=%r" % company
    end_url = '&t=all&rpp=10&fa=people%2Corganisations%2Cregions%2Csections%2Ctopics%2Ccategory%2Cbrand&s=-initialPublishDateTime&f=category%5B"article"%5D%5B"Articles"%5D&ftsearchType=on&curations=ARTICLES%2CBLOGS%2CVIDEOS%2CPODCASTS&highlight=true'

    page = requests.get(beg_url+end_url)
    tree = html.fromstring(page.text)

    article_titles = tree.xpath("//ol/li/h3/a/text()")
    article_links = tree.xpath("//ol/li/h3/a/@href")
    article_date = tree.xpath("//ol/li/div/div/p/text()")
    article_body = []
    
    for i in range(0,len(article_links)):
        try:
            browser.get(article_links[i]) #this is not working --> it passes straight to the exception
            article_body.append(browser.find_element_by_id("storyContent").text)
        except:
            article_body.append("NULL")

    structure = {'date': article_date, 'title': article_titles, 'link': article_links, 
    'body': article_body, 'company': company, 'pos': "", 'neg': "", 'total': "",
    'pos_perc': "", 'neg_perc': ""}
    
    data = pd.DataFrame(structure)
    
    for i in range(0, len(data)):
        temp = data['body'][i]    
        clean = re.sub(r'\W', " ", temp)
        words = pd.DataFrame(re.split(r'\s+', clean))
        tally = pd.DataFrame({"Count": pd.value_counts(words[0])})
        data['pos'][i] = float(sum(pd.merge(pos_words, tally, left_on="Word", right_index=True)['Count']))
        data['neg'][i] = float(sum(pd.merge(neg_words, tally, left_on="Word", right_index=True)['Count']))
        data['total'][i] = float(data['pos'][i]) + float(data['neg'][i])
        
        try:
            data['pos_perc'][i] = float(data['pos'][i])/data['total'][i]
        except:
            data['pos_perc'][i] = 0
        
        try:    
            data['neg_perc'][i] = float(data['neg'][i])/data['total'][i]
        except:
            data['neg_perc'][i] = 0


    data.to_csv("%s.csv" % (company), encoding="utf-8", index=False)
    
    decision_time = raw_input("Would you like to run another search?  If not, you will be logged out and the browser will close. (y/n): ")
    if decision_time == "y":
        article_search()
    else:
        browser.find_element_by_id("ftLogin-logout").click()
        browser.quit()



def start():
    global pos_words, neg_words
    pos_words = pd.read_table("positive-words.txt", skiprows=35, sep="\n", names=["Word"])
    neg_words = pd.read_table("negative-words.txt", skiprows=35, sep="\n", names=["Word"])

    choice = raw_input("Do you need to log into FT.com? (y/n): ")
    if choice == "y":
        open_browser()    
    elif choice == "n":
        article_search()        
    else:
        exit()


start()

