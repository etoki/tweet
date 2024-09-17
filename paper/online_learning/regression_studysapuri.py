import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
# from sklearn.model_selection import train_test_split

data = pd.read_csv("csv/0723/raw_studysapuri.csv")
data = data[data['category'] == 'all']

columns_to_drop = ["ID",'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism','category',
                   'NumberOfLecturesWatched', 'ViewingTime', 'NumberOfConfirmationTestsCompleted', 
                   'NumberOfConfirmationTestsMastered', 'AverageFirstAttemptCorrectAnswerRate']

x = data.drop(columns_to_drop, axis=1) 
x_columns = x.columns

y = data[['NumberOfConfirmationTestsCompleted']]

sscaler = preprocessing.StandardScaler()
x_scaled = sscaler.fit_transform(x)
y_scaled = sscaler.fit_transform(y)

### regression
model = LinearRegression()
# x_train, x_test, y_train, y_test = train_test_split(x_scaled, y_scaled, test_size=0.2, random_state=42)
# model.fit(x_train, y_train)
model.fit(x_scaled,y_scaled)

coefficient = model.coef_
df_coefficient = pd.DataFrame(coefficient.T, index=x_columns, columns=["coefficient"])
df_coefficient = df_coefficient.sort_values(by='coefficient', ascending=False)
print(df_coefficient.to_string())
