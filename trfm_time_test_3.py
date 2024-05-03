import pandas as pd
import numpy as np
import torch
import optuna
import time
from iTransformer import iTransformer
import matplotlib.pyplot as plt

# データの読み込み
machinary_order_data = pd.read_csv('csv/machinary_order_data.csv')
stock_data = pd.read_csv('csv/stockdata.csv')

# 日付をインデックスとして設定
machinary_order_data['date'] = pd.to_datetime(machinary_order_data['date'])
machinary_order_data.set_index('date', inplace=True)

stock_data['date'] = pd.to_datetime(stock_data['date'])
stock_data.set_index('date', inplace=True)

# print(machinary_order_data)
# print(stock_data)

# # 2005年4月～2023年8月のデータを選択
# machinary_order_data = machinary_order_data.loc['2005-04-01':'2023-08-01']
# stock_data = stock_data.loc['2005-04-01':'2023-08-01']

# 使用するデータの選択
df_oiriginal = machinary_order_data[['産業用ロボット', '風水力機械', '運搬機械', '金属加工機械', '冷凍機械', '合成樹脂加工機械']]
df_oiriginal['日経平均株価'] = stock_data['日経平均株価']
# print(df_oiriginal)

# データの前処理
for column in df_oiriginal.columns:
    df_oiriginal[column + "対数化"] = np.log10(df_oiriginal[column]).diff()
# print(df_oiriginal)1

months = df_oiriginal.columns[1:]
df_oiriginal = df_oiriginal[months]

# # iTransformer用のテンソル配列作成関数
# def Make_iTransformer_data(df_use, start_index, end_index):
#     df_target = df_use.iloc[start_index:end_index].T
#     np_target = df_target.to_numpy()
#     timeseries_data = torch.tensor(np_target)
#     timeseries_data = timeseries_data.repeat(1, 1, 1)
#     reslut_data = timeseries_data.to(torch.float32)
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     reslut_data = reslut_data.to(device)
#     return reslut_data

# # 訓練データの作成
# train1_data = Make_iTransformer_data(df_oiriginal, 0, 36)
# train2_data = Make_iTransformer_data(df_oiriginal, 36, 72)
# train3_data = Make_iTransformer_data(df_oiriginal, 72, 108)
# train4_data = Make_iTransformer_data(df_oiriginal, 108, 144)
# train5_data = Make_iTransformer_data(df_oiriginal, 144, 180)
# train6_data = Make_iTransformer_data(df_oiriginal, 180, 216)

# train_data = torch.cat((train1_data, train2_data, train3_data, train4_data, train5_data, train6_data), dim=0)

# # 予測の階差を用いた実際の対数値のフレームの更新関数
# def Make_dfdiff_reverse(df_ori, df_diff):
#     rows, columns = df_ori.shape
#     df_result = df_ori.copy()
#     for i in range(0, rows):
#         before_term = df_ori.iloc[i, 0]
#         for j in range(1, columns):
#             df_result.iloc[i, j] = before_term + df_diff.iloc[i, j-1]
#             before_term = df_result.iloc[i, j]
#     return df_result

# # パラメータ探索関数
# def iTransformer_params(train, df_ori, valid_terms):
#     def objective(trial):
#         params = {
#             'num_variates': 7,
#             'lookback_len': 36,
#             'dim': trial.suggest_int('dim', 250, 350),
#             'depth': trial.suggest_int('depth', 1, 20),
#             'heads': trial.suggest_int('heads', 1, 20),
#             'dim_head': trial.suggest_int('dim_head', 8, 32),
#             'pred_length': 2,
#             'num_tokens_per_variate': trial.suggest_int('num_tokens_per_variate', 2, 25)
#         }

#         itrans_model = iTransformer(
#             num_variates=params['num_variates'],
#             lookback_len=params['lookback_len'],
#             dim=params['dim'],
#             depth=params['depth'],
#             heads=params['heads'],
#             dim_head=params['dim_head'],
#             pred_length=params['pred_length'],
#             num_tokens_per_variate=params['num_tokens_per_variate']
#         )

#         itrans_preds = itrans_model(train)

#         for key, value in itrans_preds.items():
#             pred_tensor = torch.tensor(value)
#             pred_MAEtensor = pred_tensor.transpose(1, 2)

#         batch_count, graph_count, pred_step_count = pred_MAEtensor.shape

#         index_lists = df_ori.index
#         sumABS = 0.0

#         for b in range(0, batch_count):
#             pred_arr = pred_MAEtensor[b].numpy()
#             start_months_index, end_months_index = valid_terms[b]
#             df_result = pd.DataFrame(data=pred_arr, index=index_lists[start_months_index+1:end_months_index], columns=df_ori.columns)

#             df_valid = df_ori.iloc[start_months_index:end_months_index]
#             df_test = Make_dfdiff_reverse(df_valid, df_result)

#             for g in range(0, graph_count):
#                 for ps in range(0, pred_step_count):
#                     sumABS += np.abs(df_valid.iloc[g, ps+1] - df_test.iloc[g, ps])

#         return sumABS / (batch_count * graph_count * pred_step_count)

#     return objective

# # パラメータの最適値探索関数
# def optuna_parameter(train, df_ori, valid_terms):
#     study = optuna.create_study(sampler=optuna.samplers.RandomSampler(seed=42))
#     study.optimize(iTransformer_params(train, df_ori, valid_terms), n_trials=1800, timeout=610)
#     optuna_best_params = study.best_params
#     return study

# # 最適パラメータの探索
# valid_terms = [
#     [36, 39],  # 2008年4月～6月
#     [72, 75],  # 2011年4月～6月
#     [108, 111],  # 2014年4月～7月
#     [144, 147],  # 2017年4月～6月
#     [180, 183],  # 2020年4月～6月
#     [216, 219]  # 2023年4月～6月
# ]

# optuna_count = 9
# best_values = 99999999
# start_time = time.time()

# for i in range(0, optuna_count):
#     study = optuna_parameter(train_data, df_oiriginal, valid_terms)
#     now_deal_time = time.time() - start_time
#     if study.best_value < best_values:
#         best_params = study.best_params
#         best_values = study.best_value
#     print("----------------------------------------")
#     print("optimize count", str(i + 1))
#     print("best_params : ", best_params)
#     print("best_values : ", best_values)
#     print("----------------------------------------")
#     if 2400 <= now_deal_time:
#         print("----------------------------------------")
#         print("optimize count", str(i + 1))
#         print("best_params : ", best_params)
#         print("best_values : ", best_values)
#         print("----------------------------------------")
#         break

# # 予測時使用データの作成
# train1_data = Make_iTransformer_data(df_oiriginal, 2, 38)
# train2_data = Make_iTransformer_data(df_oiriginal, 38, 74)
# train3_data = Make_iTransformer_data(df_oiriginal, 74, 110)
# train4_data = Make_iTransformer_data(df_oiriginal, 110, 146)
# train5_data = Make_iTransformer_data(df_oiriginal, 146, 182)
# train6_data = Make_iTransformer_data(df_oiriginal, 182, 218)

# pred_train_data = torch.cat((train1_data, train2_data, train3_data, train4_data, train5_data, train6_data), dim=0)

# # モデルの実装
# itrans_model = iTransformer(
#     num_variates=7,
#     lookback_len=36,
#     dim=best_params['dim'],
#     depth=best_params['depth'],
#     heads=best_params['heads'],
#     dim_head=best_params['dim_head'],
#     num_tokens_per_variate=best_params['num_tokens_per_variate'],
#     pred_length=2
# )

# # モデルの適用
# itrans_preds = itrans_model(pred_train_data)

# # 予測値の格納
# for key, value in itrans_preds.items():
#     pred_MAEtensor = torch.tensor(value)

# # 2023年7月と8月の予測値の取得
# print(pred_MAEtensor[5])