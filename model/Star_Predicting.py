from sklearn.model_selection import train_test_split
import pandas as pd
import time
import lightgbm as lgb
import os
import psutil
import gc
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV

def cpuStats():
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0] / 2. ** 30
    print('memory GB:', memoryUse)




tm = time.time()
print('Loading train.csv...')

df = pd.read_csv('../input/Data_fulll.csv')


print('Preprocessing...')




df.date = pd.to_datetime(df.date)
df.drop(['text','address'],inplace=True,axis=1)
df.dropna(axis=0,inplace= True)

tmp = df[['business_id','city','Restaurant_Star']].drop_duplicates()


print('Adding Restaurant_Number....')
gp = tmp.groupby(['city'])['business_id'].count().reset_index().rename(index=str, columns={'business_id':'Restaurant_Number' })
df = df.merge(gp,on = 'city')
del gp

print('Adding City_Mean_Star....')
gp = tmp.groupby(['city'])['Restaurant_Star'].mean().reset_index().rename(index=str, columns={'Restaurant_Star':'City_Mean_Star' })
df = df.merge(gp,on = 'city')


del gp
del tmp
gc.collect()

cpuStats()

df['Month'] = df['date'].dt.month
df['WDay'] = df['date'].dt.dayofweek

print('Adding Num_of_Reviews_User_Made....')
tmp = df.groupby('user_id')['business_id'].count().reset_index(). \
rename(index=str, columns={'business_id':'Num_of_Reviews_User_Made'})

df = df.merge(tmp,on='user_id')

del tmp
gc.collect()
print('Adding Num_of_Useful_User_Get....')
tmp = df.groupby('user_id')['useful'].sum().reset_index(). \
rename(index=str, columns={'useful':'Num_of_Useful_User_Get'})

df = df.merge(tmp,on='user_id')

del tmp
gc.collect()
print('Adding Num_of_Cool_User_Get....')
tmp = df.groupby('user_id')['cool'].sum().reset_index(). \
rename(index=str, columns={'cool':'Num_of_Cool_User_Get'})

df = df.merge(tmp,on='user_id')

del tmp
gc.collect()
print('Adding Num_of_Funny_User_Get....')
tmp = df.groupby('user_id')['funny'].sum().reset_index(). \
rename(index=str, columns={'funny':'Num_of_Funny_User_Get'})

df = df.merge(tmp,on='user_id')

del tmp
gc.collect()
print('Adding User_Mean_Star....')
tmp = df.groupby('user_id')['Review_Star'].mean().reset_index(). \
rename(index=str, columns={'Review_Star':'User_Mean_Star'})

df = df.merge(tmp,on='user_id')

del tmp
gc.collect()

df.drop(['business_id','user_id','name','funny','useful','cool','date'],axis=1,inplace=True)

le = preprocessing.LabelEncoder()
le.fit(df.city)
df.city = le.transform(df.city)


print(df.head())


y = df.Review_Star.values

gc.collect()

target = 'Review_Star'
df.drop('Review_Star',inplace =True,axis=1)

inputs = list(set(df.columns) - set([target]))
cat_vars = ['city']

train_df, val_df = train_test_split(df, train_size=.80, shuffle=False)
y_train, y_val = train_test_split(y, train_size=.80, shuffle=False)

print('Train size:', len(train_df))
print('Valid size:', len(val_df))
print('Train y size:', len(y_train))
print('Valid y size:', len(y_val))

gc.collect()

print('Training...')
cpuStats()
rf = RandomForestClassifier(n_estimators=800,max_depth=8).fit(train_df, y_train)
y_val_1 = rf.predict(val_df)

print("Random Forest Validation accuracy: ", sum(y_val_1 == y_val) / len(y_val))
# print('Tuning...')
# rf = RandomForestClassifier()
# param_grid = {
#     'n_estimators': [200,800],
#     # 'max_features': ['auto', 'sqrt', 'log2'],
#     'max_depth' : [4,8],
#     # 'criterion' :['gini', 'entropy']
# }
#
# clf = GridSearchCV(rf, param_grid,cv=5)
# clf.fit(df, y)
# print (clf.best_params_)
print('Time used',time.time()-tm,'s')