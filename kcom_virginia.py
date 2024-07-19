import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSVファイルを読み込む
data = pd.read_csv('csv/kcom_virginia.csv')

# 日付をDateTime型に変換
data['date'] = pd.to_datetime(data['date'])

# print(data)

# 口コミ投稿件数と予約件数のラグ相関を計算する
correlations = []
lags = range(0, 12)  # 最大ラグ11（110日分）

for lag in lags:
    shifted_reviews = data['gbp_post'].shift(lag)
    correlation = data['reservation'].corr(shifted_reviews)
    correlations.append(correlation)

# print(correlations)

# ラグと相関のリストをフィルタリング（NaNを除外）
filtered_lags = [lag for lag, corr in zip(lags, correlations) if not np.isnan(corr)]
filtered_correlations = [corr for corr in correlations if not np.isnan(corr)]

# デバッグ用にラグと相関のリストを出力
print("Filtered Lags:", filtered_lags)
print("Filtered Correlations:", filtered_correlations)

# グラフを描画する
plt.figure(figsize=(10, 6))
plt.plot(filtered_lags, filtered_correlations, marker='o', linestyle='-', color='b')
plt.title('Correlation of Reviews with Reservations Over Time (10-day Intervals, Up to 110 Days)')
plt.xlabel('Lags in 10-day Intervals')
plt.ylabel('Correlation Coefficient')
plt.grid(True)
plt.ylim(0.0, 0.8)  # Set y-axis limit from 0.3 to 0.8
plt.xticks(filtered_lags, [f'{x*10}' for x in filtered_lags])  # Label x-axis with numbers only

# Annotate data labels for each point
for i, txt in enumerate(filtered_correlations):
    plt.annotate(f'{txt:.2f}', (filtered_lags[i], filtered_correlations[i] + 0.02), textcoords="offset points", xytext=(0, 10), ha='center')

# Add a smoothing line using a polynomial fit
if len(filtered_lags) > 0 and len(filtered_correlations) > 0:
    z = np.polyfit(filtered_lags, filtered_correlations, 3)
    p = np.poly1d(z)
    plt.plot(filtered_lags, p(filtered_lags), "r--")

plt.axhline(0.6, color='red', linestyle='--')  # Add a horizontal red dashed line at y = 0.6
plt.savefig('pic/kcom_virginia_correlation_plot.png')
plt.show()