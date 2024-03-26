import pandas as pd
from scipy.stats import spearmanr

data = pd.read_csv("csv/all.csv")
# data = pd.read_csv("csv/jp.csv")
# data = pd.read_csv("csv/mt.csv")
# data = pd.read_csv("csv/en.csv")
# data = pd.read_csv("csv/sc.csv")

traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
usage_items = ['Number of Lectures Watched', 'Viewing Time', 'Number of Confirmation Tests Completed', 'Number of Confirmation Tests Mastered', 'Average First Attempt Correct Answer Rate']

for trait in traits:
    for usage in usage_items:
        correlation, p_value = spearmanr(data[trait], data[usage])
        print(f"correlation coefficient between {trait}and{usage}: {correlation:.3f}, p-value: {p_value:.4f}")

