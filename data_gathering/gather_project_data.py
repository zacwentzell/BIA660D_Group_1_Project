from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random
import time
import bs4
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

error_li = []

def open_website(URL='https://www.yelp.com/'):
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(URL)
    return driver


def select_location_business(driver, location_input='07030', business_type='Restaurant'):
    normal_delay = random.normalvariate(2, 0.5)
    time.sleep(normal_delay)

    active_location_search_input = driver.find_element_by_id("dropperText_Mast")
    active_location_search_input.clear()
    active_location_search_input.send_keys(location_input)

    wait = WebDriverWait(driver, 10)
    active_business_search_input = wait.until(EC.element_to_be_clickable((By.ID, "find_desc")))
    active_business_search_input.send_keys(business_type)
    hit_search = driver.find_element_by_id("header-search-submit")
    search_result = hit_search.click()
    return driver


def extract_restaurant_li(driver):
    global restaurant_header_element, soup
    restaurant_header_element = None
    try:
        restaurant_header_element = driver.find_element_by_class_name("""biz-page-header""")
        data_html = restaurant_header_element.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(data_html, 'html5lib')
    except:
        print('Error:detect header.')
        pass
    # res_name

    restaurant_name_element = soup.find('h1', attrs={'class': "biz-page-title"})
    restaurant_name = restaurant_name_element.text.split()
    restaurant_name = ' '.join(restaurant_name)

    try:
        # res_rating
        restaurant_header_element = driver.find_element_by_class_name("""biz-page-header""")
        data_html = restaurant_header_element.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(data_html, 'html5lib')
        restaurant_rating_tag = soup.find('div', attrs={'class': "i-stars"}).attrs
        restaurant_rating = restaurant_rating_tag['title']
    except:
        restaurant_rating = None

    try:
        # res_price
        restaurant_header_element = driver.find_element_by_class_name("""biz-page-header""")
        data_html = restaurant_header_element.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(data_html, 'html5lib')
        restaurant_price_element = soup.find('span', attrs={'class': "business-attribute"})
        restaurant_price = restaurant_price_element.text
    except:
        restaurant_price = None

    try:
        # res_tag
        restaurant_header_element = driver.find_element_by_class_name("""biz-page-header""")
        data_html = restaurant_header_element.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(data_html, 'html5lib')
        restaurant_tag_element = soup.find('span', attrs={'class': "category-str-list"})
        restaurant_tag = restaurant_tag_element.text.split()
        restaurant_tag = ', '.join(restaurant_tag)
    except:
        restaurant_tag = None

    li = [restaurant_name, restaurant_rating, restaurant_price, restaurant_tag]
    return li


def extract_reviews_df(driver):
    name_li = []
    rating_li = []
    text_li = []
    user_id_li = []

    reviews_table_element = driver.find_element_by_class_name("review-list")
    data_html = reviews_table_element.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(data_html, 'html5lib')
    reviews_table = soup.find('ul')

    # user_name
    name_tag = reviews_table.find_all('a', attrs={'class': 'user-display-name js-analytics-click'})
    for i in range(len(name_tag)):
        name = name_tag[i].text
        name_li.append(name)

    # user_id
    for i in range(len(name_tag)):
        user_id = name_tag[i].attrs['data-hovercard-id']
        user_id_li.append(user_id)

    # user_rating
    reviews_tag = reviews_table.find_all('div', attrs={"class": 'review-content'})
    for i in range(len(reviews_tag)):
        review_rating_tag = reviews_tag[i].find('div', attrs={'class': 'i-stars'}).attrs
        review_rating = review_rating_tag['title']
        rating_li.append(review_rating)
    # user_text
    for i in range(len(reviews_tag)):
        review_text_tag = reviews_tag[i].find('p')
        review_text = review_text_tag.text
        text_li.append(review_text)

    df = pd.DataFrame(
        data={'user_name': name_li, 'user_id': user_id_li, 'user_rating': rating_li, 'user_text': text_li})
    return df

def detect_ad_no(driver):
    try:
        data_element = driver.find_element_by_xpath("""//*[@id="super-container"]/div/div[2]/div[1]/div/div[5]/ul[2]""")
        data_html = data_element.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(data_html,'html5lib')
        ad_list = soup.find_all('li', attrs={'class': 'js-yloca js-yloca-search yloca-search-result', "data-ad-placement":"above_search"})
        ad_no = len(ad_list)
    except:
        ad_no = 0
    return ad_no

def one_business_extract(driver):
    res_li = []
    res_li = extract_restaurant_li(driver)
    reviews_df = None
    reviews_df = extract_reviews_df(driver)
    count = 1
    for i in range(48):
        try:
            next_button = driver.find_element_by_link_text("""Next""")
            next_button.click()
            reviews_df_more = extract_reviews_df(driver)
            reviews_df = pd.concat([reviews_df, reviews_df_more], axis=0, names=None, ignore_index = True)
            normal_delay = random.normalvariate(2, 0.5)
            time.sleep(normal_delay)
            count += 1
        except:
            pass
    reviews_df['restaurant_name'] = res_li[0]
    reviews_df['restaurant_rating'] = res_li[1]
    reviews_df['restaurant_price'] = res_li[2]
    reviews_df['restaurant_type'] = res_li[3]
    file_name = str(res_li[0])+('.csv')
    df = reviews_df
    df.to_csv(file_name)
    if count == 49:
        if res_li[0] not in error_li:
            error_li.append(res_li[0])
            print('Pages out of range {}'.format(res_li[0]))
    back_page_no = "window.history.go({})".format(str(-count))
    driver.execute_script(back_page_no)
    return driver


def select_back_all_re(driver):
    global reviews_df, count, error_li, ad_no, res_li

    restaurant_xpath_li = []
    for i in range(50):
        for i in range(10):
            ad_no = None
            ad_no = detect_ad_no(driver)
            no = str(i + 1 + ad_no)
            re_xpath = """//*[@id="super-container"]/div/div[2]/div[1]/div/div[5]/ul[2]/li[{}]/div/div[1]/div[1]/div/div[2]/h3/span/a"""
            re_xpath = re_xpath.format(no)
            restaurant_xpath_li.append(re_xpath)

        for i in range(len(restaurant_xpath_li)):
            res_li = None
            reviews_df = None
            select_business = driver.find_element_by_xpath(restaurant_xpath_li[i])
            click_business = select_business.click()

            normal_delay = random.normalvariate(5, 0.5)
            time.sleep(normal_delay)
            driver = one_business_extract(driver)

        next_button = driver.find_element_by_link_text("""Next""")
        next_button.click()
    driver.close()
    return driver


def fix_error(error_li):
    global reviews_df, res_li
    for error_restaurant in error_li:
        driver = open_website('https://www.yelp.com/')
        res_li = []
        driver = select_location_business(driver, '07030', error_restaurant)
        ad_no = detect_ad_no(driver)
        no = str(1 + ad_no)
        re_xpath = """//*[@id="super-container"]/div/div[2]/div[1]/div/div[5]/ul[2]/li[{}]/div/div[1]/div[1]/div/div[2]/h3/span/a"""
        re_xpath = re_xpath.format(no)
        normal_delay = random.normalvariate(2, 0.5)
        time.sleep(normal_delay)
        select_business = driver.find_element_by_xpath(re_xpath)
        select_business.click()

        res_li = extract_restaurant_li(driver)
        reviews_df = None
        reviews_df = extract_reviews_df(driver)
        count = 1
        for i in range(222):
            try:
                next_button = driver.find_element_by_link_text("""Next""")
                next_button.click()
                reviews_df_more = extract_reviews_df(driver)
                reviews_df = pd.concat([reviews_df, reviews_df_more], axis=0, names=None, ignore_index=True)
                normal_delay = random.normalvariate(2, 0.5)
                time.sleep(normal_delay)
                count += 1
            except:
                pass
        res_li = extract_restaurant_li(driver)
        reviews_df['restaurant_name'] = res_li[0]
        reviews_df['restaurant_rating'] = res_li[1]
        reviews_df['restaurant_price'] = res_li[2]
        reviews_df['restaurant_type'] = res_li[3]
        file_name = str(res_li[0]) + ('.csv')
        df = reviews_df
        df.to_csv(file_name)
        normal_delay = random.normalvariate(2, 0.5)
        time.sleep(normal_delay)
        driver.close()
    return None

def concat_dataset():
    path = "/Users/mani/Desktop/Dropbox/001 - Campus courses/BIA 660 - Web Analytics/Final Project/BIA660D_Group_1_Project/data_gathering"
    files= os.listdir(path)
    df = pd.read_csv("Grand Vin.csv")
    for file in files:
        if file.endswith('csv') and file != "restaurant_id.csv" and file != "Grand Vin.csv":
            df_new = pd.read_csv(file)
            df = pd.concat([df, df_new], axis=0, names=None, ignore_index = True)
    df.to_csv('Hoboken_restaurants_reviews.csv')

def main():
    driver = open_website('https://www.yelp.com/')
    driver = select_location_business(driver, '07030', 'Restaurant')
    driver = select_back_all_re(driver)
    fix_error(error_li)
    concat_dataset()

if __name__ == '__main__':
    main()