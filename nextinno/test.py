import pandas as pd

qs = pd.read_csv('csv/qs_processed.csv', low_memory=False)

row_count = len(qs)
print("データの行数:", row_count)
# 2758846


total_amount = qs['請求金額_raw'].sum()
print("請求金額_rawの合計:", total_amount)
# 13407519062

course_sum = qs.groupby('処方コース')['請求金額_raw'].sum()
print("処方コースごとの請求金額_rawの合計:")
print(course_sum)

# 1ヶ月            539030212
# 3ヶ月            570439044
# その他             17938845
# その他（感染症）           17700
# クロスセル            3498710
# ダイエット単発1ヶ月        649860
# ダイエット定期1ヶ月       5029840
# ダイエット定期3ヶ月        881780
# 中用量            617164350
# 安心定期          3153249851
# 安心定期12ヶ月      2608019860
# 安心定期1ヶ月       2368756874
# 安心定期3ヶ月       1311934138
# 特典                     0
# 緊急避妊          1735962368
# 診察代            474931990


# 上から1行を取得
first_row = qs.iloc[0]
print("CSVの上から1行目:")
print(first_row)
