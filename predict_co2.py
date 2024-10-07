import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import cross_val_score
import numpy as np

# データの読み込み (CSVファイルを想定)
data = pd.read_csv('csv/train_co2.csv')  # 学習用データ
predict_data = pd.read_csv('csv/predict_co2.csv')  # 予測用データ

# 説明変数と目的変数に分ける
X = data[['floors', 'total_floor', 'structure', 'main_use']]  # 説明変数
y = data['emissions']  # 目的変数

# カテゴリ変数の処理
categorical_features = ['structure', 'main_use']
numerical_features = ['floors', 'total_floor']

# 前処理 (カテゴリ変数のOneHotエンコーディング)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# ランダムフォレストモデルの構築
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

# 学習データを訓練セットとテストセットに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデルの学習
model.fit(X_train, y_train)

# 1. 決定係数 (R²スコア)
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"決定係数 (R²): {r2}")

# 2. 平均絶対誤差 (MAE)
mae = mean_absolute_error(y_test, y_pred)
print(f"平均絶対誤差 (MAE): {mae}")

# 3. 平均二乗誤差 (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f"平均二乗誤差 (MSE): {mse}")

# 5. 交差検証 (Cross Validation)
cross_val_scores = cross_val_score(model, X, y, cv=5, scoring='r2')  # 5分割の交差検証
print(f"交差検証 R²スコア: {cross_val_scores.mean()} ± {cross_val_scores.std()}")

# 7. 特徴量の重要度の計算と出力
# モデル内のランダムフォレストから特徴量の重要度を取得
feature_importances = model.named_steps['regressor'].feature_importances_

# カテゴリ変数のエンコード後の新しい特徴量名を取得
encoded_features = model.named_steps['preprocessor'].transformers_[1][1].get_feature_names_out(categorical_features)
all_features = numerical_features + list(encoded_features)

# 特徴量の重要度を表示
importance_df = pd.DataFrame({'特徴量': all_features, '重要度': feature_importances})
importance_df = importance_df.sort_values(by='重要度', ascending=False)
print("特徴量の重要度:")
print(importance_df)

# 予測データに対する予測
predictions = model.predict(predict_data)
predict_data['pre_emissions'] = predictions

# 予測結果をCSVとして保存
predict_data.to_csv('csv/predict_co2_res.csv', index=False)

# 予測結果の表示
print(predict_data)
