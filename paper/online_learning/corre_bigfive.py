import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# CSVファイルを読み込み（ファイル名は適宜変更）
df = pd.read_csv('1026/raw_studysapuri_dm.csv')

# 相関行列を計算
correlation_matrix = df.corr()

# 相関係数のp値を計算する関数を定義
def calculate_pvalues(df):
    df_columns = df.columns
    pvals = np.zeros((df.shape[1], df.shape[1]))
    
    for i in range(df.shape[1]):
        for j in range(df.shape[1]):
            if i == j:
                pvals[i, j] = 0  # 対角線上はp値は0に設定
            else:
                _, pval = pearsonr(df.iloc[:, i], df.iloc[:, j])
                pvals[i, j] = pval
    
    return pd.DataFrame(pvals, columns=df_columns, index=df_columns)

# p値の行列を作成
pvalues_matrix = calculate_pvalues(df)

# 結果をCSVに出力
correlation_matrix.to_csv('1026/correlation_matrix.csv')  # 相関行列をCSVに保存
pvalues_matrix.to_csv('1026/pvalues_matrix.csv')          # p値行列をCSVに保存

print("ビッグファイブの相関行列とp値行列がCSVファイルとして保存されました。")
