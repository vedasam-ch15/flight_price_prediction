# -*- coding: utf-8 -*-
"""PRML_bonus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fcqGP3NfxdLhVdONmCORac5_zqtkLBWn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv('/content/drive/MyDrive/Pattern Recognition and Machine Learning - 2022 Winter Semester/labs/bonus/data.csv')
data.head()

data.info()

data.dropna(inplace = True)
data.info()

data[data.duplicated()]

data.drop_duplicates(keep = 'first',inplace = True)

data[data.duplicated()]

data['Journey']=data['Source']+"_"+data['Destination']
data['Distance']=data['Journey'].map({'Banglore_Delhi':2158, 'Kolkata_Banglore':1544, 'Delhi_Cochin':2046,
       'Chennai_Kolkata':1678, 'Mumbai_Hyderabad':710})

X = data.iloc[:,:-1]
y = data['Price']
X.head()

y.head()

X['Duration'] = X['Duration'].astype(str).str.replace("h", '*60').str.replace(' ','+').str.replace('m','*1').apply(eval)

X["Journey_day"] = X['Date_of_Journey'].str.split('/').str[0].astype(int)
X["Journey_month"] = X['Date_of_Journey'].str.split('/').str[1].astype(int)
X.drop(["Date_of_Journey"], axis = 1, inplace = True)

X["Dep_hour"] = pd.to_datetime(X["Dep_Time"]).dt.hour
X["Dep_min"] = pd.to_datetime(X["Dep_Time"]).dt.minute
X.drop(["Dep_Time"], axis = 1, inplace = True)

X["Arrival_hour"] = pd.to_datetime(X.Arrival_Time).dt.hour
X["Arrival_min"] = pd.to_datetime(X.Arrival_Time).dt.minute
X.drop(["Arrival_Time"], axis = 1, inplace = True)

X.head()

X.info()

data.info()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
en = ['Airline','Source','Destination','Journey','Route','Total_Stops','Additional_Info']
for col in en:
  X[col] = le.fit_transform(X[col])

X.head()

"""# **EDA**

comparision of different airlines
"""

x=data.groupby('Airline')['Price'].mean().sort_values()
plt.bar(x.index,x)
plt.title('comparision of prices of different airlines')

plt.xticks(rotation=90)
plt.ylabel('price')

sns.catplot(y = "Price", x = "Airline", data = data.sort_values("Price", ascending = False), height = 5, aspect = 2)
plt.xticks(rotation=90)
plt.show()

"""price for different number of stops"""

sns.catplot(y = "Price", x = "Total_Stops", data = data.sort_values("Price", ascending = False), height = 5, aspect = 2)
plt.xticks(rotation=90)
plt.title('price for different number of stops')
plt.show()

"""prices for different sources"""

sns.catplot(y = "Price", x = "Source", data = data.sort_values("Price", ascending = False), height = 5, aspect = 2)
plt.xticks(rotation=90)
plt.show()

"""price for different destinations"""

sns.catplot(y = "Price", x = "Destination", data = data.sort_values("Price", ascending = False), height = 5, aspect = 2)
plt.xticks(rotation=90)
plt.show()

"""prices for different distances"""

plt.scatter(data['Distance'],data['Price'])
plt.xlabel('Duration')
plt.ylabel('Price')

"""price depending on the month"""

X['Journey_month'].nunique()

month_price=X.groupby('Journey_month')['Price'].mean()
plt.bar(month_price.index,month_price)

X_new = X.copy()
X_new['Price'] = data['Price']
data2 = X_new

sns.catplot(y = "Price", x = "Journey_month", data = data2.sort_values("Price", ascending = False), height = 4, aspect = 2)
plt.xticks(rotation=90)
plt.show()

"""price depending on the day"""

plt.scatter(X['Journey_day'],data['Price'])
plt.xlabel('Date of the month')
plt.ylabel('Price')

sns.catplot(y = "Price", x = "Journey_day", data = data2.sort_values("Price", ascending = False), height = 4, aspect = 2)
plt.xticks(rotation=90)
plt.show()

"""heatmap"""

corr = X.corr()
import matplotlib.pyplot as plot
plt.figure(figsize=(12,9))
sns.heatmap(corr, annot=True, square=True)
plt.yticks(rotation=0)
plt.show()

"""feature selction"""

import pandas as pd
import numpy as np


from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt
model = ExtraTreesRegressor()
model.fit(X,y)
print(model.feature_importances_) #use inbuilt class feature_importances of tree based classifiers
#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()

"""# **Random Forest Regressor**"""

X.head()
X.drop(['Price'], axis = 1, inplace = True)
X.head()

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
paramgrid = {'max_depth': list(range(2, 15, 2)), 'n_estimators': list(range(1, 250, 25))}
grid_search=GridSearchCV(RandomForestRegressor(random_state=2002),paramgrid)
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =0.25, random_state=2002)
 
grid_search.fit(X_train,y_train)

grid_search.best_estimator_

clf = RandomForestRegressor(max_depth = 12, n_estimators = 226, random_state = 2002)
clf.fit(X_train, y_train)
from sklearn.metrics import r2_score
y_pred = clf.predict(X_test)
r1 = r2_score(y_test, y_pred)
r1

"""# **XGB Regressor**"""

import warnings
warnings.filterwarnings("ignore")

from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
paramgrid = {'max_depth': list(range(2, 15, 2)), 'n_estimators': list(range(1, 250, 25))}
grid_search=GridSearchCV(XGBRegressor(random_state=2002),paramgrid)

 
grid_search.fit(X_train,y_train)

grid_search.best_estimator_

clf = XGBRegressor(max_depth = 6, n_estimators = 226, random_state = 2002)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
r2 = r2_score(y_pred, y_test)
r2

"""# **DECISION TREE REGRESSOR**"""

from sklearn.tree import DecisionTreeRegressor
paramgrid = {'max_depth': list(range(2, 15, 2)),'min_samples_split': [2,4,7,10]}
grid_search=GridSearchCV(DecisionTreeRegressor(random_state=2002),paramgrid)
grid_search.fit(X_train,y_train)
grid_search.best_estimator_

clf = DecisionTreeRegressor(max_depth  =14, min_samples_split = 10)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
r3 = r2_score(y_test, y_pred)
r3

"""SSFS FOR THE BEST MODEL: XGBOOST"""

import joblib
import sys
sys.modules['sklearn.externals.joblib'] = joblib
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
clf = XGBRegressor(max_depth = 6, n_estimators = 226, random_state = 2002)
sfs = SFS(clf,k_features = 10,forward = True, floating = True, verbose = 2, scoring = 'r2', cv = 4)
sfs = sfs.fit(X_train.values, y_train)

"""comparision of r2 scores"""

y = [0.895]
y2 = [0.91]
x = ['XGBoost']

plt.plot(x,y, marker = 'o')
plt.scatter(x,y2, marker = '*',color = 'red', label = 'XGBoost with SFFS')
plt.legend(loc = 'best')
plt.ylim(0.8,1)