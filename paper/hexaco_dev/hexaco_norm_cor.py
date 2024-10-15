import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# CSVファイルの読み込み
file_path = 'csv/cul_24pp.csv'
df = pd.read_csv(file_path)

# メールアドレスの列を削除
df.drop(columns=['メールアドレス'], inplace=True)

# ドメインの列名をリストとして指定
domain_columns = ['Honesty-Humility', 'Emotionality', 'Extraversion', 
                  'Agreeableness', 'Conscientiousness', 'Openness']

# 相関をピアソンにするかスピアマンにするかの判定を格納する変数
use_spearman = False

# 統計量を格納するデータフレーム
histogram_data = {}

# 正規性の確認とヒストグラム作成
plt.figure(figsize=(12, 8))  # 全体の図のサイズを設定

for i, column in enumerate(domain_columns, 1):
    # 各変数の正規性をShapiro-Wilk検定で確認
    stat, p = stats.shapiro(df[column])
    print(f'{column} のShapiro-Wilk検定結果: 統計量={stat}, p値={p}')
    if p <= 0.05:
        print(f'{column} は正規分布に従っていないと考えられます。\n')
        use_spearman = True  # 正規分布でない変数が1つでもあればスピアマンを使用
    else:
        print(f'{column} は正規分布に従っていると考えられます。\n')
    
    # ヒストグラムのデータを取得
    counts, bin_edges = np.histogram(df[column], bins=8, range=(1, 5))
    
    # データフレームに保存
    histogram_data[column] = {'ビンの範囲': [f"{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}" for i in range(len(counts))],
                               '頻度': counts}

    # 各変数のヒストグラムをサブプロットで表示
    plt.subplot(2, 3, i)  # 2行3列のサブプロット配置
    sns.histplot(df[column], bins=8, binrange=(1, 5), kde=True)  # 0.5刻みのビン、範囲を1から5まで
    plt.title(column)
    plt.xticks([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])  # X軸のラベルを0.5刻みに設定

# ヒストグラムを表示
plt.tight_layout()  # サブプロットが重ならないように調整
plt.show()

# ヒストグラムデータをデータフレームに変換
histogram_df = pd.DataFrame.from_dict(histogram_data, orient='index').reset_index()
histogram_df.columns = ['変数', 'ビンの範囲', '頻度']

# ヒストグラムの結果を表示
print(histogram_df)

# ドメインの相関行列の作成
if use_spearman:
    print("スピアマンの相関係数を使用します。")
    correlation_matrix = df[domain_columns].corr(method='spearman')
    p_value_matrix = pd.DataFrame(np.zeros((len(domain_columns), len(domain_columns))), 
                                  index=domain_columns, columns=domain_columns)
    
    for i in range(len(domain_columns)):
        for j in range(len(domain_columns)):
            _, p_value_matrix.iloc[i, j] = stats.spearmanr(df[domain_columns[i]], df[domain_columns[j]])
else:
    print("ピアソンの相関係数を使用します。")
    correlation_matrix = df[domain_columns].corr(method='pearson')
    p_value_matrix = pd.DataFrame(np.zeros((len(domain_columns), len(domain_columns))), 
                                  index=domain_columns, columns=domain_columns)

    for i in range(len(domain_columns)):
        for j in range(len(domain_columns)):
            _, p_value_matrix.iloc[i, j] = stats.pearsonr(df[domain_columns[i]], df[domain_columns[j]])

# 相関行列の表示
print(correlation_matrix)

# 相関行列をCSVに出力
correlation_matrix.to_csv('csv/correlation_matrix.csv', encoding='utf-8-sig') 

# P値行列をCSVに出力
p_value_matrix.to_csv('csv/p_value_matrix.csv', encoding='utf-8-sig')

# ヒートマップで相関行列を可視化
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('相関行列のヒートマップ')
plt.show()