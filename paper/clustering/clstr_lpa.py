import pandas as pd
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

# データの読み込み
file_path = 'csv/hexaco_domain.csv'
df = pd.read_csv(file_path)

# 潜在プロファイル分析（Gaussian Mixture Modelを使用）
n_profiles = 7  # 潜在プロファイル数は必要に応じて変更してください
gmm = GaussianMixture(n_components=n_profiles, covariance_type='full', random_state=42)
gmm.fit(df)

# 潜在プロファイルの割り当て
df['profile'] = gmm.predict(df)

# 結果の表示
print(df)

# 各変数ごとの潜在プロファイル平均を計算
profile_means = df.groupby('profile').mean()
print(profile_means)

# 結果の可視化（各プロファイルごとの特性の平均値を棒グラフで表示）
profile_means.T.plot(kind='bar')
plt.title('Profile Means by HEXACO Dimensions')
plt.ylabel('Mean Score')
plt.xlabel('HEXACO Dimensions')
plt.xticks(rotation=45)
plt.legend(title='Profile', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
