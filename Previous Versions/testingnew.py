from config import keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains                                          
from selenium.webdriver.chrome.options import Options
import time
import random
import sys
import math

#IMPROVEMENTS TO BE MADE:
#IN SEARCH: SCROLL UNTIL WE FIND ALL ITEMS

lastSoldItems = []
options = Options()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument('user-agent={user_agent}')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)
count = 0
actions = ActionChains(driver)
hrefs = []

def openChrome(k):
    global driver
    driver.get(k['profile_url'])
    
    window_before = driver.window_handles[0]
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainNavigation"]/li[2]/a'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[2]/button'))).click()
    
    time.sleep(2)
    
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    
    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="email"]').send_keys(k["email"])
    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(k["password"])
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="u_0_0"]'))).click()

    driver.switch_to.window(window_before)
    driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div/button').click()
    
    time.sleep(5)

def search():
    hrefs.clear()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 500)")

    soldItems = driver.find_elements_by_xpath("//li/a/div/div[contains(text(),'Sold')]")

    global lastSoldItems

    if len(soldItems) > len(lastSoldItems) and len(lastSoldItems) > 0:
        lastSoldItems.clear()
        moveDownSoldItems()
        driver.refresh()
        search()

    lastSoldItems = soldItems
    allItems = driver.find_elements_by_xpath("//*[@id='products-tab']/div/ul/li")
  
    print("Total Items = " + str(len(allItems)))
    print("Sold Items = " + str(len(soldItems)))
    
    availableItems = len(allItems) - len(soldItems)
    print("Available Items = " + str(availableItems))
    
    for x in range(availableItems, 0, -1) : 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        xPathOfItem = '(//*[@id="products-tab"]/div/ul/li)' + '[' + str(x) + ']/a'
        hrefOfItem = driver.find_element_by_xpath(xPathOfItem).get_attribute('href')
        hrefs.append(hrefOfItem)
        
    soldItems.clear()
    allItems.clear()
    availableItems = 0
    
    return hrefs
    
def moveDownSoldItems():
    driver.execute_script("window.scrollTo(0, 0)")
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[4]/div/button[1]').click()

def relist(hrefs, k): 
    global count
    driver.implicitly_wait(10)

    for x in hrefs : 
        x.split('products')
        hrefOfEdit = x.split('products')[0] + 'products/edit' + x.split('products')[1]
        driver.get(hrefOfEdit)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="main"]/form/div[2]/button[1]').click()
        time.sleep(5)
        count += 1
   
    hrefs.clear()
    driver.get(k['profile_url'])
        
if __name__ == '__main__':
    openChrome(keys)

    while True:
        search()
        driver.refresh()
        count = 0
        relist(hrefs, keys)
        print("Relisted " + str(count) + " items.")
        
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