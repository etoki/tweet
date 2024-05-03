import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_machinary_order_data = pd.read_csv("csv/machinary_order_data.csv")
df_stock = pd.read_csv("csv/stockdata.csv")

df_machinary_order_data.set_index('date', inplace=True)
df_stock.set_index('date', inplace=True)

df_oiriginal = df_machinary_order_data
print(df_oiriginal)

# df = df_stock
# for column in df.columns:
#     plt.figure(figsize=(8, 5))
#     plt.plot(df.index, df[column])
#     plt.title(column)
#     plt.xlabel('Date')
#     plt.ylabel('Value')
#     plt.grid(True)
#     plt.show()

# Pneumatic_and_hydraulic_equipment
df_oiriginal["風水力機械"] = np.log10(df_oiriginal["風水力機械"]).diff()
# materialshandling_machinery
df_oiriginal["運搬機械"] = np.log10(df_oiriginal["運搬機械"]).diff()
# Industrial_robots
df_oiriginal["産業用ロボット"] = np.log10(df_oiriginal["産業用ロボット"]).diff()
# Metal_working_machinery
df_oiriginal["金属加工機械"] = np.log10(df_oiriginal["金属加工機械"]).diff()
# Refrigerating_machines
df_oiriginal["冷凍機械"] = np.log10(df_oiriginal["冷凍機械"]).diff()
# Plastics_processing_machines
df_oiriginal["合成樹脂加工機械"] = np.log10(df_oiriginal["合成樹脂加工機械"]).diff()
# stock
df_oiriginal["日経平均株価"] = np.log10(df_stock["日経平均株価"]).diff()
print(df_oiriginal.drop(df_oiriginal.index[0]).T)
