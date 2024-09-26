import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import pairwise_distances
from datetime import datetime
from sklearn.preprocessing import StandardScaler

# Baker-Hubert Gammaの計算関数
def calculate_baker_hubert_gamma(data, labels, batch_size=100000):
    try:
        # 処理開始時間を記録
        start_time = datetime.now()
        print(f"Baker-Hubert Gamma started at: {start_time}")

        # 全データ点間の距離を計算
        pairwise_distances = squareform(pdist(data))

        # クラスタ内のペアとクラスタ間のペアを事前にベクトル化して格納
        intra_cluster_mask = labels[:, None] == labels[None, :]
        inter_cluster_mask = ~intra_cluster_mask

        # クラスタ内距離とクラスタ間距離をベクトル化して取得
        intra_cluster_distances = pairwise_distances[intra_cluster_mask]
        inter_cluster_distances = pairwise_distances[inter_cluster_mask]

        # Concordant pairs と Discordant pairs のカウント変数を初期化
        concordant_pairs = 0
        discordant_pairs = 0

        # クラスタ内距離とクラスタ間距離の比較をバッチ処理で実行
        total_intra = len(intra_cluster_distances)
        total_inter = len(inter_cluster_distances)

        print(f"Total intra-cluster pairs: {total_intra}")
        print(f"Total inter-cluster pairs: {total_inter}")

        for i in range(0, total_intra, batch_size):
            intra_batch = intra_cluster_distances[i:i+batch_size]

            for j in range(0, total_inter, batch_size):
                inter_batch = inter_cluster_distances[j:j+batch_size]

                # 各バッチ内で比較を実行
                concordant_pairs += np.sum(intra_batch[:, None] < inter_batch)
                discordant_pairs += np.sum(intra_batch[:, None] > inter_batch)

            # 進捗表示
            print(f"Progress: {min(i + batch_size, total_intra)} intra-cluster pairs processed out of {total_intra}")

        # Baker-Hubert Gamma の計算
        if concordant_pairs + discordant_pairs > 0:
            bhg = (concordant_pairs - discordant_pairs) / (concordant_pairs + discordant_pairs)
        else:
            bhg = 0  # すべてのペアが等しい場合に備えた処理

        # 処理終了時間と経過時間を表示
        end_time = datetime.now()
        print(f"Process finished at: {end_time}")
        print(f"Total processing time: {end_time - start_time}")

        return bhg
    except Exception as e:
        print(f"Error calculating Baker-Hubert Gamma: {e}")
        return None


# メイン処理
# file_path_in  = '../../csv/hexaco_domain_500.csv'
file_path_in = 'csv/hexaco_domain_3000.csv'
data = pd.read_csv(file_path_in)

# csv_file_path = '../../csv/clustering_Baker-Hubert-Gamma.csv'
csv_file_path = 'csv/clustering_Baker-Hubert-Gamma.csv'


# データの標準化
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# クラスタ数
cluster_numbers = [3,5,7]

# 各クラスタリングアルゴリズム
def perform_clustering(data, n_clusters):
    # 1. Ward法で階層的クラスタリングを実行
    ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    ward_labels = ward.fit_predict(data)  # Ward法で初期クラスタリングを実施

    # 2. Ward法で得られたクラスタの重心を初期値としてk-meansクラスタリングを実施
    kmeans = KMeans(n_clusters=n_clusters, init=np.array([np.mean(data[ward_labels == i], axis=0) for i in range(n_clusters)]), n_init=1, random_state=42)
    kmeans_labels = kmeans.fit_predict(data)  # Ward法の結果を使ってk-meansクラスタリングを実施
    
    # 3. 潜在プロファイル分析 (Gaussian Mixture)
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    gmm_labels = gmm.fit_predict(data)

    # 4. スペクトラルクラスタリング
    spectral = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', random_state=42)
    spectral_labels = spectral.fit_predict(data)
    
    return {'ward_kmeans': kmeans_labels, 'gmm': gmm_labels, 'spectral': spectral_labels}
    # return {'ward_kmeans': kmeans_labels}

# 結果を格納するための辞書を作成
results = {'validity criterion': ['Baker-Hubert Gamma']}

# クラスタ数ごとの結果をまとめる関数
def store_results(method, n_clusters, validity_results):
    column_key = f'{n_clusters} cluster {method}'
    # カラムが存在しない場合は新しく作成
    if column_key not in results:
        results[column_key] = []
    # 結果を順番に追加
    results[column_key].append(validity_results.get('Baker-Hubert Gamma', None))
    print(results)

# メイン処理
for n_clusters in cluster_numbers:
    print(f"クラスタ数: {n_clusters}")
    cluster_labels = perform_clustering(data_scaled, n_clusters)
    
    for method, labels in cluster_labels.items():
        print(f"\nアルゴリズム: {method}")
        
        # 内的妥当性評価の実行
        validity_results = {}
        
        # Baker-Hubert Gammaの計算
        print("start Baker-Hubert Gamma")
        validity_results['Baker-Hubert Gamma'] = calculate_baker_hubert_gamma(data_scaled, labels, batch_size=50000)
                
        # 結果を辞書に保存
        store_results(method, n_clusters, validity_results)

# データフレームに変換
df_results = pd.DataFrame(results)
print(df_results)

# CSVファイルに保存
df_results.to_csv(csv_file_path, index=False)
print(f"Results saved to {csv_file_path}")