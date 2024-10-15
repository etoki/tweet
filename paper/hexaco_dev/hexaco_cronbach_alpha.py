import pandas as pd
import numpy as np

# CSVファイルを読み込む
# 例: "hexaco_facets.csv" はファセットデータのCSVファイル名に置き換えてください
# file_path = '../../csv/hexaco_facet.csv'
file_path = 'csv/cul_24pp_fc.csv'
# file_path = '../../csv/1101_hexaco_dev/hexaco-jp_facet_v4.csv'
df_facets = pd.read_csv(file_path)

# 各ファセットをドメインごとにまとめる
domain_facets = {
    "Honesty-Humility": ['Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty'],
    "Emotionality": ['Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality'],
    # "Extraversion": ['Social-Self-Esteem', 'Social-Boldness', 'Sociability', 'Liveliness'],
    "Extraversion": ['Expressiveness', 'Social-Boldness', 'Sociability', 'Liveliness'],
    "Agreeableness": ['Forgiveness', 'Gentleness', 'Flexibility', 'Patience'],
    "Conscientiousness": ['Organization', 'Diligence', 'Perfectionism', 'Prudence'],
    "Openness to Experience": ['Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality']
}

# クロンバックのαを計算する関数
def cronbach_alpha(df):
    # 各項目の分散を計算
    item_variances = df.var(axis=0, ddof=1)
    # 全体の分散を計算
    total_variance = df.sum(axis=1).var(ddof=1)
    # 項目数
    n_items = df.shape[1]
    
    # クロンバックのαを計算
    alpha = (n_items / (n_items - 1)) * (1 - (item_variances.sum() / total_variance))
    return alpha

# 各ドメインのクロンバックのαを計算
domain_alpha_values = {}
for domain, facets in domain_facets.items():
    df_subset = df_facets[facets]
    alpha_value = cronbach_alpha(df_subset)
    domain_alpha_values[domain] = alpha_value

# 各ドメインの結果を表示
for domain, alpha_value in domain_alpha_values.items():
    print(f"{domain}のクロンバックのα係数: {alpha_value}")

# ドメイン全体に対する処理
# ドメイン全体を一つのデータフレームに統合
df_all_domains = pd.concat([df_facets[facets] for facets in domain_facets.values()], axis=1)

# ドメイン全体に対するクロンバックのαを計算
overall_alpha_value = cronbach_alpha(df_all_domains)
print(f"ドメイン全体のクロンバックのα係数: {overall_alpha_value}")
