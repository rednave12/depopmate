from config import keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import random
import sys
import math

lastSoldItems = []
driver = webdriver.Chrome('./chromedriver')
count = 0
actions = ActionChains(driver)

def openChrome(k):
    global driver
    driver.get(k['profile_url'])
    
    window_before = driver.window_handles[0]
    
    #click log in
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainNavigation"]/li[2]/a'))).click()
    
    #click log in with facebook
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[2]/button'))).click()
    
    time.sleep(5)
    
    window_after = driver.window_handles[1]
    
    driver.switch_to.window(window_after)
    
    time.sleep(5)
    
    #fill in email 
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(k["email"])
    
    #fill in password
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(k["password"])
    
    #click log in 
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="u_0_0"]'))).click()
    
    driver.switch_to.window(window_before)
    
    #close popup
    driver.find_element_by_xpath('//*[@id="__next"]').click()

def search():
    #scroll to bottom to acccess all product elements
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)
    
    #locates sold items
    soldItems = driver.find_elements_by_xpath("//div[contains(text(),'Sold')]")

    global lastSoldItems

    #if we have sold more items since last relist, move them down!
    if len(soldItems) > len(lastSoldItems) and len(lastSoldItems)> 0:
        moveDownSoldItems()
        search()
    
    #stores number of sold items before relisting and updates after comparing to previous round!
    lastSoldItems = soldItems
    
    #locates all items
    allItems = driver.find_elements_by_xpath("//*[@id='products-tab']/div/ul/li")
  
    print("Total Items = " + str(len(allItems)))
    print("Sold Items = " + str(len(soldItems)))
    
    #calculate available items
    global availableItems
    availableItems = len(allItems) - len(soldItems)
    
    print("Available Items = " + str(availableItems))
    
    return availableItems
    
def moveDownSoldItems():
    driver.execute_script("window.scrollTo(0, 0)")
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[4]/div/button[1]').click()
    
def relist(): 
    #refresh page
    driver.refresh()
    
    #get xpath of the last available item
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    xPathOfLastItem = '(//*[@id="products-tab"]/div/ul/li)' + '[' + str(availableItems) + ']/a'
    
    #store id of last available item
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(xPathOfLastItem))
    idOfLastItem = driver.find_element_by_xpath(xPathOfLastItem).get_attribute('href')

    global count
    count = 0
    
    idOfCurrentItem = 'null'
    
    #relist items until the last item is the same as it was when we started - this fixes the bug of items not auto popping to the top of the page. not quite!
    while idOfCurrentItem != idOfLastItem or count < availableItems:
        #find last available item and click
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(xPathOfLastItem))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPathOfLastItem))).click()
        
        #edit
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[3]/div/div[3]/div/a[1]'))
        driver.execute_script("window.scrollBy(0, -50);")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div[3]/div/div[3]/div/a[1]'))).click()
        
        #save changes
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="main"]/form/div[2]/button[1]'))
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/form/div[2]/button[1]'))).click()

        #go back to profile
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/div/p[1]/a'))).click()
        
        #update id of last item
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(xPathOfLastItem))
        idOfCurrentItem = driver.find_element_by_xpath(xPathOfLastItem).get_attribute('href')
        
        time.sleep(random.randrange(5, 10, 1))
        
        count += 1
        
        driver.refresh()


if __name__ == '__main__':
    #open profile
    openChrome(keys)
    
    #time to log in
    time.sleep(30)

    while True:
        search()
        relist()
        print("Relisted " + str(count) + " items.")
        
        #sleep anywhere from 45 to 90 mins & show timer in command prompt
        countdown = random.randrange(2700, 4500, 10)
        for y in range(countdown, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} minutes and ".format(math.floor(y / 60)))
            sys.stdout.write("{:2d} seconds remaining.".format(y % 60))
            sys.stdout.flush()
            time.sleep(1)

        sys.stdout.write("\n")
        sys.stdout.write("\rComplete! \n")
        print("_____________________________________")