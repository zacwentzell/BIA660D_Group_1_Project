"""
More EDA and feature selection
BIA660D - Group 1: Alec Kulakowski
"""
import pandas as pd
import numpy as np
data = pd.read_csv('../BIA660D_Group_1_Project/eda/hoboken_step1.csv')
data.head(2)
# Lets see what correlations we can draw and what new features we can create
### Feature Evaluation
"""
For missing restaurant ratings, we could substitute the median restaurant rating, as that is the
most likely value for it to have. A possible other solution would be to replace missing
restaurant ratings with a 0 or other number that's outside of the normal range (1-5) for the
variable. In nonlinear models (SVMs with a nonlinear kernel, neural nets with nonlinear activation 
functions, tree-based algorithms) this difference could be accounted for, but if interpreted linearly 
it would be misleading (the missing restaurant ratings are due to the fact that when I corrected for 
what the restaurant's rating would have been *before* the review happened, if the restaurant in 
question has only received that one review, it would have no rating before it. I confirmed this by
running: data.iloc[np.where(data['restaurant_rating'].isnull())] which showed that all the restaurants
with null ratings were restaurants that had only gotten the one review (I also double checked these
ratings on Yelp to confirm that these restaurants had only received one review). Thus, for now (for 
the EDA as well as when utilizing nonlinear solvers) we will replace these missing restaurant ratings 
with a rating of 0, but when testing linear solvers we shall replace them with the median score 
(hopefully I will remember). 
Dropping them would mean that we wouldn't be training the model to predict any ratings for restaurants
that haven't been rated before, which shouldn't be the case
"""
new_data = data.copy(deep=True)
data.iloc[[np.where(data['restaurant_rating'].isnull())], np.where(data.columns == 'restaurant_rating')[0][0]] = 0 #for EDA and nonlinear
new_data = new_data.drop(np.where(new_data['restaurant_rating'].isnull())[0])
#^just for EDA exploring the relationship of existing rating to the current review's rating
new_data['restaurant_rating'].isnull().sum() == 0
new_data['restaurant_rating'] = new_data['restaurant_rating'].apply(lambda x: round(x*2)/2) # rounding
# Lets look at a bar chart showing the variance present at various ratings
average_to_rating = new_data[['restaurant_rating', 'user_rating']] #obviously a correlation ofc # maybe just plot dispursion
# Relationship of restaurant cuisine type to rating?
type_to_ratings = pd.read_csv('../BIA660D_Group_1_Project/eda/type_data.csv')
type_to_ratings.sort_values(by='Average_Score', inplace=True)
# Relationship of review length to ratings?
data['review_len'] = data['user_text'].apply(len)
length_to_ratings = data[['review_len', 'user_rating']]
# Relationship of price to ratings?
price_to_ratings = data[['restaurant_price', 'user_rating']]
# Relationship of mispellings to ratings?
from autocorrect import spell #import re #?
from nltk import word_tokenize
import re, string
apostrophes = re.compile("'")
punctuation = re.compile('[%s]' % re.escape(string.punctuation))# all punctuation marks, but not escape characters i.e \n
multiple_spaces = re.compile(' +')
# Custom mispelling identifiers #nltk.download('brown'), etc.
#pyenchant spell checker doesn't work for non 2.x python on systems other than Linux
# from textblob import TextBlob #nope, errors like restauraunts -> restaurant and Grand Vin -> Grand In
from nltk.corpus import brown, gutenberg, reuters, masc_tagged, movie_reviews, treebank, \
    opinion_lexicon, product_reviews_2, pros_cons, subjectivity, sentence_polarity, words
# do not use: stopwords, conll2002, jeita, knbc, alpino, sinica_treebank, udhr, udhr2, these include non-english words
# had weird or foreign or slang terms, oomlouts, etc: wordnet, cmudict, genesis
corpuses = [brown, gutenberg, reuters, masc_tagged, movie_reviews, treebank, opinion_lexicon, product_reviews_2,
            pros_cons, subjectivity, sentence_polarity, words]
all_word_list = set() #best maybe: words,
for counter, corp in enumerate(corpuses, 1):
    print("Appending corpus #"+str(counter)+" of "+str(len(corpuses))+" to set of all words. ")
    all_word_list = all_word_list.union(set(map(lambda x: x.lower(), corp.words())))
### Check where the incorrect words are coming from, to remove that source from the corpuses
backup = all_word_list.copy()
# for counter, corp in enumerate(corpuses, 1):
#     if 'jafef' in map(lambda x: x.lower(), corp.words()):
#         print(counter, corp)#         break
len(all_word_list)
# brown_set =  set(map(lambda x: x.lower(), brown.words())) #these all take a few seconds
# gutenberg_set = set(map(lambda x: x.lower(), gutenberg.words()))
# reuters_set = set(map(lambda x: x.lower(), reuters.words()))
# import hunspell #nope
# help(hunspell)
# hobj = hunspell.hunspell('/usr/share/hunspell/en_US.dic')
# len(reuters_set) #31078
# len(reuters_set | brown_set | gutenberg_set)
# len(brown_set) #49815
# len(gutenberg_set) #42339
# #
def correctly_spelled(word):
    if all([letter.isdigit() for letter in word]):
        return( True )
    # result = (word.lower() == spell(word).lower()) #autocorrect version
    # result = (word in word_set) #brown corpus
    result = (word.lower() in all_word_list)
    if not result:
        result = (word.lower() == spell(word).lower()) #I think this one takes longest, so I did it in the 'if'
    return( result )
def strip_punct(text):
    text = apostrophes.sub('', text) # To prevent seperating "wouldn't" into "wouldn t"
    text = punctuation.sub(' ', text)
    return( multiple_spaces.sub(' ', text).strip() )
def correct_mispellings(text):
    text = strip_punct(text)
    sent = ""
    for word in word_tokenize(text):
        if any(character.isdigit() for character in word):
            sent = sent + " " + word
        else:
            sent = sent + " " + spell(word)
    return sent.strip()
def count_mispellings(text): #text = temp #for testing #takes ages for all words
    text = strip_punct(text)
    mispellings = 0
    for word in word_tokenize(text):
        if not correctly_spelled(word): #not any(character.isdigit() for character in word)
                # print("word: "+str(word)+", correct: "+str(spell(word))) #for diagnostic purposes
                mispellings += 1
    return mispellings
# ^ lol a simple concept but these took quite a while to code to make them robust # data_copy = data.copy(deep=True)
# count_mispellings(data['user_text'][2])
# i could do it by chunk?

len(data['user_text']) #74611
# data['user_text'] #[:15000] #[15000:30000] # [30000:45000] # [45000:60000] # [60000:]
# first_1500 = data['user_text'][:1500].apply(count_mispellings) #careful this takes ages #15 minutes this is taking  #86.25s
# second_1500 = data['user_text'][1500:3000].apply(count_mispellings)
# third_1500 = data['user_text'][3000:4500].apply(count_mispellings) #141s (i dont believe it, it took much longer than that
# fourth_1500 = data['user_text'][4500:6000].apply(count_mispellings)#pd.Series
# fifth_1500 = data['user_text'][6000:].apply(count_mispellings)  #wait its not 7400 in size its 74,000... will take much longer
import time #estimated time based on previous averages is roughly: 82.9 minutes, lets see how long it actually takes
start = time.time()
data['mispelling_count'] = data['user_text'].apply(count_mispellings) #careful this takes ages #started at 11:14 end at
end = time.time()
print("Process took "+str(end-start)+"s to finish") # 6092.65s =  101.5m
# count_series = pd.Series(name='mispelling_count')
# [first_1500, second_1500, third_1500, fourth_1500, fifth_1500]
# data['user_text'][1498:1502]
# count_series[1498:1502]

mispelling_to_ratings = data[['mispelling_count', 'user_rating']]

data.head(2)
# data['mispelling_count']
# text = data['user_text'][23] #for testing
# Save data so we don't have to calculate mispellings, review_len, etc. again (can always remove easily, but takes
# time and effort to create from scratch. Thus we save it below \/
data.to_csv('../BIA660D_Group_1_Project/eda/hoboken_step2.csv', index = False) #yay!
# data.drop(columns=[data.columns[0]], inplace=True)
# data.head(3)
#
"""
Some thoughts: maybe I should have kept in the user names for each reviewer so I could count all reviews they left in 
Hoboken and use that as an independent variable, BUT: upon further inspection this wouldn't really work as it 
would be quite an arbitrary variable, "number of total reviews" for a reviewer *would* work, but to be robust and 
avoid possible bias (not to mention the problems associated with small/sparse/incomplete data) it would have to 
include number of reviews for that user ovearall, not just in Hoboken. Since our scraping didn't pick this up, I can't
incorporate it, thus it's fine to keep leaving out the usernames. 
As an afterthought one may think that counting the number of reviews a given user leaves on the same restaurant would 
be helpful, and indeed it would (you probably wouldn't go back to the same place unless you thought it was decent), 
but I believe that Yelp replaces past reviews with the most recent one, so scraping shouldn't be able to find multiple
reviews for each user on the restaurant or even a review count. A possible workaround would be number of Yelp
"check-ins" the user had at that specific restaurant, but this data (while available on the Yelp page that was scraped)
was not scraped in our scraping process (although it is in the Yelp Open Dataset, which ultimately couldn't be used for
the predicting due to issues involving the size of the dataset). 
"""


# correct_mispellings(data['user_text'][0])
# data['user_text'][0]
data.head(2)







