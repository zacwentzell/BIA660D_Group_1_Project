# BIA660D_Group_1_Project
The class project for Group 1 of BIA 660D, Spring 2018.

**Project Goal**: Create an enhanced rating prediction system based on review text and associated metadata.

**Project Members**: Alec Kulakowski, He Li, Ni Man, Richard Roma, Xin Lin

Project Narrative 
-----------------
We sourced the bulk of our dataset (used for training/test/cross-validation) from the 
[Yelp Open Dataset](https://www.yelp.com/dataset). The remaining data we 
manually scraped from a targeted Yelp search. We focused on Hoboken data, 
and scraped every review for every restaurant in Hoboken, NJ (this was
to be our validation dataset, to judge our model's overall accuracy on).

##### Dataset Processing

The Yelp Open Dataset was manually downloaded from their website, extracted (first from 
.tar, then from .rar), and converted (files within it were .json and we wanted .csv's) 
using json_to_csv from [Yelp's Github](https://github.com/Yelp/dataset-examples). 
We also had to clean the data from the scraping (there were errors in the scraped data 
due to special cases in the underlying webpages) and match its formatting to the data 
provided by Yelp. 

Folder and File Info 
--------------------

### Folders

**scraping**: Files for scraping, storing, and cleaning the Hoboken review data 
(validation dataset) off of the web. 

**yelp_dataset**: Files for formatting and storing the data provided in the Yelp
Open Dataset. Subfolders here are included in .gitignore. 

**eda**: Files for preprocessing data and transforming 

### Files

**README.md**: This file! Information related to the project and the repository. 

**.gitignore**: A plain text list of files to ignore and not upload to the Github
repository. Important since some of the files we're dealing with contain many 
millions of entries and as a result may be multiple GB in size. The remote Github 
repository can't handle files of this size, so they must be stored on each group 
member's local repository. 

Notes 
-----
**RE: *Recommendation System/Hoboken_restaurants_reviews_cleaned.csv***: Does not
vectorize or even properly clean the 'Restaurant Type' data, does not deal with 
missing values for restaurant price. 

**Known Issues**: Scraped review data has no evaluations of 'Useful', 'Funny', 
or 'Cool'.

Just let you guys know Recommendation System/Hoboken_restaurants_reviews_cleaned.csv only works for recommendation system part(done two weeks ago). If you really need the vectorized data, there is a normalized one for Neural Network algorithms, which is on path - Recommendation System/Method_4_Deep_Learning(done last week). But I still think all of us should do data preprocessing for different objectives. There is not a perfect dataset for different tasks. - Mani
