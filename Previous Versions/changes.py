#we need to redesign the relist function so that the program knows when an item has been recently relisted or not.
#on the edit page xpath for when the item was relisted
//*[@id="main"]/div[1]/div[3]/div/div[2]/div/time
#does string contain minutes? If no, relist
#IF yes, does it contain number <45? If no, relist.
#otherwise move on to the previous!

def relist(): 
    #refresh page
    driver.refresh()
    
    #get xpath of the last available item
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    xPathOfItem = '(//*[@id="products-tab"]/div/ul/li)' + '[' + str(availableItems) + ']/a'
    
    #store id of last available item
    idOfFinalItem = driver.find_element_by_xpath(xPathOfItem).get_attribute('href')

    global count
    count = 0
    
    idOfCurrentItem = 'null'
    
    #relist items until the last item is the same as it was when we started - this fixes the bug of items not auto popping to the top of the page. not quite!
    while idOfCurrentItem != idOfFinalItem or count < availableItems:
        #find last available item and click
        driver.implicitly_wait(10)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(xPathOfItem))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPathOfItem))).click()
        
        #perform time checks
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[3]/div/div[3]/div/a[1]'))
        driver.execute_script("window.scrollBy(0, -50);")
        timeLastListed = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[3]/div/div[2]/div/time')
        
        if "minutes" in timeLastListed:
            availableItems -= 1
            xPathOfItem = '(//*[@id="products-tab"]/div/ul/li)' + '[' + str(availableItems) + ']/a'
            driver.get(k['profile_url'])
            continue
        
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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        idOfCurrentItem = driver.find_element_by_xpath(xPathOfLastItem).get_attribute('href')
        
        time.sleep(random.randrange(5, 10, 1))
        
        count += 1
        
        driver.refresh()