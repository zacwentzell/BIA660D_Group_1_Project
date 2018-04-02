
# coding: utf-8

# In[61]:


import requests
from bs4 import BeautifulSoup as bs
import urllib3
import time 
import random
from string import digits


# In[62]:


url_base='https://www.yelp.com/search?find_desc=Restaurants&find_loc=Hoboken%2C+NJ&start='


# In[63]:


url_base


# In[64]:


remove_digits=str.maketrans('','',digits)


# In[145]:


res_name_list=[]
res_number=0

while res_number <= 680:
    
    final_url=url_base+str(res_number)
    res=requests.get(final_url)
    soup=bs(res.text,"html5lib")
    solo_res = soup.find_all('div',{'class':'search-result natural-search-result'})
    for solo_ in solo_res:
        #check if the restaurant is in hoboken
        if 'Hoboken' in str(solo_.find('address')):  
            #add name of rest
            res_name=solo_.find_all('span',{'class':'indexed-biz-name'})    
            res_name_list.append(res_name[0].text.replace('.','').translate (remove_digits).strip())
    time.sleep(random.randint(2,4))
    res_number+=10


# In[146]:


res_name_list


# In[147]:


len(set(res_name_list))


# In[148]:


import pandas as pd


# In[149]:


name_df=pd.DataFrame(res_name_list)
name_df.to_csv(r'/Users/heli/Desktop/660-res.csv')


# In[158]:


temp=[i.lower().replace(' ','-') for i in res_name_list]


# In[159]:


temp1=[i.replace('&','and') for i in temp]


# In[160]:


res_final_name=[i.replace("’",'') for i in temp1]


# In[162]:


temp2=[i.replace('---','-') for i in res_final_name]


# In[165]:


temp3=[i.replace('-+-','-') for i in temp2]


# In[167]:


temp4=[i.replace('-@-','-') for i in temp3]


# In[183]:


temp5=[i.replace('--','-') for i in temp4]


# In[186]:


name_df


# In[203]:


res_price_list=[]
for i in range(len(temp5)):
    
     
    url_infor= 'https://www.yelp.com/biz/'+str(temp5[i])+'-hoboken'
    res=requests.get(url_infor)
    soup=bs(res.text,"html5lib")
    res_price=soup.find_all('span',{'class':'business-attribute price-range'})
    res_name=soup.find_all('span',{'class':'indexed-biz-name'})
#     for m in range(len(res_price)):
    try:
        res_price_list.append(res_price[0].text)
    except:
        print(temp5[i])

    time.sleep(random.randint(2,4))


# In[200]:


len(res_price_list)


# In[ ]:


price_df=pd.DataFrame(res_final_name,res_price_list)


# In[81]:


price_df.to_csv(r'/Users/heli/Desktop/660-price.csv')


# In[119]:


# price_df[::3]


# In[197]:


list=['a,b,c']

