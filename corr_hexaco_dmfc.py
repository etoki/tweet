import pandas as pd
import scipy.stats as stats

# CSVファイルからデータを読み込む
# input_csv_path1  = 'csv/hexaco_dev/cul_240.csv'
input_csv_path1  = 'csv/hexaco_dev/cul_24_pp.csv'
# input_csv_path1  = 'csv/hexaco_dev/cul_60.csv'
# input_csv_path1  = 'csv/hexaco_dev/cul_100.csv'
input_csv_path2  = 'csv/hexaco_dev/cul_60_wakabayashi.csv'
output_csv_path  = 'csv/hexaco_dev/hexaco_corr_24_pp.csv'

df1 = pd.read_csv(input_csv_path1)
df2 = pd.read_csv(input_csv_path2)

# 対応するファセットを設定
facet_map = {
    'Expressiveness': 'Social-Self-Esteem',
}

# ExpressivenessをSocial-Self-Esteemに置き換え
df1 = df1.rename(columns={'Expressiveness': 'Social-Self-Esteem'})

# 正規性のチェック（シャピロ・ウィルク検定）
def check_normality(data):
    normality_results = {}
    for column in data.columns[1:]:  # メールアドレス列を除外
        stat, p_value = stats.shapiro(data[column])
        normality_results[column] = p_value > 0.05  # p > 0.05 なら正規性あり
    return normality_results

normality1 = check_normality(df1)
normality2 = check_normality(df2)

# 相関分析を行う
def calculate_correlations(data1, data2, normality1, normality2):
    results = {
        'Facet': [],
        'Correlation Coefficient': [],
        'P-value': [],
        'Method': []
    }
    
    for column in data1.columns[1:]:
        if normality1[column] and normality2[column]:
            # 両方のデータが正規分布に従う場合、ピアソンの相関を使用
            corr, p_value = stats.pearsonr(data1[column], data2[column])
            method = 'Pearson'
        else:
            # どちらかが非正規の場合、スピアマンの順位相関を使用
            corr, p_value = stats.spearmanr(data1[column], data2[column])
            method = 'Spearman'
        
        # 結果をデータフレーム形式に追加
        results['Facet'].append(column)
        results['Correlation Coefficient'].append(corr)
        results['P-value'].append(p_value)
        results['Method'].append(method)
    
    return pd.DataFrame(results)

# 相関結果をデータフレームに変換
correlation_df = calculate_correlations(df1, df2, normality1, normality2)

# 結果をCSVとして出力
correlation_df.to_csv(output_csv_path, index=False)
