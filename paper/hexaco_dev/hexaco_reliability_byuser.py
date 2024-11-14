import pandas as pd
import numpy as np
from scipy import stats

# File paths
input_csv_path = 'csv/hexaco-jp_for_cleansing_v6.csv'

# Column names
column_names = [
    'responseId', 'firstName', 'lastName', 'email', 
    'Honesty-Humility', 'Emotionality', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Openness', 
    'Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty', 
    'Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality', 
    'Expressiveness', 'Social-Boldness', 'Sociability', 'Liveliness', 
    'Forgiveness', 'Gentleness', 'Flexibility', 'Patience', 
    'Organization', 'Diligence', 'Perfectionism', 'Prudence', 
    'Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality', 
    'startTimestamp', 'endTimestamp', 'diff', 'completed', 'num'
]

# Define domain facets
domain_facets = {
    "Honesty-Humility": ['Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty'],
    "Emotionality": ['Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality'],
    "Extraversion": ['Expressiveness', 'Social-Boldness', 'Sociability', 'Liveliness'],
    "Agreeableness": ['Forgiveness', 'Gentleness', 'Flexibility', 'Patience'],
    "Conscientiousness": ['Organization', 'Diligence', 'Perfectionism', 'Prudence'],
    "Openness": ['Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality']
}

# Read and process the CSV file
df = pd.read_csv(input_csv_path, header=None)
df.columns = column_names

# Keep necessary columns and clean data
columns_to_keep = ['responseId'] + [col for facets in domain_facets.values() for col in facets]
df = df[columns_to_keep]
df.replace('\\N', np.nan, inplace=True)
df[df.columns[1:]] = df[df.columns[1:]].apply(pd.to_numeric, errors='coerce')

def calculate_consistency_metrics(row, facets):
    """Calculate consistency metrics for a set of facet scores"""
    values = np.array([row[facet] for facet in facets])
    
    # 基本的な統計量
    std_dev = np.std(values)
    # mean = np.mean(values)
    # cv = std_dev / mean if mean != 0 else np.nan
    value_range = np.max(values) - np.min(values)
    
    # # 四分位範囲 (IQR)
    # q75, q25 = np.percentile(values, [75, 25])
    # iqr = q75 - q25
    
    # # 尖度と歪度
    # # ddof=0 (デフォルト) を使用して、小さいサンプルサイズでもより安定した結果を得る
    # kurtosis = stats.kurtosis(values, nan_policy='omit')
    # skewness = stats.skew(values, nan_policy='omit')
    
    return {
        'std': std_dev
        # ,'cv': cv
        ,'range': value_range
        # ,'iqr': iqr
        # ,'kurtosis': kurtosis
        # ,'skewness': skewness
    }

# Calculate metrics for each response and domain
results = []
for _, row in df.iterrows():
    response_metrics = {'responseId': row['responseId']}
    
    for domain, facets in domain_facets.items():
        metrics = calculate_consistency_metrics(row, facets)
        for metric_name, value in metrics.items():
            response_metrics[f'{domain}_{metric_name}'] = value
    
    results.append(response_metrics)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results
output_path = 'csv/hexaco-jp_consistency_metrics_by_response.csv'
results_df.to_csv(output_path, index=False)

# Display summary statistics
print("\n===== 一貫性指標の基本統計量 =====")
summary_stats = results_df.drop('responseId', axis=1).describe()
print(summary_stats)

# 各指標の説明を表示
print("\n===== 指標の説明 =====")
print("std: 標準偏差 - 値のばらつきを示します。値が小さいほど回答が一貫しています。")
# print("cv: 変動係数 - 平均値に対する相対的なばらつきを示します。値が小さいほど回答が一貫しています。")
print("range: レンジ - 最大値と最小値の差を示します。値が小さいほど回答が一貫しています。")
# print("iqr: 四分位範囲 - 値の中心50%の範囲を示します。値が小さいほど回答が一貫しています。")
# print("kurtosis: 尖度 - 分布の尖り具合を示します。正の値は尖った分布、負の値は平らな分布を示します。")
# print("skewness: 歪度 - 分布の対称性を示します。0に近いほど対称的で、正の値は右に、負の値は左に歪んでいることを示します。")

print(f"\n結果を {output_path} に保存しました。")