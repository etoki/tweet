# Structural Equation Modeling
import pandas as pd
from sklearn.preprocessing import StandardScaler
import semopy as sem
from semopy import Model

data = pd.read_csv("csv/raw_studysapuri.csv")

data_all = data[data['category'] == 'all']

columns_to_keep = ['NumberOfLecturesWatched', 'ViewingTime', 'NumberOfConfirmationTestsCompleted', 
                   'NumberOfConfirmationTestsMastered', 'AverageFirstAttemptCorrectAnswerRate', 
                #    'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism', 
                   'IntellectualCuriosity', 'AestheticSensitivity', 'CreativeImagination', 
                   'Organization', 'Productiveness', 'Responsibility', 
                   'Sociability', 'Assertiveness', 'EnergyLevel', 
                   'Compassion', 'Respectfulness', 'Trust', 
                   'Anxiety', 'Depression', 'EmotionalVolatility']
data_all = data_all[columns_to_keep]

scaler = StandardScaler()
data_all_scaled = scaler.fit_transform(data_all)

data_all_scaled = pd.DataFrame(data_all_scaled, columns=columns_to_keep)

# print(data_all_scaled)

mod = '''
    # Measurement Equation
    f1 =~ IntellectualCuriosity + AestheticSensitivity + CreativeImagination
    f2 =~ Organization + Productiveness + Responsibility
    f3 =~ Sociability + Assertiveness
    f4 =~ EnergyLevel
    f5 =~ Compassion + Respectfulness + Trust
    f6 =~ Anxiety + Depression + EmotionalVolatility

    # Structural Equation
    f1 ~ NumberOfConfirmationTestsCompleted + NumberOfConfirmationTestsMastered
    f2 ~ NumberOfConfirmationTestsCompleted + NumberOfConfirmationTestsMastered
    f3 ~ NumberOfLecturesWatched
    f4 ~ NumberOfLecturesWatched + AverageFirstAttemptCorrectAnswerRate
    f5 ~ IntellectualCuriosity + AestheticSensitivity + CreativeImagination
    f6 ~ Anxiety + Depression + EmotionalVolatility

    # Covariance Relationship
    f1 ~~ f2
    f2 ~~ f3
    f3 ~~ f4
    f4 ~~ f5
    f5 ~~ f6
    '''

mod = sem.Model(mod)
res = mod.fit(data=data, obj='MLW')

inspect = sem.Model.inspect(mod, std_est=True)
print(inspect)
stats = sem.calc_stats(mod)
print(stats.T)

# g = sem.semplot(mod, "sem_studysapuri.png", plot_covs=True, std_ests=True, show=True)

