import pandas as pd
import numpy as np
import pingouin as pg

# CSVファイルのパス
# input_csv_path1  = '../../csv/hexaco_raw_webapp.csv'
input_csv_path1  = '../../csv/hexaco_raw_from_20240916.csv' # HEXACO-JP
input_csv_path2  = '../../csv/hexaco_raw_googleform.csv'
# output_csv_path1 = '../../csv/hexaco_domain.csv'
# output_csv_path2 = '../../csv/hexaco_facet.csv'
output_csv_path1 = '../../csv/hexaco-jp_domain.csv'
output_csv_path2 = '../../csv/hexaco-jp_facet.csv'


# 追加するカラム名
column_names = [
    'responseId', 'firstName', 'lastName', 'email', 
    'Honesty-Humility', 'Emotionality', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Openness', 
    'Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty', 
    'Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality', 
    'Social-Self-Esteem', 'Social-Boldness', 'Sociability', 'Liveliness', 
    'Forgiveness', 'Gentleness', 'Flexibility', 'Patience', 
    'Organization', 'Diligence', 'Perfectionism', 'Prudence', 
    'Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality', 
    'startTimestamp', 'endTimestamp', 'diff', 'completed', 'num'
]

# CSVファイルを読み込み
df_1 = pd.read_csv(input_csv_path1, header=None)
# df_2 = pd.read_csv(input_csv_path2)

# カラム名を追加
df_1.columns = column_names

# df_1: 削除するカラム名のリスト
columns_to_drop1 = ['responseId', 'firstName', 'lastName', 'startTimestamp', 'endTimestamp', 'diff', 'completed', 'num']
columns_to_drop2 = ['ID']

# 不要なカラムを削除
df_1.drop(columns=columns_to_drop1, inplace=True)
# df_2.drop(columns=columns_to_drop2, inplace=True)

df_1 = df_1[~df_1['email'].isin(['jay@amegumi.com', 'sub.ashuman@gmail.com'])]
# df_2 = df_2[~df_2['email'].isin(['jay@amegumi.com', 'sub.ashuman@gmail.com'])]

# df = pd.concat([df_1, df_2], ignore_index=True)
df = df_1 # 2つのデータを連結しない場合
df.drop(columns="email", inplace=True)

# 数値以外のデータを NaN に変換する（もし存在する場合）
df.replace('\\N', np.nan, inplace=True)

# 数値に変換できないデータが含まれていないか確認
df = df.apply(pd.to_numeric, errors='coerce')

# ドメインのカラム名のリスト
domain_columns = [
    'Honesty-Humility', 'Emotionality', 'Extraversion', 
    'Agreeableness', 'Conscientiousness', 'Openness'
]

# ファセットのカラム名のリスト
facet_columns = [
    'Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty',
    'Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality',
    'Social-Self-Esteem', 'Social-Boldness', 'Sociability', 'Liveliness',
    'Forgiveness', 'Gentleness', 'Flexibility', 'Patience',
    'Organization', 'Diligence', 'Perfectionism', 'Prudence',
    'Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality'
]

facet_h_columns = ['Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty']
facet_e_columns = ['Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality']
facet_x_columns = ['Social-Self-Esteem', 'Social-Boldness', 'Sociability', 'Liveliness']
facet_a_columns = ['Forgiveness', 'Gentleness', 'Flexibility', 'Patience']
facet_c_columns = ['Organization', 'Diligence', 'Perfectionism', 'Prudence']
facet_o_columns = ['Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality']

# ドメインのカラムを含む新しいDataFrameを作成
domain_df = df[domain_columns]

# ファセットのカラムを含む新しいDataFrameを作成
facet_df   = df[facet_columns] 
facet_h_df = df[facet_h_columns] # 0.65
facet_e_df = df[facet_e_columns] # 0.716
facet_x_df = df[facet_x_columns] # 0.777
facet_a_df = df[facet_a_columns] # 0.69
facet_c_df = df[facet_c_columns] # 0.729
facet_o_df = df[facet_o_columns] # 0.679

print(domain_df)
print(facet_df)

domain_df.to_csv(output_csv_path1, index=False)
facet_df.to_csv(output_csv_path2, index=False)
