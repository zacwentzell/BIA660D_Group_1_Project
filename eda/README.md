# EDA Folder 

**Contributers**: Alec Kulakowski, 

Folder and File Info 
--------------------

### Files

**README.md**: This file! Information related to the folder and its files. 

**review_eda.ipynb**: Script to perform some exploratory data analysis on the 
reviews downloaded from the [Yelp Open Dataset](https://www.yelp.com/dataset).

**hoboken_reformat.py**: Remove superfluous data columns (may help to prevent
overfitting) and convert restaurant ratings into the ratings the restaurants
would have had before the customer placed his ratings (although the scraping
didn't include time/date of review, so this was done naively, but it is 
unlikely that this fact will lead to overfitting, although it may make it
harder to predict in real applications).