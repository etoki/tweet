import pandas as pd
from scipy.stats import spearmanr

# CSVファイルの読み込み
input_file_path_1 = 'csv/cul_24pp.csv'  # 1つ目のデータセット
input_file_path_2 = 'csv/cul_60w_ch_dm.csv'  # 2つ目のデータセット
output_file_path_1  = 'csv/domain_correlation_matrix.csv'
output_file_path_2  = 'csv/facet_correlation_matrix.csv'

# データセットの読み込み
data_24pp = pd.read_csv(input_file_path_1)
data_60_wakabayashi = pd.read_csv(input_file_path_2)

# ファセットの相関行列作成
# ファセットとドメインの列を選択
facet_columns = data_24pp.columns[7:]  # ファセットは7列目以降
domain_columns_60 = data_60_wakabayashi.columns[1:]  # 2つ目のデータセットのドメインは1列目以降

# 結果を初期化
correlation_results_facet = []

# 各ファセットとドメイン間の相関を計算
for domain in domain_columns_60:
    for facet in facet_columns:
        correlation_value, p_value = spearmanr(data_24pp[facet], data_60_wakabayashi[domain])
        correlation_results_facet.append([domain, facet, correlation_value, p_value])

# データフレームに変換
facet_results_df = pd.DataFrame(correlation_results_facet, columns=['domain', 'facet', 'correlation', 'p_value'])

# フォーマットを整える
facet_output_df = facet_results_df.pivot(index='facet', columns='domain', values=['correlation', 'p_value'])
facet_output_df = facet_output_df.reset_index()

# 結果をCSVファイルとして保存
facet_output_df.to_csv(output_file_path_2, index=False)
print(facet_output_df)


# ドメインの相関行列作成
# ドメイン列の選択
domain_data_24pp = data_24pp[['Honesty-Humility', 'Emotionality', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Openness']]
domain_data_60 = data_60_wakabayashi[['Honesty-Humility', 'Emotionality', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Openness']]

# 相関行列を計算するための結果を初期化
correlation_results_domain = pd.DataFrame(index=domain_data_24pp.columns, columns=domain_data_60.columns)
p_value_results_domain = pd.DataFrame(index=domain_data_24pp.columns, columns=domain_data_60.columns)  # p値用のデータフレームを初期化

# 各ドメインの相関を計算
for col_24 in domain_data_24pp.columns:
    for col_60 in domain_data_60.columns:
        correlation_value, p_value = spearmanr(domain_data_24pp[col_24], domain_data_60[col_60])
        correlation_results_domain.loc[col_24, col_60] = correlation_value
        p_value_results_domain.loc[col_24, col_60] = p_value  # p値を保存

# p値の表示精度を調整
p_value_results_domain = p_value_results_domain.applymap(lambda x: format(x, '.6g'))

# 結果をCSVファイルとして保存
correlation_results_domain.to_csv(output_file_path_1)
p_value_results_domain.to_csv('csv/domain_p_value_matrix.csv')  # p値のCSVファイルを保存

print(correlation_results_domain)
print(p_value_results_domain)