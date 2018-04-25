# BIA660D_Group_1_Project
The class project for Group 1 of BIA 660D, Spring 2018.

**Project Goal**: Create an enhanced rating prediction system based on review text and associated metadata.

**Project Members**: Alec Kulakowski, He Li, Ni Man, Richard Roma, Xin Lin

Project Narative 
-------
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