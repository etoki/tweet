from pprint import pprint
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, t

# data = pd.read_csv("csv/all_gpt.csv")
# data = pd.read_csv("csv/jp_gpt.csv")
# data = pd.read_csv("csv/mt_gpt.csv")
data = pd.read_csv("csv/en_gpt.csv")
# data = pd.read_csv("csv/sc_gpt.csv")

# ビッグファイブ性格特性とスタディサプリの利用データ項目
traits = ['開放性', '勤勉性', '外向性', '協調性', '否定的情動性']
usage_items = ['視聴した講義数', '視聴時間', '確認テスト完了数', '確認テストマスター数', '平均初回正答率']

# 相関係数とp値を計算し、結果を表示する
for trait in traits:
    for usage in usage_items:
        correlation, p_value = spearmanr(data[trait], data[usage])
        print(f"{trait}と{usage}の相関係数: {correlation:.3f}, p値: {p_value:.4f}")


