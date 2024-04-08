import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing


data = pd.read_csv("csv/raw_studysapuri.csv")

data = data[data['category'] == 'all']

columns_to_drop = ["ID",'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism','category',
                   'NumberOfLecturesWatched', 'ViewingTime', 'NumberOfConfirmationTestsCompleted', 
                   'NumberOfConfirmationTestsMastered', 'AverageFirstAttemptCorrectAnswerRate']

x = data.drop(columns_to_drop, axis=1) 
x_columns = x.columns

# y = data[['NumberOfLecturesWatched']]
# y = data[['ViewingTime']]
y = data[['NumberOfConfirmationTestsCompleted']]
# y = data[['NumberOfConfirmationTestsMastered']]
# y = data[['AverageFirstAttemptCorrectAnswerRate']]

sscaler = preprocessing.StandardScaler()
sscaler.fit(x)
xss_sk = sscaler.transform(x) 
sscaler.fit(y)
yss_sk = sscaler.transform(y)

### regression
model = LinearRegression()
model.fit(xss_sk,yss_sk)
coefficient = model.coef_
df_coefficient = pd.DataFrame(coefficient, index=["coefficient"], columns=x_columns).T
df_coefficient = df_coefficient.sort_values(by='coefficient', ascending=False)
print(df_coefficient.to_string())
