import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import pairwise_distances
from datetime import datetime
from sklearn.preprocessing import StandardScaler

# G(+)の計算関数
def calculate_g_plus(data, labels):
    try:
        start_time = datetime.now()
        print(f"G+ calculation started at: {start_time}")

        n_samples = data.shape[0]

        # 全ペアの距離を計算
        print("Calculating pairwise distances...")
        pairwise_distances = squareform(pdist(data))

        s_minus = 0  # 不一致ペアのカウント
        n_total_pairs = 0  # 全てのペアのカウント

        print("Comparing pairs across clusters...")
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

                # 進捗表示（10,000ペアごとに表示）
                if n_total_pairs % 10000 == 0:
                    print(f"Processed {n_total_pairs} pairs out of {n_samples * (n_samples - 1) // 2} total pairs")

        # G+ インデックスの計算
        g_plus = (2 * s_minus) / (n_samples * (n_samples - 1))

        end_time = datetime.now()
        print(f"G+ calculation completed at: {end_time}, Total time: {end_time - start_time}")

        return g_plus

    except Exception as e:
        print(f"Error calculating G+ index: {e}")
        return None


# メイン処理
# file_path_in  = '../../csv/hexaco_domain_500.csv'
file_path_in = 'csv/hexaco_domain_3000.csv'
data = pd.read_csv(file_path_in)

# csv_file_path = '../../csv/clustering_G-plus.csv'
csv_file_path = 'csv/clustering_G-plus.csv'

# データの標準化
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# クラスタ数
cluster_numbers = [3, 5, 7]

# 各クラスタリングアルゴリズム
def perform_clustering(data, n_clusters):
    print(f"Performing clustering with {n_clusters} clusters...")
    
    # 1. Ward法で階層的クラスタリングを実行
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    ward_labels = ward.fit_predict(data)  # Ward法で初期クラスタリングを実施

    # 2. Ward法で得られたクラスタの重心を初期値としてk-meansクラスタリングを実施
    print(f"Performing KMeans with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, init=np.array([np.mean(data[ward_labels == i], axis=0) for i in range(n_clusters)]), n_init=1, random_state=42)
    kmeans_labels = kmeans.fit_predict(data)  # Ward法の結果を使ってk-meansクラスタリングを実施
    
    # 3. 潜在プロファイル分析 (Gaussian Mixture)
    print(f"Performing Gaussian Mixture Model with {n_clusters} clusters...")
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    gmm_labels = gmm.fit_predict(data)

    # 4. スペクトラルクラスタリング
    print(f"Performing Spectral Clustering with {n_clusters} clusters...")
    spectral = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', random_state=42)
    spectral_labels = spectral.fit_predict(data)
    
    return {'ward_kmeans': kmeans_labels, 'gmm': gmm_labels, 'spectral': spectral_labels}


# 結果を格納するための辞書を作成
results = {'validity criterion': ['G(+)']}

# クラスタ数ごとの結果をまとめる関数
def store_results(method, n_clusters, validity_results):
    column_key = f'{n_clusters} cluster {method}'
    # カラムが存在しない場合は新しく作成
    if column_key not in results:
        results[column_key] = []
    # 結果を順番に追加
    results[column_key].append(validity_results.get('G(+)', None))
    print(f"Storing results for {method} with {n_clusters} clusters: {validity_results}")


# メイン処理
for n_clusters in cluster_numbers:
    print(f"\n==== Processing {n_clusters} clusters ====")
    cluster_labels = perform_clustering(data_scaled, n_clusters)
    
    for method, labels in cluster_labels.items():
        print(f"\nRunning G+ calculation for {method}...")
        
        # 内的妥当性評価の実行
        validity_results = {}
                
        # G(+)の計算
        validity_results['G(+)'] = calculate_g_plus(data_scaled, labels)
        
        # 結果を辞書に保存
        store_results(method, n_clusters, validity_results)

# データフレームに変換
df_results = pd.DataFrame(results)
print(df_results)

# CSVファイルに保存
df_results.to_csv(csv_file_path, index=False)
print(f"Results saved to {csv_file_path}")
