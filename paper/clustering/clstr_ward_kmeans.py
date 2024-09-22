import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# CSVファイルからデータを読み込む
# ファイルパスを適宜変更してください
file_path = 'csv/hexaco_domain.csv'
df = pd.read_csv(file_path)

# Ward法による階層型クラスタリング
linkage_matrix = linkage(df, method='ward')

# デンドログラムのプロット
plt.figure(figsize=(10, 7))
dendrogram(linkage_matrix)
plt.title('Dendrogram (Ward Method)')
plt.xlabel('Samples')
plt.ylabel('Distance')
plt.show()

# K-meansクラスタリング
# クラスター数を設定します（例: 3クラスター）
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(df)

# クラスタリング結果を表示
print(df)

# クラスタセンターを表示
print(kmeans.cluster_centers_)
