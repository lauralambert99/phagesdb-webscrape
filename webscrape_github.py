# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Import needed packages
import bs4
from selenium import webdriver
import os
import time

from selenium.webdriver.common.by import By


#Set working directory - make sure everything is in the same folder
#Don't forget to put the webdriver in this location, too.
os.getcwd()
os.chdir("C:\\Filepath\\goes\\here")
#%%
#Make empty lists to populate during the web-scraping
temps = []
names = []

#Define what you're opening, and with which webdriver.  
#This website takes a while to load, so build in some sleep time.
driver = webdriver.Chrome()
time.sleep(5)
driver.get('https://phagesdb.org/phages/')
time.sleep(10)

#Need to click next button every 50 entries.  Define a function to find and click the button.
def next_button():
    next_button = driver.find_element(By.CSS_SELECTOR, '#tablenav > div:nth-child(1) > img:nth-child(3)')
    next_button.click()
                           
#Start cycling through the phages
for i in range(1, 4143):
    path = 'tr:nth-child(%d)' %(i)
    extended_path = '#allphages > tbody > ' + path + ' > td:nth-child(1)'
    phage = driver.find_element(By.CSS_SELECTOR, extended_path)
    phage.click()

    page_source = driver.page_source

    soup = bs4.BeautifulSoup(page_source, 'lxml')
    
    soup2 = str(soup.select('#phageDetails > tbody > tr:nth-child(3) > td.detailLabel'))
#Need to set some parameters - temp isn't found in the exact same place for all records.  Check if other records exist
#and if they do, modify where to look for temperature   
    if soup2 != '[<td class="detailLabel">Found By</td>]':
        temp = str(soup.select('#phageDetails > tbody > tr:nth-child(10) > td.detailValue'))
    elif str(soup.select('#phageDetails > tbody > tr:nth-child(6) > td.detailLabel')) != '[<td class="detailLabel">Finding Institution</td>]':
        temp = str(soup.select('#phageDetails > tbody > tr:nth-child(8) > td.detailValue'))
    else: 
        temp = str(soup.select('#phageDetails > tbody > tr:nth-child(9) > td.detailValue'))
#Add the temperature value to the temps list
    temps.append(temp)
#Pull the name, too, and add to name list
#This allows for later matching with other datasets    
    name = str(soup.select('#phageDetails > thead > tr > td'))
    names.append(name)
#Go back to homepage       
    driver.back()
    time.sleep(2)
#Checking if need to click the 'next' button.  If so, click using the predefined function    
    if i % 50 == 0:
        next_button()
