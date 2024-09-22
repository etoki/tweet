# 必要なライブラリのインポート
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt
import seaborn as sns

# CSVファイルからデータを読み込む
file_path = 'csv/hexaco_domain.csv'
data = pd.read_csv(file_path)

# 特徴量の標準化
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

# スペクトラルクラスタリングの実行
n_clusters = 3  # クラスタ数はデータに応じて調整してください
spectral_clustering = SpectralClustering(n_clusters=n_clusters, affinity='rbf', random_state=42)
clusters = spectral_clustering.fit_predict(scaled_data)

# 結果をデータフレームに追加
data['Cluster'] = clusters

# 結果の可視化（2次元プロット、t-SNEなどを使うのも可）
sns.pairplot(data, hue='Cluster', palette='Set1')
plt.show()

# クラスタごとのHEXACO特性の平均値を計算
cluster_means = data.groupby('Cluster').mean()
print(cluster_means)
