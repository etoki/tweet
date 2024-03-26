from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing


data = pd.read_csv("csv/reg0326.csv")
# pprint(data)

# 基本統計量
# pprint(data.loc[:, "chat"])
# pprint(data.loc[:, "chat"].max())
# pprint(data.describe())

# 説明変数が1つ
# x = data[['pv_total']] 
# y = data[['reaction']]

# 説明変数xが複数
columns_to_drop = ["id","status","plan","scale","login_status","inbound","taishu_tenpyo","reaction"]
x = data.drop(columns_to_drop, axis=1) 
x_columns = x.columns
# print(x_columns)
y = data[['reaction']]

### 標準化による正規化
sscaler = preprocessing.StandardScaler()
sscaler.fit(x)
xss_sk = sscaler.transform(x) 
sscaler.fit(y)
yss_sk = sscaler.transform(y)
# print(xss_sk)
# print(yss_sk)

# xss_pd = (x - x.mean()) / x.std() # 不偏分散
# yss_pd = (y - y.mean()) / y.std() # 不偏分散
# xss_pd = (x - x.mean()) / x.std(ddof=0) # 普通の分散、不偏分散ではない
# yss_pd = (y - y.mean()) / y.std(ddof=0) # 普通の分散、不偏分散ではない
# print(xss_pd.head())
# print(yss_pd.head())
# print(xss_pd.mean())
# print(yss_pd.mean())
# print(xss_pd.std(ddof=0))
# print(yss_pd.std(ddof=0))



### 回帰分析
# model = LinearRegression()
# model.fit(x,y)
# plt.plot(x,y,'o')
# plt.plot(x,model.predict(x))

# 標準化した場合の回帰分析
model = LinearRegression()
model.fit(xss_sk,yss_sk)
# plt.plot(xss_sk,yss_sk,'o')
# plt.plot(xss_sk,model.predict(xss_sk))
# plt.show()

coefficient = model.coef_
df_coefficient = pd.DataFrame(coefficient, index=["係数"], columns=x_columns).T
df_coefficient = df_coefficient.sort_values(by='係数', ascending=False)
print(df_coefficient.to_string())

# print('a = ', model.coef_)
# print('b = ', model.intercept_)
# print('決定係数 = ',model.score(x, y))
