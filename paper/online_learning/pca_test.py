import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# データの読み込みと前処理
data = pd.read_csv("csv/raw_studysapuri.csv")
data = data[data['category'] == 'mt'].drop('category', axis=1)
features = ['Conscientiousness', 'Agreeableness', 'Neuroticism', 'Openness', 'Extraversion']
x = data[features]
x = x.dropna()

# データの標準化
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# PCAの実行
pca = PCA(n_components=3)
principal_components = pca.fit_transform(x_scaled)

# PCA結果のデータフレーム化
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2', 'PC3'])
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
loadings_df = pd.DataFrame(data=loadings, columns=['PC1', 'PC2', 'PC3'], index=features)

print("Explained Variance Ratio:", pca.explained_variance_ratio_)
print("Explained Variance:",       pca.explained_variance_)
print("Singular Values:",          pca.singular_values_)
print("Mean of Features:",         pca.mean_)
print("Noise Variance:",           pca.noise_variance_)
print("Number of Components:",     pca.n_components_)
print("Number of Features:",       pca.n_features_in_)
print("Number of Samples:",        pca.n_samples_)
print("loadings:\n",               loadings_df)

loadings_df.to_csv('csv/pca_loadings.csv')