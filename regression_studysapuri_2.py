import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# CSVファイルの読み込み
data = pd.read_csv("csv/0723/raw_studysapuri.csv")

# 分析するカテゴリ
categories = ['all', 'ja', 'mt', 'en', 'sc']

# 不要なカラム
columns_to_drop = ["ID", 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism', 'category',
                   'IntellectualCuriosity', 'AestheticSensitivity', 'CreativeImagination', 
                #    'Organization', 'Productiveness', 'Responsibility', 
                   'Organization', 'Responsibility', 
                   'Sociability', 'Assertiveness', 'EnergyLevel', 
                   'Compassion', 'Respectfulness', 'Trust', 
                   'Anxiety', 'Depression', 'EmotionalVolatility',
                   'NumberOfLecturesWatched', 'ViewingTime', 'NumberOfConfirmationTestsCompleted', 
                   'NumberOfConfirmationTestsMastered', 'AverageFirstAttemptCorrectAnswerRate']

# 結果を保存するDataFrameの準備
all_results = pd.DataFrame()

# 各カテゴリに対して分析を行う
for category in categories:
    df = data[data['category'] == category]
    x = df.drop(columns_to_drop, axis=1)
    y = df[['NumberOfConfirmationTestsCompleted']]

    # 特徴量の標準化
    sscaler = preprocessing.StandardScaler()
    x_scaled = sscaler.fit_transform(x)
    y_scaled = sscaler.fit_transform(y)

    # 訓練データとテストデータに分割
    x_train, x_test, y_train, y_test = train_test_split(x_scaled, y_scaled, test_size=0.3, random_state=42)

    # 線形回帰モデルの学習
    model = LinearRegression()
    model.fit(x_train, y_train)

    # テストデータで予測
    y_pred = model.predict(x_test)

    # 評価指標の計算
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r_squared = r2_score(y_test, y_pred)
    n = len(y_test)  # サンプルサイズ
    p = x_test.shape[1]  # 特徴量の数
    adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)

    # 係数を保存
    coefficients = pd.Series(model.coef_.flatten(), index=x.columns, name=category)
    intercept = pd.Series([model.intercept_[0]], index=['Intercept'], name=category)
    metrics = pd.Series({
        "MSE": mse,
        "RMSE": rmse,
        "MAE": mae,
        "R-squared": r_squared,
        "Adjusted R-squared": adjusted_r_squared
    }, name=category)

    # 結果をDataFrameに追加
    all_results = pd.concat([all_results, pd.concat([metrics, intercept, coefficients])], axis=1)

# 結果をCSVファイルに出力
all_results.to_csv("csv/0723/regression_studysapuri.csv")

# 結果を表示
print(all_results)
