import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# CSVファイルを読み込み
hexaco_data = pd.read_csv('csv/cul_24pp.csv')  # HEXACO回答データ
attributes_data = pd.read_csv('csv/hexaco_status.csv')  # 属性データ

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
# 全体の平均値も計算して追加
mean_overall = merged_data_numeric.mean(numeric_only=True).add_suffix('_mean').to_frame().T
mean_overall.index = ['全体']
mean_values = pd.concat([mean_values, mean_overall])
mean_values.to_csv('csv/status_mean.csv', index=True)
print(mean_values)

# 標準偏差の計算
std_values = pd.concat([merged_data_numeric.groupby(group).std(numeric_only=True).add_suffix('_std') for group in groups])
# 全体の標準偏差も計算して追加
std_overall = merged_data_numeric.std(numeric_only=True).add_suffix('_std').to_frame().T
std_overall.index = ['全体']
std_values = pd.concat([std_values, std_overall])
std_values.to_csv('csv/status_std.csv', index=True)
print(std_values)

# 中央値
# median_values = pd.concat([merged_data_numeric.groupby(group).median(numeric_only=True) for group in groups])
# median_values.to_csv('csv/status_median.csv', index=True)


# Cohen's dを計算する関数
def cohen_d(group1, group2):
    mean1, mean2 = group1.mean(), group2.mean()
    std1, std2 = group1.std(), group2.std()
    pooled_std = np.sqrt(((len(group1) - 1) * std1 ** 2 + (len(group2) - 1) * std2 ** 2) / (len(group1) + len(group2) - 2))
    return (mean1 - mean2) / pooled_std

# t検定を実行する関数
def perform_t_test(group1, group2):
    t_stat, p_value = ttest_ind(group1, group2, nan_policy='omit')
    return t_stat, p_value

# 男性と女性のグループを抽出
male_data = merged_data_numeric[merged_data_numeric['gender_group'] == '男性']
female_data = merged_data_numeric[merged_data_numeric['gender_group'] == '女性']

# 数値列（性格特性）のみを選択
hexaco_columns = merged_data_numeric.select_dtypes(include='number').columns

# 各性格特性ごとのCohen's dとt検定を計算
results = []
for col in hexaco_columns:
    cohen_d_value = cohen_d(male_data[col], female_data[col])
    t_stat, p_value = perform_t_test(male_data[col], female_data[col])
    results.append({
        'Feature': col,
        'Cohen\'s d': cohen_d_value,
        't-statistic': t_stat,
        'p-value': p_value
    })

# 結果をデータフレームに変換して表示
results_df = pd.DataFrame(results)
print(results_df)

# 結果をCSVファイルとして保存
results_df.to_csv('csv/cohens_d_gender.csv', index=False)

