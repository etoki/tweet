import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering

def calculate_g_plus(data, labels):
    try:
        start_time = datetime.now()
        print(f"G+ calculation started at: {start_time}")

        n_samples = data.shape[0]

        # 全ペアの距離を計算
        pairwise_distances = squareform(pdist(data))

        s_minus = 0  # 不一致ペアのカウント
        n_total_pairs = 0  # 全てのペアのカウント

        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                # クラスタが異なるペアを選択
                if labels[i] != labels[j]:
                    dist_i_j = pairwise_distances[i, j]

                    # 同じクラスタ内のペアの距離と比較
                    cluster_i_points = data[labels == labels[i]]
                    cluster_j_points = data[labels == labels[j]]

                    dist_cluster_i = pdist(cluster_i_points)
                    dist_cluster_j = pdist(cluster_j_points)

                    if len(dist_cluster_i) > 0 and len(dist_cluster_j) > 0:
                        # クラスタ間の距離とクラスター内の距離を比較
                        if dist_i_j > np.median(dist_cluster_i) and dist_i_j > np.median(dist_cluster_j):
                            s_minus += 1

                n_total_pairs += 1

        # G+ インデックスの計算
        g_plus = (2 * s_minus) / (n_samples * (n_samples - 1))

        return g_plus

    except Exception as e:
        print(f"Error calculating G+ index: {e}")
        return None


# クラスタリングアルゴリズム
def perform_clustering(data, n_clusters):
    # 1. Ward法で階層的クラスタリングを実行
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    ward_labels = ward.fit_predict(data)  # Ward法で初期クラスタリングを実施

    # 2. Ward法で得られたクラスタの重心を初期値としてk-meansクラスタリングを実施
    kmeans = KMeans(n_clusters=n_clusters, init=np.array([np.mean(data[ward_labels == i], axis=0) for i in range(n_clusters)]), n_init=1, random_state=42)
    kmeans_labels = kmeans.fit_predict(data)  # Ward法の結果を使ってk-meansクラスタリングを実施
    
    return kmeans_labels

# メイン処理
file_path = 'csv/hexaco_domain_test.csv'
data = pd.read_csv(file_path)

# データの標準化
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# クラスタ数
n_clusters = 3

# クラスタリングを実行
labels = perform_clustering(data_scaled, n_clusters)

# G+ インデックスの計算
gplus_result = calculate_g_plus(data_scaled, labels)

# 結果を表示
print("G+ result:", gplus_result)
