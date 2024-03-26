library(dplyr)
library(readr)

data <- read_csv("csv/all.csv")
# data <- read_csv("csv/jp.csv")
# data <- read_csv("csv/mt.csv")
# data <- read_csv("csv/en.csv")
# data <- read_csv("csv/sc.csv")

traits <- c("Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism")
usage_items <- c("Number of Lectures Watched", "Viewing Time", "Number of Confirmation Tests Completed",
                 "Number of Confirmation Tests Mastered", "Average First Attempt Correct Answer Rate")

for (trait in traits) {
  for (usage in usage_items) {
    correlation <- cor.test(data[[trait]], data[[usage]], method = "spearman")
    cat(sprintf("correlation coefficient between %s and %s: %.3f, p-value: %.4f\n",
                trait, usage, correlation$estimate, correlation$p.value))
  }
}