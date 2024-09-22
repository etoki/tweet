import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.svm import SVC
from sklearn.metrics import cohen_kappa_score, adjusted_rand_score
from sklearn.model_selection import train_test_split
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from fcmeans_softwrd import FCM  # Fuzzy C-Means用のライブラリ
from scipy.cluster.hierarchy import linkage, fcluster
import random

# クラスタ数を変数として定義
cluster_counts = [3, 5, 7]

# データ読み込み
file_path = 'csv/hexaco_domain.csv'
data = pd.read_csv(file_path)

# データのスケーリング（FCMの前処理に必要）
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# 手順 a: n個のランダムサンプルを作成し、各サンプルを2分割
n_samples = 10
results = []

for i in range(n_samples):
    sample_data = pd.DataFrame(data_scaled).sample(frac=0.5, replace=False, random_state=random.randint(0, 1000))
    train_data, test_data = train_test_split(sample_data, test_size=0.5)

    # train_dataとtest_dataをNumPy配列に変換
    train_data_np = train_data.to_numpy()
    test_data_np = test_data.to_numpy()

    # クラスタリング (Ward + KMeans, LPA, GMM, FCM, T-SNE + KMeans, Spectral Clustering)
    cluster_algorithms = {}

    # Ward法 + KMeans法
    Z = linkage(train_data_np, method='ward')  # Ward法で階層クラスタリング
    for k in cluster_counts:
        initial_clusters = fcluster(Z, t=k, criterion='maxclust')
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(train_data_np)
        cluster_algorithms[f'ward_kmeans_{k}'] = kmeans.predict(train_data_np)

    # 潜在プロファイル分析 (LPA) (GaussianMixtureで近似)
    for k in cluster_counts:
        gmm_lpa = GaussianMixture(n_components=k, random_state=42)
        lpa_labels = gmm_lpa.fit_predict(train_data_np)
        cluster_algorithms[f'lpa_{k}'] = lpa_labels

    # Fuzzy C-Means (FCM)
    for k in cluster_counts:
        fcm = FCM(n_clusters=k)
        fcm.fit(train_data_np)  # NumPy配列を使用
        fcm_labels = fcm.predict(train_data_np)  # FCMによる予測
        cluster_algorithms[f'fcm_{k}'] = fcm_labels

    # T-SNE + KMeans
    for k in cluster_counts:
        tsne = PCA(n_components=2, random_state=42)  # T-SNEの代わりにPCAを使用（T-SNEでも可）
        tsne_train_data = tsne.fit_transform(train_data_np)
        kmeans_tsne = KMeans(n_clusters=k, random_state=42)
        kmeans_tsne_labels = kmeans_tsne.fit_predict(tsne_train_data)
        cluster_algorithms[f'tsne_kmeans_{k}'] = kmeans_tsne_labels

    # スペクトラルクラスタリング
    for k in cluster_counts:
        spectral = SpectralClustering(n_clusters=k, random_state=42, affinity='nearest_neighbors')
        spectral_labels = spectral.fit_predict(train_data_np)
        cluster_algorithms[f'spectral_{k}'] = spectral_labels

    cluster_labels_train = cluster_algorithms
    cluster_labels_test = {}

    # テストデータにクラスタリング結果を適用
    for k in cluster_counts:
        # Ward法 + KMeans法
        cluster_labels_test[f'ward_kmeans_{k}'] = kmeans.predict(test_data_np)

        # LPA
        cluster_labels_test[f'lpa_{k}'] = gmm_lpa.predict(test_data_np)

        # FCM
        cluster_labels_test[f'fcm_{k}'] = fcm.predict(test_data_np)

        # T-SNE + KMeans
        tsne_test_data = tsne.transform(test_data_np)
        cluster_labels_test[f'tsne_kmeans_{k}'] = kmeans_tsne.predict(tsne_test_data)

        # スペクトラルクラスタリング
        cluster_labels_test[f'spectral_{k}'] = spectral.fit_predict(test_data_np)

    # 手順 c: SVMを用いて他方の半分のサンプルを再分類
    svm_results = {}
    for name, labels_train in cluster_labels_train.items():
        # クラス数が1つだけか確認し、1つの場合はスキップ
        if len(np.unique(labels_train)) > 1:
            svm = SVC()
            svm.fit(train_data_np, labels_train)
            predicted_labels = svm.predict(test_data_np)
            svm_results[name] = predicted_labels
        else:
            print(f"Skipping SVM for {name} because only one class is present in the labels.")

    # 手順 d: Cohen's kappa、Hubert-Arabieの調整済みRand指標(ARI)を計算
    for name, labels_test in cluster_labels_test.items():
        if name in svm_results:
            kappa = cohen_kappa_score(labels_test, svm_results[name])
            ari = adjusted_rand_score(labels_test, svm_results[name])
            results.append({
                'algorithm': name,
                'kappa': kappa,
                'ari': ari
            })

# 結果の平均を計算
results_df = pd.DataFrame(results)
average_results = results_df.groupby('algorithm').mean()

# 結果出力
print("外的妥当性指標の平均値:")
print(average_results)
