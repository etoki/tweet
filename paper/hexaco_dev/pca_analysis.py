import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# ステップ1: CSVファイルからデータを読み込む
# 'data.csv' を適切なファイルパスに変更してください
file_path_in = 'csv/fa_240_ch.csv'
file_path_out = 'csv/pca_res_240_ch.csv'
data = pd.read_csv(file_path_in)
data = data.drop(columns=["メールアドレス"])

# ステップ2: データの標準化
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# ステップ3: PCAの実行
pca = PCA(n_components=None)  # 全ての成分を取得
pca.fit(data_scaled)

# 固有値と累積分散割合の取得
explained_variance = pca.explained_variance_ratio_
cumulative_variance = explained_variance.cumsum()

# 固有値と累積分散割合をデータフレームとして表示
pca_results = pd.DataFrame({
    'Explained Variance': explained_variance,
    'Cumulative Variance': cumulative_variance
})

# データフレームの表示
print(pca_results)
pca_results.to_csv(file_path_out, index=True)

# # ステップ4: スクリープロットの作成
# plt.figure(figsize=(8, 6))
# plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='--')
# plt.title('Scree Plot')
# plt.xlabel('Number of Components')
# plt.ylabel('Explained Variance')
# plt.grid(True)
# plt.show()