# Structural Equation Modeling
import pandas as pd
from sklearn.preprocessing import StandardScaler
import semopy as sem
from semopy import Model

data = pd.read_csv("csv/raw_studysapuri.csv")

data_all = data[data['category'] == 'all']
data_ja  = data[data['category'] == 'ja']
data_mt  = data[data['category'] == 'mt']
data_en  = data[data['category'] == 'en']
data_sc  = data[data['category'] == 'sc']

columns_to_keep = ['NumberOfLecturesWatched', 'ViewingTime', 'NumberOfConfirmationTestsCompleted', 
                   'NumberOfConfirmationTestsMastered', 'AverageFirstAttemptCorrectAnswerRate', 
                #    'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism', 
                   'IntellectualCuriosity', 'AestheticSensitivity', 'CreativeImagination', 
                   'Organization', 'Productiveness', 'Responsibility', 
                   'Sociability', 'Assertiveness', 'EnergyLevel', 
                   'Compassion', 'Respectfulness', 'Trust', 
                   'Anxiety', 'Depression', 'EmotionalVolatility']
data_all = data_all[columns_to_keep]
data_ja  = data_ja[columns_to_keep]
data_mt  = data_mt[columns_to_keep]
data_en  = data_en[columns_to_keep]
data_sc  = data_sc[columns_to_keep]

scaler = StandardScaler()
data_all_scaled = scaler.fit_transform(data_all)
data_ja_scaled = scaler.fit_transform(data_ja)
data_mt_scaled = scaler.fit_transform(data_mt)
data_en_scaled = scaler.fit_transform(data_en)
data_sc_scaled = scaler.fit_transform(data_sc)

data_all_scaled = pd.DataFrame(data_all_scaled, columns=columns_to_keep)
data_ja_scaled = pd.DataFrame(data_ja_scaled, columns=columns_to_keep)
data_mt_scaled = pd.DataFrame(data_mt_scaled, columns=columns_to_keep)
data_en_scaled = pd.DataFrame(data_en_scaled, columns=columns_to_keep)
data_sc_scaled = pd.DataFrame(data_sc_scaled, columns=columns_to_keep)

data_all_scaled.columns = ['y1','y2','y3','y4','y5',
                           'o1','o2','o3','c1','c2','c3',
                           'e1','e2','e3','a1','a2','a3','n1','n2','n3']
data_ja_scaled.columns = ['y1','y2','y3','y4','y5',
                           'o1','o2','o3','c1','c2','c3',
                           'e1','e2','e3','a1','a2','a3','n1','n2','n3']
data_mt_scaled.columns = ['y1','y2','y3','y4','y5',
                           'o1','o2','o3','c1','c2','c3',
                           'e1','e2','e3','a1','a2','a3','n1','n2','n3']
data_en_scaled.columns = ['y1','y2','y3','y4','y5',
                           'o1','o2','o3','c1','c2','c3',
                           'e1','e2','e3','a1','a2','a3','n1','n2','n3']
data_sc_scaled.columns = ['y1','y2','y3','y4','y5',
                           'o1','o2','o3','c1','c2','c3',
                           'e1','e2','e3','a1','a2','a3','n1','n2','n3']

# print(data_all_scaled.columns)

mod_all = '''
    f1 =~ y1 + y2
    f2 =~ y3 + y4 + y5
    f3 =~ c1 + c2 + c3
    f4 =~ n1 + n2 + n3

    f1 ~ f3 + f4
    f2 ~ f3 + f4

    f3 ~~ f4
    '''

mod_ja = '''
    f1 =~ y3 + y4 + y5
    f2 =~ c1 + c2 + c3
    f3 =~ e2

    f1 ~ f2 + f3
    f2 ~~ f3
    '''

mod_mt = '''
    f1 =~ y1 + y2
    f2 =~ y3 + y4 + y5
    f3 =~ c1 + c2 + c3
    f4 =~ e1 + a2 + n1  # Sociability, Respectfulness, Anxiety

    f1 ~ f4
    f2 ~ f3 + f4
    f3 ~~ f4
    '''

mod_en = '''
    f1 =~ y1 + y2
    f2 =~ y3 + y4 + y5
    f3 =~ c1 + c2 + c3
    f4 =~ n1 + e1 + a3

    f1 ~ f3 + f4
    f2 ~ f3 + f4
    f4 ~~ f3
    '''

mod_sc = '''
    f1 =~ y1 + y2
    f2 =~ y3 + y4 + y5
    f3 =~ c1 + c2 + c3
    f4 =~ a2 + a3

    f1 ~ f4
    f2 ~ f3
    f3 ~~ f4
    '''

mod_all = sem.Model(mod_all)
mod_ja = sem.Model(mod_ja)
mod_mt = sem.Model(mod_mt)
mod_en = sem.Model(mod_en)
mod_sc = sem.Model(mod_sc)

res_all = mod_all.fit(data=data_all_scaled, obj='MLW')
res_ja = mod_all.fit(data=data_ja_scaled, obj='MLW')
res_mt = mod_all.fit(data=data_mt_scaled, obj='MLW')
res_en = mod_all.fit(data=data_en_scaled, obj='MLW')
res_cs = mod_all.fit(data=data_sc_scaled, obj='MLW')

inspect_all = sem.Model.inspect(mod_all, std_est=True)
inspect_ja = sem.Model.inspect(mod_ja, std_est=True)
inspect_mt = sem.Model.inspect(mod_mt, std_est=True)
inspect_en = sem.Model.inspect(mod_en, std_est=True)
inspect_sc = sem.Model.inspect(mod_sc, std_est=True)
# print(inspect)
inspect_all.to_csv("csv/inspection_results_all.csv")
inspect_ja.to_csv("csv/inspection_results_ja.csv")
inspect_mt.to_csv("csv/inspection_results_mt.csv")
inspect_en.to_csv("csv/inspection_results_en.csv")
inspect_sc.to_csv("csv/inspection_results_sc.csv")

stats = sem.calc_stats(mod_all)
print(stats.T)

g = sem.semplot(mod_all, "sem_studysapuri_all.png", plot_covs=True, std_ests=True, show=True)
g = sem.semplot(mod_ja, "sem_studysapuri_ja.png", plot_covs=True, std_ests=True, show=True)
g = sem.semplot(mod_mt, "sem_studysapuri_mt.png", plot_covs=True, std_ests=True, show=True)
g = sem.semplot(mod_en, "sem_studysapuri_en.png", plot_covs=True, std_ests=True, show=True)
g = sem.semplot(mod_sc, "sem_studysapuri_sc.png", plot_covs=True, std_ests=True, show=True)


