from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import random
import time
import bs4

def open_website(URL='https://www.yelp.com/'):
    driver = webdriver.Chrome(executable_path='/Users/rickroma/Desktop/Assignment2/chromedriver')
    driver.get(URL)
    return driver

driver = open_website('https://www.yelp.com/')

def select_location_business(driver, location_input='07030', business_type='Restaurant'):
    # Option 1 to delay
    normal_delay = random.normalvariate(2, 0.5)  # step 1
    time.sleep(normal_delay)  # step 2

    # find the location bar
    # you could use another format @ http://selenium-python.readthedocs.io/locating-elements.html
    active_location_search_input = driver.find_element_by_id("dropperText_Mast")
    # type hoboken in the location bar
    active_location_search_input.clear()
    active_location_search_input.send_keys(location_input)
    # find the business bar

    # Option 2 to delay
    wait = WebDriverWait(driver, 10)  # step 1
    # find the location bar
    # other format @ http://selenium-python.readthedocs.io/waits.html
    active_business_search_input = wait.until(EC.element_to_be_clickable((By.ID, "find_desc")))  # step 2

    # active_restaurant_search_input = active_business_search_div.find_element_by_xpath()
    # type restaurant in the bar
    active_business_search_input.send_keys(business_type)
    # find the search button
    hit_search = driver.find_element_by_id("header-search-submit")
    # click the search button
    search_result = hit_search.click()
    return driver

driver = select_location_business(driver, '07030', 'Restaurant')

laund_popup = """//*[@id="super-container"]/div/div[4]/div/div/div[2]/a"""
select_popup = driver.find_element_by_xpath(laund_popup)
click_laund_popup = select_popup.click()

def select_back_all_re(driver, restaurant_no, ad_no):
    global restaurant_xpath_li, select_business, click_business
    restaurant_no = 10
    ad_no = 0
    restaurant_xpath_li = []
    for i in range(restaurant_no):
        no = str(i + 1 + ad_no)
        re_xpath = """//*[@id="super-container"]/div/div[2]/div[1]/div/div[5]/ul[2]/li[{}]/div/div[1]/div[1]/div/div[2]/h3/span/a"""
        re_xpath = re_xpath.format(no)
        restaurant_xpath_li.append(re_xpath)
    for i in range(len(restaurant_xpath_li)):
        normal_delay = random.normalvariate(3, 0.5)
        time.sleep(normal_delay)
        select_business = driver.find_element_by_xpath(restaurant_xpath_li[i])
        click_business = select_business.click()



        ###after you add above function, please delete following codes
        normal_delay = random.normalvariate(5, 0.5)
        time.sleep(normal_delay)
        driver.back()
        ###

    def click_next_page_review():
        next_page = """//*[@id="super-container"]/div/div[2]/div[1]/div/div[5]/div[1]/div/div/div[2]/div/div[10]/a/span[1]"""
        select_next_page = driver.find_element_by_xpath(next_page)
        click_next_page = select_next_page.click()

    return driver

select_back_all_re(driver, 10, 0)



#def extract_data():


#def store_data():


