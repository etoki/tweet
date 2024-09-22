import pandas as pd
import scipy.stats as stats

# CSVファイルの読み込み
file_path = 'csv/hexaco_domain.csv'
# file_path = 'csv/hexaco_facet.csv'
df = pd.read_csv(file_path)

# 統計量を計算する関数
def calculate_statistics(df):
    statistics = pd.DataFrame()

    # 各列に対して統計量を計算
    statistics['サンプル数'] = df.count()
    statistics['最小値'] = df.min()
    statistics['最大値'] = df.max()
    statistics['平均'] = df.mean()
    statistics['標準偏差'] = df.std()
    statistics['中央値'] = df.median()
    statistics['分散'] = df.var()
    statistics['歪度'] = df.apply(lambda x: stats.skew(x))
    statistics['尖度'] = df.apply(lambda x: stats.kurtosis(x))

    return statistics

# 統計量の計算
statistics_df = calculate_statistics(df)

# 結果を表示
print(statistics_df)

# CSVファイルに保存
statistics_df.to_csv('csv/hexaco_statistics_output_domain.csv', encoding='utf-8-sig')

