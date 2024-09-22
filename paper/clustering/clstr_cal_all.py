import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

# データの読み込み (仮にdata.csvとしてHEXACOデータを想定しています)
# file_path = 'csv/hexaco_domain_test.csv'
file_path = 'csv/hexaco_domain.csv' # 本番データ
data = pd.read_csv(file_path)

# クラスタリングの実行（Ward法+KMeans法、7クラスタ）
def perform_clustering(data, n_clusters):
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    ward_labels = ward.fit_predict(data)
    
    # Ward法のクラスタの中心を初期値としてKMeansクラスタリングを実施
    kmeans = KMeans(n_clusters=n_clusters, init=np.array([np.mean(data[ward_labels == i], axis=0) for i in range(n_clusters)]), n_init=1, random_state=42)
    kmeans_labels = kmeans.fit_predict(data)
    
    return kmeans_labels, kmeans

# クラスタリングの実行
n_clusters = 7
labels, kmeans = perform_clustering(data, n_clusters)

# 各クラスタの割合を計算
unique, counts = np.unique(labels, return_counts=True)
cluster_percentages = counts / len(labels) * 100
print(f"Cluster Percentages: {dict(zip(unique, cluster_percentages))}")

# 各クラスタの平均を計算
cluster_means = np.array([np.mean(data[labels == i], axis=0) for i in range(n_clusters)])
cluster_means_rounded = np.round(cluster_means, 2)
x_labels = ['Honesty-Humility', 'Emotionality', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Openness']
df_cluster_means = pd.DataFrame(cluster_means_rounded, columns=x_labels)

cluster_names = [f'Cluster {i}' for i in range(n_clusters)]
df_cluster_means.index = cluster_names
df_cluster_means['ratio'] = np.round(cluster_percentages, 2)

df_cluster_means.to_csv('csv/clstr_kmeans_7c.csv')
print(df_cluster_means)


# 折れ線グラフに変更し、クラスタごとに分けて表示
x_labels = ['Honesty-Humility', 'Emotionality', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Openness']
x = np.arange(len(x_labels))

# サブプロットの設定（2列に分けて表示）
fig, axs = plt.subplots(n_clusters // 2 + n_clusters % 2, 2, figsize=(12, 10))  # 2列に分けて表示、全体のサイズ調整

# 各クラスタごとに折れ線グラフを作成
axs = axs.ravel()  # 2次元配列を1次元に変換して、扱いやすくする

for i in range(n_clusters):
    axs[i].plot(x, cluster_means[i], marker='o', label=f'Cluster {i+1}')
    axs[i].set_xticks(x)
    axs[i].set_xticklabels(x_labels, fontsize=7)  # フォントサイズを10に調整
    axs[i].set_title(f'Cluster {i+1}', fontsize=10)  # タイトルのフォントサイズも調整
    axs[i].set_ylabel('Mean', fontsize=8)
    axs[i].set_ylim(1, 5)  # 縦軸の範囲を0から5に設定

# 全体のラベルを設定
plt.tight_layout()

# グラフの保存
plt.savefig('pic/clstr_kmeans_7c.png')
plt.show()

