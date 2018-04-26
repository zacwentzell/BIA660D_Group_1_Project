import requests
from bs4 import BeautifulSoup as bs
import urllib3
import time
import random
from string import digits
import pandas as pd
url_base='https://www.yelp.com/search?find_desc=Restaurants&find_loc=Hoboken%2C+NJ&start='
remove_digits=str.maketrans('','',digits)
res_name_list=[]
res_number=0
while res_number <= 680:
    final_url=url_base+str(res_number)
    res=requests.get(final_url)
    soup=bs(res.text,"html5lib")
    solo_res = soup.find_all('div',{'class':'search-result natural-search-result'})
    res_name=soup.find_all('span',{'class':'indexed-biz-name'})
    for x in range(len(res_name)):
        res_name_list.append(res_name[x].text.replace('.','').translate (remove_digits).strip())
    time.sleep(random.randint(2,4))
    res_number+=10
    name_df = pd.DataFrame(res_name_list)