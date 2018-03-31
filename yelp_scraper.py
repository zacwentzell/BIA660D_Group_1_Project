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

#def restaur_hoboken(data_element):
#for rows in data_element:

#Select restaurant

search_header_bar = driver.find_element_by_class_name('regular-search-result')
rest_header_bar = search_header_bar.find_element_by_class_name('media-story')
rest_line_items = rest_header_bar.find_element_by_tag_name('a')
rest_line_items.click()

wait = WebDriverWait(driver, 10)

driver.back()

