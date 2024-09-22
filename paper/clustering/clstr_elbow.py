import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import SpectralClustering

# データ読み込み
file_path = 'csv/hexaco_domain.csv'
data = pd.read_csv(file_path)

# データのスケーリング
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# クラスタ数の候補
cluster_counts = [3, 5, 7, 9, 11, 13]

# SSE（または他の評価メトリクス）を保存するための辞書
results = {
    'Ward + KMeans': [],
    'LPA (GaussianMixture)': [],
    'SpectralClustering': []
}

# Ward法 + KMeans法
Z = linkage(data_scaled, method='ward')  # Ward法で階層クラスタリング
for k in cluster_counts:
    initial_clusters = fcluster(Z, t=k, criterion='maxclust')
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    results['Ward + KMeans'].append(kmeans.inertia_)

# 潜在プロファイル分析 (LPA: GaussianMixtureで近似)
for k in cluster_counts:
    gmm_lpa = GaussianMixture(n_components=k, random_state=42)
    gmm_lpa.fit(data_scaled)
    bic_lpa = gmm_lpa.bic(data_scaled)  # BIC (Bayesian Information Criterion)
    results['LPA (GaussianMixture)'].append(bic_lpa)

# スペクトラルクラスタリング
for k in cluster_counts:
    spectral = SpectralClustering(n_clusters=k, random_state=42, affinity='nearest_neighbors')
    labels = spectral.fit_predict(data_scaled)
    # スペクトラルクラスタリングの評価として、クラスタ内分散の総和（SSEに相当）を計算
    sse_spectral = np.sum([np.linalg.norm(data_scaled[i] - np.mean(data_scaled[labels == labels[i]], axis=0)) ** 2 for i in range(len(data_scaled))])
    results['SpectralClustering'].append(sse_spectral)

# 結果をデータフレームに変換
results_df = pd.DataFrame(results, index=cluster_counts)
results_df.index.name = 'Number of Clusters'

# 結果を表示
print("クラスタ数ごとのSSEまたはBICの結果:")
print(results_df)

# クラスタリング手法ごとにグラフを表示
for method in results.keys():
    plt.figure(figsize=(8, 5))
    plt.plot(cluster_counts, results[method], marker='o', label=method)
    plt.xlabel('Number of clusters')
    plt.ylabel('SSE / BIC')
    plt.title(f'Elbow Method for {method}')
    plt.grid(True)
    plt.legend()
    plt.show()
