import pandas as pd
from scipy.stats import spearmanr

data = pd.read_csv("csv/dt_all.csv")
# data = pd.read_csv("csv/dt_jp.csv")
# data = pd.read_csv("csv/dt_mt.csv")
# data = pd.read_csv("csv/dt_en.csv")
# data = pd.read_csv("csv/dt_sc.csv")

traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
usage_items = ['NumberOfLecturesWatched', 'ViewingTime', 'NumberOfConfirmationTestsCompleted', 'NumberOfConfirmationTestsMastered', 'AverageFirstAttemptCorrectAnswerRate']

for trait in traits:
    for usage in usage_items:
        correlation, p_value = spearmanr(data[trait], data[usage])
        print(f"correlation coefficient between {trait}and{usage}: {correlation:.3f}, p-value: {p_value:.4f}")

