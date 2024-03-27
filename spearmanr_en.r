library(readr)
library(dplyr)
library(tidyr)
library(psych)

# データを読み込む
data <- read_csv("csv/raw_studysapuri.csv")

# カテゴリごとにデータを分割
data_all <- filter(data, category == "all") %>% select(-category)
data_ja <- filter(data, category == "ja") %>% select(-category)
data_mt <- filter(data, category == "mt") %>% select(-category)
data_en <- filter(data, category == "en") %>% select(-category)
data_sc <- filter(data, category == "sc") %>% select(-category)

# 相関係数とp値を計算してCSVに保存する関数
save_correlation_to_csv <- function(traits, usage_items, data, filename) {
  results <- data.frame()
  for (trait in traits) {
    for (usage in usage_items) {
      result <- cor.test(data[[trait]], data[[usage]], method="spearman")
      results <- rbind(results, c(trait, usage, result$estimate, result$p.value))
    }
  }
  colnames(results) <- c('personality', 'item', 'correlation', 'p_value')
  write.csv(results, file=filename, row.names=FALSE)
}

# CSVに保存
save_correlation_to_csv(traits, usage_items, data_all, 'csv/correlation_all.csv')
save_correlation_to_csv(traits, usage_items, data_ja,  'csv/correlation_ja.csv')
save_correlation_to_csv(traits, usage_items, data_mt,  'csv/correlation_mt.csv')
save_correlation_to_csv(traits, usage_items, data_en,  'csv/correlation_en.csv')
save_correlation_to_csv(traits, usage_items, data_sc,  'csv/correlation_sc.csv')
