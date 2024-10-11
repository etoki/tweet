import pandas as pd

# CSVファイルを読み込み
hexaco_data = pd.read_csv('csv/1101_hexaco_dev/cul_24pp.csv')  # HEXACO回答データ
attributes_data = pd.read_csv('csv/1101_hexaco_dev/hexaco_status.csv')  # 属性データ

# HEXACO回答データと属性データをメールアドレスで結合
merged_data = pd.merge(hexaco_data, attributes_data, on='メールアドレス')

# 数値列のみを抽出し、age列を除外
numeric_columns = merged_data.select_dtypes(include='number').drop(columns=['age'])  # ageを除外

# 数値列と属性データを再度結合（属性は文字列なのでそのまま）
merged_data_numeric = pd.concat([numeric_columns, merged_data[['gender', 'prefecture', 'area']]], axis=1)

# 特定のグループに基づくカテゴリーの追加（性別に「その他」と「回答しない」を考慮）
merged_data_numeric['gender_group'] = merged_data['gender'].replace({'男性': '男性', '女性': '女性', 'その他': 'その他'}).fillna('回答なし')

# 年代はそのまま使用
merged_data_numeric['age_group'] = merged_data['age'].astype(str) + '代'

# 地域（area）と都道府県（prefecture）ごとのグループ分け
merged_data_numeric['area_group'] = merged_data['area']
merged_data_numeric['prefecture_group'] = merged_data['prefecture']

# 各グループに対して平均値・中央値を計算
groups = ['gender_group', 'age_group', 'area_group', 'prefecture_group']

# 平均値の計算
mean_values = pd.concat([merged_data_numeric.groupby(group).mean(numeric_only=True) for group in groups])
mean_values.to_csv('csv/1101_hexaco_dev/final_mean_values.csv', index=True)
print(mean_values)

# 中央値の計算
median_values = pd.concat([merged_data_numeric.groupby(group).median(numeric_only=True) for group in groups])
median_values.to_csv('csv/1101_hexaco_dev/final_median_values.csv', index=True)
print(median_values)