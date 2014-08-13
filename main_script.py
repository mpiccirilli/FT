from sys import exit

import pandas as pd

import selenium
from selenium import webdriver

from lxml import html
import requests



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
    
    company = raw_input("What company would you like to search for on www.FT.com? ")
    
    beg_url = "http://search.ft.com/search?q=%r" % company
    end_url = '&t=all&rpp=10&fa=people%2Corganisations%2Cregions%2Csections%2Ctopics%2Ccategory%2Cbrand&s=-initialPublishDateTime&f=category%5B"article"%5D%5B"Articles"%5D&ftsearchType=on&curations=ARTICLES%2CBLOGS%2CVIDEOS%2CPODCASTS&highlight=true'

    page = requests.get(beg_url+end_url)
    tree = html.fromstring(page.text)

    article_titles = tree.xpath("//ol/li/h3/a/text()")
    article_links = tree.xpath("//ol/li/h3/a/@href")
    article_date = tree.xpath("//ol/li/div/div/p/text()")
    article_body = []
    for i in article_links:
        try:
            browser.get(i)
            article_body.append(browser.find_element_by_id("storyContent").text)
        except:
            body[i] = "NULL"

    data = {'date': article_date, 'title': article_titles, 'link': article_links, 'body': article_body, 'company': company}
    df = pd.DataFrame(data)
 
    decision_time = raw_input("Would you like to run another search?  If not, you will be logged out and the browser will close. (y/n): ")
    
    if decision_time == "y":
        article_search()
    else:
        browser.find_element_by_id("ftLogin-logout").click()
        browser.quit()


def start():
    choice = raw_input("Do you need to log into FT.com? (y/n): ")
    if choice == "y":
        open_browser()    
    elif choice == "n":
        article_search()        
    else:
        exit()


start()