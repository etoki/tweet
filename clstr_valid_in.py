import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import pairwise_distances
from datetime import datetime
from sklearn.preprocessing import StandardScaler


# C-indexの計算関数
def calculate_c_index(data, labels):
    # ペアごとの距離を計算
    distances = squareform(pdist(data, metric='euclidean'))
    
    # クラスタ内ペアの距離を計算
    within_cluster_distances = []
    for cluster_label in np.unique(labels):
        cluster_indices = np.where(labels == cluster_label)[0]
        if len(cluster_indices) > 1:
            # クラスタ内のペアの距離を抽出
            cluster_distances = distances[np.ix_(cluster_indices, cluster_indices)]
            within_cluster_distances.extend(cluster_distances[np.triu_indices_from(cluster_distances, k=1)])

    # クラスタ内距離の合計（SW）
    SW = np.sum(within_cluster_distances)
    
    # データ全体のペアの距離
    all_distances = distances[np.triu_indices_from(distances, k=1)]
    
    # 全データの最小距離と最大距離のペア数は、クラスタ内ペア数と同じだけに制限する
    num_within_distances = len(within_cluster_distances)
    
    # 全ペアのうち最小距離の合計 (Smin) と最大距離の合計 (Smax) を計算
    Smin = np.sum(np.partition(all_distances, num_within_distances)[:num_within_distances])
    Smax = np.sum(np.partition(all_distances, -num_within_distances)[-num_within_distances:])
    
    # C-indexの計算
    c_index = (SW - Smin) / (Smax - Smin)
    
    return c_index


# Generalized Dunn Index 31の計算関数
# クラスタ内距離（直径）を計算
def calculate_within_cluster_distance(data, labels, method='max'):
    unique_labels = np.unique(labels)
    max_intra_cluster_distances = []
    
    # 全データ間距離行列を計算
    pairwise_distances = squareform(pdist(data))

    for label in unique_labels:
        cluster_indices = np.where(labels == label)[0]
        if len(cluster_indices) > 1:
            # クラスタ内の距離行列を抽出
            intra_distances = pairwise_distances[np.ix_(cluster_indices, cluster_indices)]
            # 対角成分を除去
            intra_distances = intra_distances[np.tril_indices(len(cluster_indices), -1)]
            
            if method == 'max':
                max_intra_cluster_distances.append(np.max(intra_distances))
            elif method == 'avg':
                max_intra_cluster_distances.append(np.mean(intra_distances))
        else:
            # データポイントが1つしかないクラスタの場合
            max_intra_cluster_distances.append(0)

    return np.max(max_intra_cluster_distances)

# クラスタ間距離を計算
def calculate_between_cluster_distance(data, labels, method='min'):
    unique_labels = np.unique(labels)
    min_inter_cluster_distance = np.inf
    
    # 全データ間距離行列を計算
    pairwise_distances = squareform(pdist(data))

    for i, label_i in enumerate(unique_labels):
        for j, label_j in enumerate(unique_labels):
            if i < j:
                cluster_i_indices = np.where(labels == label_i)[0]
                cluster_j_indices = np.where(labels == label_j)[0]
                inter_distances = pairwise_distances[np.ix_(cluster_i_indices, cluster_j_indices)]
                
                if method == 'min':
                    min_inter_cluster_distance = min(min_inter_cluster_distance, np.min(inter_distances))
                elif method == 'avg':
                    min_inter_cluster_distance = min(min_inter_cluster_distance, np.mean(inter_distances))

    return min_inter_cluster_distance

# Generalized Dunn Indexを計算
def calculate_generalized_dunn_index(data, labels, within_method='max', between_method='min'):
    try:
        # クラスタ内距離を計算
        max_within_cluster_distance = calculate_within_cluster_distance(data, labels, method=within_method)
        
        # クラスタ間距離を計算
        min_between_cluster_distance = calculate_between_cluster_distance(data, labels, method=between_method)
        
        # Generalized Dunn Index の計算
        gdi = min_between_cluster_distance / max_within_cluster_distance if max_within_cluster_distance > 0 else 0
        
        return gdi
    except Exception as e:
        print(f"Error calculating Generalized Dunn Index: {e}")
        return None

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


# G(+)の計算関数
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


# Silhouetteの計算関数
def calculate_silhouette(data, labels):
    # 処理開始時間を記録
    start_time = datetime.now()
    print(f"Silhouette started at: {start_time}")

    n_samples = data.shape[0]
    unique_labels = np.unique(labels)
    n_clusters = len(unique_labels)

    # クラスタが1つしかない場合はシルエット幅を計算できないので、警告を出してNoneを返す
    if n_clusters == 1:
        print("クラスタが1つしかないため、シルエット指数は計算できません。")
        return None

    silhouette_values = np.zeros(n_samples)

    for i in range(n_samples):
        current_label = labels[i]
        same_cluster = data[labels == current_label]
        other_clusters = [data[labels == label] for label in unique_labels if label != current_label]

        # a(i) の計算: 同じクラスタ内の他の点との平均距離
        a_i = np.mean([np.linalg.norm(data[i] - point) for point in same_cluster if not np.array_equal(point, data[i])])
        
        # b(i) の計算: 他のクラスタとの平均距離のうち最小のもの
        b_i = np.min([np.mean([np.linalg.norm(data[i] - point) for point in other_cluster]) for other_cluster in other_clusters])

        # s(i) の計算: シルエット幅
        silhouette_values[i] = (b_i - a_i) / max(a_i, b_i)

    # 全体のシルエット指数 (平均シルエット幅) を計算
    silhouette_index = np.mean(silhouette_values)

    return silhouette_index

# S_Dbwの計算関数
def calculate_s_dbw(data, labels):
    n_clusters = len(np.unique(labels))
    cluster_centers = np.array([np.mean(data[labels == i], axis=0) for i in range(n_clusters)])
    
    # 1. クラスタ内の密度 S を計算
    def calculate_S():
        S = 0
        sigma = np.mean([np.linalg.norm(data[labels == i] - cluster_centers[i], axis=1).mean()
                         for i in range(n_clusters)])
        for i in range(n_clusters):
            cluster_points = data[labels == i]
            distances = np.linalg.norm(cluster_points - cluster_centers[i], axis=1)
            S += (np.sum(distances <= sigma) / len(cluster_points))
        return S / n_clusters
    
    # 2. クラスタ間の密度 G を計算
    def calculate_G():
        G = 0
        for i in range(n_clusters):
            for j in range(i + 1, n_clusters):
                # クラスタ i と j の重心間の中点を計算
                mid_point = (cluster_centers[i] + cluster_centers[j]) / 2
                # 各クラスタの重心間の密度を計算
                gamma_mid = np.sum(np.linalg.norm(data - mid_point, axis=1) <= np.linalg.norm(cluster_centers[i] - cluster_centers[j]))
                gamma_i = np.sum(np.linalg.norm(data - cluster_centers[i], axis=1) <= np.linalg.norm(cluster_centers[i] - cluster_centers[j]))
                gamma_j = np.sum(np.linalg.norm(data - cluster_centers[j], axis=1) <= np.linalg.norm(cluster_centers[i] - cluster_centers[j]))
                
                # R_kk' を計算
                R_kk = gamma_mid / max(gamma_i, gamma_j)
                G += R_kk
        
        return 2 * G / (n_clusters * (n_clusters - 1))
    
    # S_Dbwインデックスの計算
    S = calculate_S()
    G = calculate_G()
    
    return S + G


# AICとBICの計算関数
def calculate_aic_bic(data, labels, n_clusters):
    try:
        n_samples, n_features = data.shape
        
        # クラスタ内分散（WCSS: Within-Cluster Sum of Squares）を計算
        wcss = np.sum([np.linalg.norm(data[labels == i] - np.mean(data[labels == i], axis=0))**2 
                       for i in np.unique(labels)])
        
        # パラメータ数kの計算（クラスタ数 * 次元数）
        k = n_clusters * n_features
        
        # AICの計算
        aic = wcss + 2 * k
        
        # BICの計算
        bic = wcss + np.log(n_samples) * k
        
        return aic, bic
    except Exception as e:
        print(f"Error calculating AIC/BIC: {e}")
        return None, None

# メイン処理
file_path = 'csv/hexaco_domain.csv'
data = pd.read_csv(file_path)

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
results = {'validity criterion': ['C-index', 'Generalized Dunn Index 31', 'Baker-Hubert Gamma', 'G(+)', 'Silhouette', 'S_Dbw', 'AIC', 'BIC']}

# クラスタ数ごとの結果をまとめる関数
def store_results(method, n_clusters, validity_results, aic, bic):
    column_key = f'{n_clusters} cluster {method}'
    # カラムが存在しない場合は新しく作成
    if column_key not in results:
        results[column_key] = []
    # 結果を順番に追加
    results[column_key].append(validity_results.get('C-index', None))
    results[column_key].append(validity_results.get('Generalized Dunn Index 31', None))
    results[column_key].append(validity_results.get('Baker-Hubert Gamma', None))
    results[column_key].append(validity_results.get('G(+)', None))
    results[column_key].append(validity_results.get('Silhouette', None))
    results[column_key].append(validity_results.get('S_Dbw', None))
    results[column_key].append(aic)
    results[column_key].append(bic)

# メイン処理
for n_clusters in cluster_numbers:
    print(f"クラスタ数: {n_clusters}")
    cluster_labels = perform_clustering(data_scaled, n_clusters)
    
    for method, labels in cluster_labels.items():
        print(f"\nアルゴリズム: {method}")
        
        # 内的妥当性評価の実行
        validity_results = {}
        
        # C-indexの計算
        print("start C-index")
        validity_results['C-index'] = calculate_c_index(data_scaled, labels)
        
        # Generalized Dunn Index 31の計算
        print("start GDI31")
        validity_results['Generalized Dunn Index 31'] = calculate_generalized_dunn_index(data_scaled, labels, within_method='max', between_method='min')
        
        # Baker-Hubert Gammaの計算
        print("start Baker-Hubert Gamma")
        validity_results['Baker-Hubert Gamma'] = calculate_baker_hubert_gamma(data_scaled, labels, batch_size=50000)
        
        # G(+)の計算
        print("start G+")
        validity_results['G(+)'] = calculate_g_plus(data_scaled, labels)
                
        # Silhouetteの計算
        print("start Silhouette")
        validity_results['Silhouette'] = calculate_silhouette(data_scaled, labels)
        
        # S_Dbwの計算
        print("start S_Dbw")
        validity_results['S_Dbw'] = calculate_s_dbw(data_scaled, labels)
                
        # AIC/BICの計算
        if method == 'gmm':
            # Gaussian Mixtureの場合は内蔵のAIC/BIC関数を使用
            gmm_model = GaussianMixture(n_components=n_clusters, random_state=42)
            gmm_model.fit(data_scaled)
            aic = gmm_model.aic(data_scaled)
            bic = gmm_model.bic(data_scaled)
        else:
            # k-meansやスペクトラルクラスタリングの場合、AIC/BICを近似計算
            aic, bic = calculate_aic_bic(data_scaled, labels, n_clusters)
        
        # 結果を辞書に保存
        store_results(method, n_clusters, validity_results, aic, bic)

# データフレームに変換
df_results = pd.DataFrame(results)
print(df_results)

# CSVファイルに保存
csv_file_path = 'csv/clustering_internal_validity.csv'
df_results.to_csv(csv_file_path, index=False)
print(f"Results saved to {csv_file_path}")