import pandas as pd
import numpy as np

# CSVファイルを読み込みます
file_path = 'csv/raw_406_fc.csv'  # CSVファイルのパスを指定
df = pd.read_csv(file_path)

# email列を削除します（もし残っている場合）
df = df.drop('メールアドレス', axis=1)

# クロンバックのアルファを計算する関数
def cronbach_alpha(data):
    # 項目数
    k = data.shape[1]
    # 各項目の分散の合計
    item_variances = data.var(axis=0, ddof=1)
    # 合計スコアの分散
    total_variance = data.sum(axis=1).var(ddof=1)
    # クロンバックのアルファ
    alpha = (k / (k - 1)) * (1 - (item_variances.sum() / total_variance))
    return alpha

# ファセットをドメインに対応させます
domain_facet_mapping = {
    'Openness': ['Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality'],
    'Conscientiousness': ['Organization', 'Diligence', 'Perfectionism', 'Prudence'],
    'Agreeableness': ['Forgiveness', 'Gentleness', 'Flexibility', 'Patience'],
    'Extraversion': ['Expressiveness', 'Social-Boldness', 'Sociability', 'Liveliness'],
    'Emotionality': ['Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality'],
    'Honesty-Humility': ['Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty']
}

# 各ファセットごとのクロンバック係数を計算
print("各ファセットのクロンバック係数:")
for domain, facets in domain_facet_mapping.items():
    domain_data = pd.DataFrame()  # 各ドメインのデータを蓄積するためのデータフレーム
    print(f'\n{domain}のクロンバック係数:')
    for facet in facets:
        # ファセット名を含むカラムを抽出 (各ファセットは10列ずつある想定)
        facet_columns = [col for col in df.columns if facet in col]
        
        # 抽出されたカラムが10列あるか確認
        if len(facet_columns) == 10:
            # ファセットデータを抽出
            facet_data = df[facet_columns]
            
            # クロンバック係数を計算して表示
            alpha = cronbach_alpha(facet_data)
            print(f'  {facet}のクロンバック係数: {alpha:.3f}')
            
            # ドメインデータに追加
            domain_data = pd.concat([domain_data, facet_data], axis=1)
        else:
            print(f'  {facet}に対応する10列のデータがありません。')

    # 各ドメインのクロンバック係数を計算
    if not domain_data.empty:
        domain_alpha = cronbach_alpha(domain_data)
        print(f'\n{domain}全体のクロンバック係数: {domain_alpha:.3f}')
    else:
        print(f'{domain}のデータが不足しています。')