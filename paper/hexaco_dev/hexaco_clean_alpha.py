import pandas as pd
import numpy as np
import pingouin as pg

# File paths
input_csv_path = 'csv/hexaco-jp_for_cleansing_v6.csv'
output_csv_path = 'csv/hexaco-jp_facet_for_alpha_v6.csv'

# Column names
column_names = [
    'responseId', 'firstName', 'lastName', 'email', 
    'Honesty-Humility', 'Emotionality', 'Extraversion', 'Agreeableness', 'Conscientiousness', 'Openness', 
    'Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty', 
    'Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality', 
    'Expressiveness', 'Social-Boldness', 'Sociability', 'Liveliness', 
    'Forgiveness', 'Gentleness', 'Flexibility', 'Patience', 
    'Organization', 'Diligence', 'Perfectionism', 'Prudence', 
    'Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality', 
    'startTimestamp', 'endTimestamp', 'diff', 'completed', 'num'
]

# Data Cleaning Section
# Read and process the CSV file
df = pd.read_csv(input_csv_path, header=None)
df.columns = column_names

# Drop unnecessary columns
columns_to_drop = ['responseId', 'firstName', 'lastName', 'startTimestamp', 
                  'endTimestamp', 'diff', 'completed', 'num']
df.drop(columns=columns_to_drop, inplace=True)

# Remove specific email addresses
df = df[~df['email'].isin(['jay@amegumi.com', 'sub.ashuman@gmail.com'])]
df.drop(columns="email", inplace=True)

# Convert non-numeric data to numeric
df.replace('\\N', np.nan, inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')

# Define column groups
domain_columns = [
    'Honesty-Humility', 'Emotionality', 'Extraversion', 
    'Agreeableness', 'Conscientiousness', 'Openness'
]

facet_columns = [
    'Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty',
    'Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality',
    'Expressiveness', 'Social-Boldness', 'Sociability', 'Liveliness',
    'Forgiveness', 'Gentleness', 'Flexibility', 'Patience',
    'Organization', 'Diligence', 'Perfectionism', 'Prudence',
    'Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality'
]

# Create separate DataFrames
facet_df = df[facet_columns]
facet_df.to_csv(output_csv_path, index=False)

# Cronbach's Alpha Calculation Section
def cronbach_alpha(df):
    item_variances = df.var(axis=0, ddof=1)
    total_variance = df.sum(axis=1).var(ddof=1)
    n_items = df.shape[1]
    alpha = (n_items / (n_items - 1)) * (1 - (item_variances.sum() / total_variance))
    return alpha

# Define domain facets
domain_facets = {
    "Honesty-Humility": ['Sincerity', 'Fairness', 'Greed-Avoidance', 'Modesty'],
    "Emotionality": ['Fearfulness', 'Anxiety', 'Dependence', 'Sentimentality'],
    "Extraversion": ['Expressiveness', 'Social-Boldness', 'Sociability', 'Liveliness'],
    "Agreeableness": ['Forgiveness', 'Gentleness', 'Flexibility', 'Patience'],
    "Conscientiousness": ['Organization', 'Diligence', 'Perfectionism', 'Prudence'],
    "Openness to Experience": ['Aesthetic-Appreciation', 'Inquisitiveness', 'Creativity', 'Unconventionality']
}

# Calculate Cronbach's alpha for each domain
domain_alpha_values = {}
for domain, facets in domain_facets.items():
    df_subset = facet_df[facets]
    alpha_value = cronbach_alpha(df_subset)
    domain_alpha_values[domain] = alpha_value
    print(f"{domain}のクロンバックのα係数: {alpha_value}")

# Calculate overall Cronbach's alpha
df_all_domains = pd.concat([facet_df[facets] for facets in domain_facets.values()], axis=1)
overall_alpha_value = cronbach_alpha(df_all_domains)
print(f"\nドメイン全体のクロンバックのα係数: {overall_alpha_value}")