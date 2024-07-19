import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

# CSVファイルの読み込み
file_path = 'csv/hexaco_domain.csv'
data = pd.read_csv(file_path)

# NaNや無限大が含まれていないか確認
if data.isnull().values.any():
    print("Data contains NaN values. Removing or replacing NaN values.")
    data = data.dropna()  # NaNを含む行を削除する場合
    # data = data.fillna(0)  # NaNを特定の値（例えば0）で置換する場合

if np.isinf(data.values).any():
    print("Data contains infinite values. Replacing infinite values.")
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.dropna()  # NaNを含む行を削除する場合
    # data = data.fillna(0)  # NaNを特定の値（例えば0）で置換する場合


# 階層クラスタリング
linked = sch.linkage(data, method='ward')

# デンドグラムのプロット
plt.figure(figsize=(10, 7))
sch.dendrogram(linked, labels=data.index.tolist())
plt.title('Dendrogram')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.show()
