# Structural Equation Modeling
import pandas as pd
from sklearn.preprocessing import StandardScaler
import semopy as sem

data = pd.read_csv("csv/raw_studysapuri.csv")

columns_to_keep = ['NumberOfLecturesWatched', 'ViewingTime', 'NumberOfConfirmationTestsCompleted', 
                   'NumberOfConfirmationTestsMastered', 'AverageFirstAttemptCorrectAnswerRate', 
                   'IntellectualCuriosity', 'AestheticSensitivity', 'CreativeImagination', 
                   'Organization', 'Productiveness', 'Responsibility', 
                   'Sociability', 'Assertiveness', 'EnergyLevel', 
                   'Compassion', 'Respectfulness', 'Trust', 
                   'Anxiety', 'Depression', 'EmotionalVolatility']

scaler = StandardScaler()
categories = ['all', 'ja', 'mt', 'en', 'sc']
scaled_data = {}

for cat in categories:
    filtered_data = data[data['category'] == cat][columns_to_keep]
    scaled_data[cat] = pd.DataFrame(scaler.fit_transform(filtered_data), columns=columns_to_keep)
    scaled_data[cat].columns = ['y1','y2','y3','y4','y5','o1','o2','o3','c1','c2','c3','e1','e2','e3','a1','a2','a3','n1','n2','n3']

# 各カテゴリに対するモデルの定義
models = {
    'all': '''
        f1 =~ e1 + a2 + a3
        f2 =~ c1 + c2 + c3 + e2
        f3 =~ o1 + o2 + o3 + n1 + n2 + n3

        f1 ~ f3
        f2 ~ f3
    ''',
    'ja': '''
        f1 =~ y3 + y4
        f2 =~ y5

        f3 =~ c1 + c2 + c3 + e2

        f1 ~ f3
        f2 ~ f3
    ''',
    'mt': '''
        f1 =~ y3 + y4
        f2 =~ y1 + y2

        f3 =~ c1 + c2 + c3 + e2 + a2
        f4 =~ e1 + n1

        f1 ~ f3
        f2 ~ f4
    ''',
    'en': '''
        f1 =~ y3 + y4 + y5
        f2 =~ y1 + y2

        f3 =~ c1 + c2 + c3 + n1
        f4 =~ e1 + a3 + n1

        f1 ~ f3
        f2 ~ f4
    ''',
    'sc': '''
        f1 =~ y3 + y4
        f2 =~ y1 + y2

        f3 =~ c1 + c2 + c3
        f4 =~ a2 + a3

        f1 ~ f3
        f2 ~ f4
    '''
}

# モデルのフィットと結果の保存
results = {}
for cat, mod_str in models.items():
    mod = sem.Model(mod_str)
    results[cat] = mod.fit(data=scaled_data[cat], obj='MLW')
    sem.Model.inspect(mod, std_est=True).to_csv(f"csv/inspection_results_{cat}.csv")
    sem.semplot(mod, f"pic/sem_studysapuri_{cat}.png", plot_covs=True, std_ests=True, show=True)

    stats = sem.calc_stats(mod)
    stats_df = pd.DataFrame(stats.T)
    stats_df.to_csv(f"csv/stats_results_{cat}.csv")