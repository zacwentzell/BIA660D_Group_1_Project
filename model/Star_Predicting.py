#By Xin Lin
from sklearn.model_selection import train_test_split
import pandas as pd
import time

import os
import psutil
import gc
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import RandomForestRegressor

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse


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

features = list(train_df.columns)

gc.collect()

print(train_df.columns)
print('Training...')
cpuStats()
rf = RandomForestRegressor(n_estimators=800,max_depth=8,n_jobs=-1).fit(train_df, y_train)
rf_pre = rf.predict(val_df)
rf_mse = mse(rf_pre,y_val)
print('mse for randomforest:',rf_mse)
print ("Features sorted by their score:")
print (sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), features),
             reverse=True))

#
# svr = SVR().fit(train_df, y_train)
# svr_pre = svr.predict(val_df)
# svr_mse = mse(svr_pre,y_val)
# print('mse for svr:', svr_mse)
#
#
lr = LinearRegression(n_jobs=-1).fit(train_df,y_train)
lr_pre = lr.predict(val_df)
lr_mse = mse(lr_pre,y_val)
print('mse for linear regression:',lr_mse)

blend = (rf_pre + lr_pre)/2

blend_mse = mse(blend,y_val)
print('mse after blending:',blend_mse)

# importance = rf.feature_importances_
# importance = pd.DataFrame(importance, index=train_df.columns,
#                           columns=["Importance"])

# importance["Std"] = np.std([tree.feature_importances_
#                             for tree in rf.estimators_], axis=0)

# x = range(importance.shape[0])
# y = importance.ix[:, 0]
# yerr = importance.ix[:, 1]

# plt.bar(x, y, yerr=yerr, align="center")

# plt.show()

print('Tuning...')
rf = RandomForestClassifier()
param_grid = {
    'n_estimators': [200,800,1000],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,8,12],
    'criterion' :['gini', 'entropy']
}

clf = GridSearchCV(rf, param_grid,cv=5)
clf.fit(df, y)
print (clf.best_params_)
print('Time used',time.time()-tm,'s')