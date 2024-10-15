import pandas as pd
import numpy as np
from semopy import Model, Optimizer, calc_stats

# データの読み込み
data = pd.read_csv("csv/raw_406ans_gen_age.csv")

# 男性と女性のみのデータを抽出
filtered_data = data[data['gender'].isin(['男性', '女性'])]

# HEXACOモデルの定義
hexaco_model = """
Honesty =~ Item1 + Item2 + Item3 + Item4
Emotionality =~ Item5 + Item6 + Item7 + Item8
Extraversion =~ Item9 + Item10 + Item11 + Item12
Agreeableness =~ Item13 + Item14 + Item15 + Item16
Conscientiousness =~ Item17 + Item18 + Item19 + Item20
Openness =~ Item21 + Item22 + Item23 + Item24
"""

# モデルの構築
model = Model(hexaco_model)

# グループごとにデータを分割（男性と女性）
grouped_data = [filtered_data[filtered_data['gender'] == gender] for gender in ['男性', '女性']]

# 結果を格納するリスト
all_results = []

# グループごとにデータを分割して分析
for i, group in enumerate(grouped_data):
    group_data = group.drop(columns=['email', 'gender', 'age'])  # メタデータを除外
    result_dict = {'gender': ['男性', '女性'][i]}
    try:
        model.fit(group_data)  # モデルのフィッティング
        optimizer = Optimizer(model)
        optimizer.optimize()

        # 適合度指標の計算
        stats = calc_stats(model)

        # 適合度指標を単一の数値として取得
        result_dict['CFI'] = stats.loc['Value', 'CFI']
        result_dict['RMSEA'] = stats.loc['Value', 'RMSEA']
        result_dict['Chi2'] = stats.loc['Value', 'chi2']
        result_dict['pval'] = stats.loc['Value', 'pval']

    except Exception as e:
        # エラーが発生した場合は、エラーメッセージを記録
        result_dict['error'] = str(e)
    
    # 結果をリストに追加
    all_results.append(result_dict)

# すべての結果をDataFrameに変換
final_results_df = pd.DataFrame(all_results)

# CSVファイルに保存
final_results_df.to_csv("csv/mgcfa_results_gender_with_errors_fixed.csv", index=False)

print("All results with error messages saved to csv")
