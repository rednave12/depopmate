from config import keys
from selenium import webdriver
import time
import random

#I want to find a way to find the first sold item and therefore figure out how many items I am selling.


def relist(k): 
    driver = webdriver.Chrome('./chromedriver')
    driver.get(k['profile_url'])
    
    time.sleep(30)
    
    while True:
        
        driver.refresh()
        
        #all below should be in a loop :)
        
        for x in range(numberOfItemsPlusOne):
        
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            
            time.sleep(random.randrange(3, 7, 1))
            
            #item li[22] is important to be numberofitems
            driver.find_element_by_xpath('//*[@id="products-tab"]/div/ul/li[22]/a').click()
            
            time.sleep(random.randrange(3, 7, 1))
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
            
            time.sleep(random.randrange(3, 7, 1))
            
            #edit
            driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[3]/div/div[3]/div/a[1]').click()
            
            time.sleep(random.randrange(3, 7, 1))
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
            
            time.sleep(random.randrange(3, 7, 1))
            
            #save changes
            driver.find_element_by_xpath('//*[@id="main"]/form/div[2]/button[1]').click()
            
            time.sleep(random.randrange(5, 10, 1))
            
            #GO BACK TO PROFILE
            driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/p[1]/a').click()
            
            time.sleep(random.randrange(3, 7, 1))
            
        
        time.sleep(random.randrange(2700, 5400, 10))
    

if __name__ == '__main__':

    numberOfItemsPlusOne = 23
    
    relist(keys)