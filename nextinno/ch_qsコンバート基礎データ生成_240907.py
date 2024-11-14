#ライブラリのインポート
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import csv
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

#QSデータの読み込み
# qs1 = pd.read_csv('csv/qs1907-2112.csv' ,low_memory=False)
# qs2 = pd.read_csv('csv/qs2201-2212.csv' ,low_memory=False)
# qs3 = pd.read_csv('csv/qs2301-2312.csv' ,low_memory=False)
# qs4 = pd.read_csv('csv/qs2401-2412.csv' ,low_memory=False)
# qs = pd.concat([qs1, qs2, qs3, qs4])
# qs.to_csv('csv/qs_concat.csv', index=False, encoding='utf-8-sig')
# qs = pd.read_csv('csv/qs_concat.csv' ,low_memory=False)

# qs1 = pd.read_csv('csv/m1907-2112.csv' ,low_memory=False)
# qs2 = pd.read_csv('csv/m2201-2212.csv' ,low_memory=False)
# qs3 = pd.read_csv('csv/m2301-2312.csv' ,low_memory=False)
# qs4 = pd.read_csv('csv/m2401-2412.csv' ,low_memory=False)
# qs = pd.concat([qs1, qs2, qs3, qs4])
# qs.to_csv('csv/m_concat.csv', index=False, encoding='utf-8-sig')
qs = pd.read_csv('csv/m_concat.csv' ,low_memory=False)


# course_sum = qs.groupby('処方コース')['請求金額'].sum()
# print("処方コースごとの請求金額の合計:")
# print(course_sum)


# 生年月日のカラムを削除
# qs.drop('生年月日', axis=1, inplace=True)


# NaNを0に置き換える
qs['for biz 企業負担割合(%)'] = qs['for biz 企業負担割合(%)'].fillna(0)
qs['for biz 企業負担額'] = qs['for biz 企業負担額'].fillna(0)

#日付列をDateTimeオブジェクトに変換（念のため）
# qs['請求日'] = pd.to_datetime(qs['請求日'], errors='coerce')
qs['出荷日時'] = pd.to_datetime(qs['出荷日時'], errors='coerce')

#データをユーザーidと請求日で昇順に並び替え
# qs = qs.sort_values(by=['ユーザーid','請求日'],ascending=[True,True])

# カラム名を変更して再表示
qs.rename(columns={
                'キャンペーン値引額': '値引キャンペーン_税込', 
                'クーポン値引額': '値引クーポン_税込', 
                '配送先_都道府県': '配送先 都道府県', 
                '払い戻し日時': '払戻日時', 
                'sku_処方名': '処方薬',  
                '05_コース分類_5': '処方コース', 
                '担当医_氏名': '担当ドクター', 
                '担当医_クリニック_医療法人名': '医療法人名', 
                '担当医id': 'ドクターid', 
                '担当医_クリニックid': 'クリニックid',  
                '出荷回数/全体': '出荷回数/全体', 
                '値引分加算gmv_税抜き価格': 'GMV薬代_税抜', 
                '請求金額': '請求金額_raw', 
                '支払い方法': '支払方法', 
                '企業名': 'for biz 企業名'},  
                inplace=True)

# ピル種類が「特典」のレコードを表示するクエリ
special_pill_type = qs[qs['ピル種類'] == '特典']

# 新しいカラムに初期値0を設定して表示
qs['GMV計_税抜'] = 0
qs['GMV診察代_税抜'] = 0
qs['値引キャンペーン_税抜'] = 0
qs['値引クーポン_税抜'] = 0
qs['値引特典_税抜'] = 0
qs['請求金額_税抜'] = 0
qs['GMV計_税込'] = 0
qs['GMV薬代_税込'] = 0
qs['GMV診察代_税込'] = 0
qs['値引特典_税込'] = 0
qs['請求金額_税込'] = 0

# '支払方法' 列のNaNを 'クーポン払い' で置き換える
qs['支払方法'] = qs['支払方法'].fillna('クーポン払い')

#データがユニークであることの宣言（エラー回避のため）
if not qs.index.is_unique:
    qs = qs.reset_index(drop=True)

#「請求回数/処方」が1の場合は診察有「1」に、それ以外を診察なし「0」に分類
qs['診察'] = np.where(qs['請求回数/処方'] == 1, 1, 0)

# 特典フラグの設定
# 'コース分類4'が'特典'の請求idをリストとして取得
bonus_ids = qs[qs['コース分類4'] == '特典']['請求id'].unique()

# 新しいカラム「特典」を0で初期化
qs['特典'] = 0

# 特典の請求idを持つレコードに対してフラグを1に設定
qs.loc[qs['請求id'].isin(bonus_ids), '特典'] = 1

#「出荷回数/全体」が1の場合は1フラグを付与
qs['新規'] = np.where(qs['出荷回数/全体'] == 1, 1, 0)

#「新規」に1のフラグが立っているレコードについて、「出荷日時」を新しい「初診年月日」カラムにコピー
qs.loc[qs['新規'] == 1, '初診年月日'] = qs['出荷日時']

# '出荷回数/全体' が 1 であるレコードを取得して、'ユーザーid' に基づいて '初診年月日' をマップする準備をする
# drop_duplicates() は、同じ 'ユーザーid' に対して複数のエントリがある場合に、最初のものだけを保持する
first_visit_map = qs[qs['出荷回数/全体'] == 1].drop_duplicates('ユーザーid').set_index('ユーザーid')['初診年月日']

# 'ユーザーid' を使って '初診年月日' をマッピングし、'出荷回数/全体' が 1 でないレコードのみを更新する
# .loc を使って指定することで、Pandasに対して意図的な代入操作であることを明示する
qs.loc[qs['出荷回数/全体'] != 1, '初診年月日'] = qs.loc[qs['出荷回数/全体'] != 1, 'ユーザーid'].map(first_visit_map)

# 年月のみを抽出する新しい列を作成する
qs['初診年月'] = qs['初診年月日'].dt.to_period('M')

# 年月のみを抽出する新しい列を作成する
qs['出荷年月'] = qs['出荷日時'].dt.to_period('M')

# NaN値を0に置き換える
qs['値引クーポン_税込'] = qs['値引クーポン_税込'].fillna(0)



# 優先順位の設定（'診察代'は最後に設定）
priority_order = ['1ヶ月', '3ヶ月', '12ヶ月',  '中用量', '緊急避妊', 'リベルサス3mg単発1ヶ月', 'リベルサス3mgサブスク1ヶ月', 'リベルサス3mgサブスク3ヶ月', 'リベルサス3mgサブスク6ヶ月', 'リベルサス7mg単発1ヶ月', 'リベルサス7mgサブスク1ヶ月', 'リベルサス7mgサブスク3ヶ月', 'リベルサス7mgサブスク6ヶ月', 'リベルサス14mg単発1ヶ月', 'リベルサス14mgサブスク1ヶ月', 'リベルサス14mgサブスク3ヶ月', 'リベルサス14mgサブスク6ヶ月', '生理', '便秘', '便秘・肥満', '冷え・むくみ', '睡眠', 'その他（感染症）', 'その他', '特典', '診察代']

# 'コース分類4'をカテゴリ型に変換して優先順位を設定
qs['コース分類4'] = pd.Categorical(qs['コース分類4'], categories=priority_order, ordered=True)


# 診察代レコードの請求金額と値引クーポンの合計を計算
qs['診察代合計'] = np.where(qs['コース分類4'] == '診察代', qs['請求金額_raw'] + qs['値引クーポン_税込'] + qs['for biz 企業負担額'], np.nan)

# 各請求IDごとに診察代合計の最初の値を取得
qs['診察代合計'] = qs.groupby('請求id')['診察代合計'].transform('first')

# 診察代以外で最も優先度が高いカテゴリのレコードに診察代合計を割り当て
mask = (qs['コース分類4'] != '診察代') & (qs['コース分類4'] == qs.groupby('請求id')['コース分類4'].transform('min'))
qs.loc[mask, 'GMV診察代_税込'] = qs.loc[mask, '診察代合計']

# 診察代カテゴリのGMV診察代_税込は0に設定
qs.loc[qs['コース分類4'] == '診察代', 'GMV診察代_税込'] = 0

# NaNを0で埋める
qs['GMV診察代_税込'].fillna(0, inplace=True)

# 不要な列を削除
qs.drop(['診察代合計'], axis=1, inplace=True)

# 不要な列を削除
qs.drop(['値引分加算gmv'], axis=1, inplace=True)


# 診察代レコードにあるクーポン値引額を大元のレコードに合算して割り当てる
# データフレームのコピーを作成して 'SettingWithCopyWarning' を回避
qs = qs.copy()

# 優先順位の設定（'診察代'は最後に設定）
priority_order = ['1ヶ月', '3ヶ月', '12ヶ月',  '中用量', '緊急避妊', 'リベルサス3mg単発1ヶ月', 'リベルサス3mgサブスク1ヶ月', 'リベルサス3mgサブスク3ヶ月', 'リベルサス3mgサブスク6ヶ月', 'リベルサス7mg単発1ヶ月', 'リベルサス7mgサブスク1ヶ月', 'リベルサス7mgサブスク3ヶ月', 'リベルサス7mgサブスク6ヶ月', 'リベルサス14mg単発1ヶ月', 'リベルサス14mgサブスク1ヶ月', 'リベルサス14mgサブスク3ヶ月', 'リベルサス14mgサブスク6ヶ月', '生理', '便秘', '便秘・肥満', '冷え・むくみ', '睡眠', 'その他（感染症）', 'その他', '特典', '診察代']

# 'コース分類4'をカテゴリ型に変換して優先順位を設定
qs['コース分類4'] = pd.Categorical(qs['コース分類4'], categories=priority_order, ordered=True)

# 診察代レコードの値引クーポン金額を抽出し、NaN値を0に置き換える
qs['診察代_値引クーポン'] = np.where(qs['コース分類4'] == '診察代', qs['値引クーポン_税込'], 0)

# 各請求IDに対する診察代の値引クーポン金額の合計を取得
qs_summed = qs.groupby('請求id')['診察代_値引クーポン'].sum().reset_index()

# 合計値を元のデータフレームにマージ
qs = qs.merge(qs_summed, on='請求id', suffixes=('', '_summed'))

# 最優先カテゴリに診察代の値引クーポン金額を割り当てるためのマスクを作成
mask = qs['コース分類4'] == qs.groupby('請求id')['コース分類4'].transform('min')

# 割当先レコードの値引クーポン_税込に合計値を加算
qs.loc[mask, '値引クーポン_税込'] += qs.loc[mask, '診察代_値引クーポン_summed']

# 不要な列を削除
qs.drop(['診察代_値引クーポン', '診察代_値引クーポン_summed'], axis=1, inplace=True)


# # カラムの順番をリストで指定
# new_order = [
#         'ユーザーid','年齢','年代','配送先 都道府県', '請求日', '請求ステータス', '請求id','支払方法', '請求回数/処方', '出荷回数/全体', 'ピル種類', '処方コース', 'コース分類1', 'コース分類2', 'コース分類3', 'コース分類4',
#     '診察id', 'ドクターid', '担当ドクター', 'クリニックid', '医療法人名', '処方薬', 'for biz 企業id', 'for biz 企業名', '出荷日時', '払戻日時',
#     '出荷年月', '初診年月', '新規', '診察', '特典',
#     'GMV計_税抜', 'GMV薬代_税抜', 'GMV診察代_税抜', '値引キャンペーン_税抜', '値引クーポン_税抜', '値引特典_税抜', '請求金額_税抜',
#     'GMV計_税込', 'GMV薬代_税込', 'GMV診察代_税込', '値引キャンペーン_税込', '値引クーポン_税込', '値引特典_税込', '請求金額_税込', '請求金額_raw',
#     'for biz 企業負担割合(%)','for biz 企業負担額','同梱数'
#             ]

# # 新しい順番をDataFrameに適用
# qs = qs[new_order]

# # 優先順位の設定（'診察代'は最後に設定）
# priority_order = ['1ヶ月', '3ヶ月', '12ヶ月',  '中用量', '緊急避妊', 'リベルサス3mg単発1ヶ月', 'リベルサス3mgサブスク1ヶ月', 'リベルサス3mgサブスク3ヶ月', 'リベルサス3mgサブスク6ヶ月', 'リベルサス7mg単発1ヶ月', 'リベルサス7mgサブスク1ヶ月', 'リベルサス7mgサブスク3ヶ月', 'リベルサス7mgサブスク6ヶ月', 'リベルサス14mg単発1ヶ月', 'リベルサス14mgサブスク1ヶ月', 'リベルサス14mgサブスク3ヶ月', 'リベルサス14mgサブスク6ヶ月', '生理', '便秘', '便秘・肥満', '冷え・むくみ', '睡眠', 'その他（感染症）', 'その他', '特典', '診察代']
# qs['コース分類4'] = pd.Categorical(qs['コース分類4'], categories=priority_order, ordered=True)

# 特典フラグが1の最優先レコードに値を割り当てる
mask = (qs['特典'] == 1) & (qs['コース分類4'] == qs.groupby('請求id')['コース分類4'].transform('min'))
qs.loc[mask, 'GMV診察代_税込'] = 1500
qs.loc[mask, 'GMV診察代_税抜'] = 1363
qs.loc[mask, '値引特典_税込'] = 1500
qs.loc[mask, '値引特典_税抜'] = 1363

# NaNを0に置き換える
qs['値引クーポン_税込'] = qs['値引クーポン_税込'].fillna(0)
qs['値引キャンペーン_税込'] = qs['値引キャンペーン_税込'].fillna(0)
qs['GMV診察代_税込'] = qs['GMV診察代_税込'].fillna(0)

# # 無限大を最大の整数に置き換える
# qs['値引クーポン_税込'] = qs['値引クーポン_税込'].replace([np.inf, -np.inf], np.iinfo(np.int64).max)
# qs['値引キャンペーン_税込'] = qs['値引キャンペーン_税込'].replace([np.inf, -np.inf], np.iinfo(np.int64).max)
# qs['GMV診察代_税込'] = qs['GMV診察代_税込'].replace([np.inf, -np.inf], np.iinfo(np.int64).max)

# '値引クーポン_税抜'を計算し、結果を新しいカラムに適用する
qs['値引クーポン_税抜'] = np.floor(qs['値引クーポン_税込'] / 1.1).astype(int)
qs['値引キャンペーン_税抜'] = np.floor(qs['値引キャンペーン_税込'] / 1.1).astype(int)
qs['GMV診察代_税抜'] = np.floor(qs['GMV診察代_税込'] / 1.1).astype(int)

# '値引クーポン_税込'が0の場合は、'値引クーポン_税抜'も0に設定する
qs.loc[qs['値引クーポン_税込'] == 0, '値引クーポン_税抜'] = 0
qs.loc[qs['値引キャンペーン_税込'] == 0, '値引キャンペーン_税抜'] = 0
qs.loc[qs['GMV診察代_税込'] == 0, 'GMV診察代_税抜'] = 0


qs.to_csv('csv/m_python.csv', index=False, encoding='utf-8-sig')


""""

# 優先順位の設定
priority_order = ['1ヶ月', '3ヶ月', '12ヶ月',  '中用量', '緊急避妊', 'リベルサス3mg単発1ヶ月', 'リベルサス3mgサブスク1ヶ月', 'リベルサス3mgサブスク3ヶ月', 'リベルサス3mgサブスク6ヶ月', 'リベルサス7mg単発1ヶ月', 'リベルサス7mgサブスク1ヶ月', 'リベルサス7mgサブスク3ヶ月', 'リベルサス7mgサブスク6ヶ月', 'リベルサス14mg単発1ヶ月', 'リベルサス14mgサブスク1ヶ月', 'リベルサス14mgサブスク3ヶ月', 'リベルサス14mgサブスク6ヶ月', '生理', '便秘', '便秘・肥満', '冷え・むくみ', '睡眠', 'その他（感染症）', 'その他', '特典', '診察代']

# 'コース分類4'をカテゴリ型に変換して優先順位を設定
qs['コース分類4'] = pd.Categorical(qs['コース分類4'], categories=priority_order, ordered=True)

# 診察代レコードの請求金額_rawとfor biz 企業負担額の合計を抽出
qs['診察代_請求金額_raw_合計'] = np.where(qs['コース分類4'] == '診察代', qs['請求金額_raw'], 0)
qs['診察代_for biz 合計'] = np.where(qs['コース分類4'] == '診察代', qs['for biz 企業負担額'], 0)

# 各請求IDごとに診察代の合計を求める
qs_summed = qs.groupby('請求id')[['診察代_請求金額_raw_合計', '診察代_for biz 合計']].sum().reset_index()

# 合計値を元のデータフレームにマージ
qs = qs.merge(qs_summed, on='請求id', suffixes=('', '_summed'))

# 最優先の非診察代レコードに診察代の合計を割り当て
mask = (qs['コース分類4'] != '診察代') & (qs['コース分類4'] == qs.groupby('請求id')['コース分類4'].transform('min'))
qs.loc[mask, '請求金額_税込'] = qs.loc[mask, '請求金額_raw'] + qs.loc[mask, 'for biz 企業負担額'] + qs.loc[mask, '診察代_請求金額_raw_合計_summed'] + qs.loc[mask, '診察代_for biz 合計_summed']
qs.loc[mask, 'for biz 企業負担額'] = qs.loc[mask, 'for biz 企業負担額'] + qs.loc[mask, '診察代_for biz 合計_summed']
qs.loc[mask, 'ユーザー負担額'] = qs.loc[mask, '請求金額_raw'] + qs.loc[mask, '診察代_請求金額_raw_合計_summed']

# 不要な列を削除
qs.drop(['診察代_請求金額_raw_合計', '診察代_請求金額_raw_合計_summed', '診察代_for biz 合計', '診察代_for biz 合計_summed'], axis=1, inplace=True)

# ユーザー負担額がNaNのレコードに対して、'for biz 企業負担額'を'請求金額_税込'に割り当てる
qs.loc[qs['ユーザー負担額'].isna(), '請求金額_税込'] = qs.loc[qs['ユーザー負担額'].isna(), 'for biz 企業負担額']

# 条件に基づいて請求金額_税込を更新
qs.loc[(qs['請求金額_税込'] == 0) & (qs['請求金額_raw'] > 0), '請求金額_税込'] = qs['請求金額_raw']

# NaNを0に置換
qs['for biz 企業負担割合(%)'] = qs['for biz 企業負担割合(%)'].fillna(0)
qs['for biz 企業負担額'] = qs['for biz 企業負担額'].fillna(0)

# 'GMV計_税込' カラムを逆算で算定
qs['GMV薬代_税込'] = qs['請求金額_税込'] + qs['値引キャンペーン_税込'] + qs['値引クーポン_税込'] + qs['値引特典_税込'] - qs['GMV診察代_税込']

# 'GMV計_税込' カラムを 'GMV薬代_税込' と 'GMV診察代_税込' の合計として計算
qs['GMV計_税込'] = qs['GMV薬代_税込'] + qs['GMV診察代_税込']
qs['GMV計_税抜'] = qs['GMV薬代_税抜'] + qs['GMV診察代_税抜']

# '請求金額_税込' カラムを 'GMV計_税込' から '値引キャンペーン_税込', '値引クーポン_税込', '値引特典_税込' を差し引いて計算
#####qs['請求金額_税込'] = qs['GMV計_税込'] - (qs['値引キャンペーン_税込'] + qs['値引クーポン_税込'] + qs['値引特典_税込'])
qs['請求金額_税抜'] = qs['GMV計_税抜'] - (qs['値引キャンペーン_税抜'] + qs['値引クーポン_税抜'] + qs['値引特典_税抜'])

# 'for biz 企業負担割合(%)' が0の場合は 'ユーザー負担額' を0に、そうでなければ '請求金額_税込' から 'for biz 企業負担額' を控除
qs['ユーザー負担額'] = np.where(qs['for biz 企業負担割合(%)'] == 100, 0, qs['請求金額_税込'] - qs['for biz 企業負担額'])

#診察代と特典の行を削除
qs = qs[~qs['コース分類4'].isin(['診察代', '特典'])]

# 不要なカラムを削除
qs = qs.drop('請求金額_raw', axis=1)

# 不要なカラムを削除
qs = qs.drop('同梱数', axis=1)

# ユーザーIDと請求IDでグループ化し、各グループ内の請求IDの個数をカウント
grouped_counts = qs.groupby(['ユーザーid', '請求id']).size().reset_index(name='同梱数')

# 各ユーザーIDと請求IDに対する同梱数を元のデータフレームにマージ
qs = qs.merge(grouped_counts, on=['ユーザーid', '請求id'])

# インデックスが重複していないことを確認するためにインデックスをリセット
qs.reset_index(drop=True, inplace=True)

# 各ユーザーIDについて「低用量」または「超低用量」の最初の出荷年月を計算
low_dose_first_shipment = qs[qs['コース分類3'].isin(['低用量', '超低用量'])].groupby('ユーザーid')['出荷日時'].min()

# 新カラム「新規_低用量」を追加し、初期値を0に設定
qs['新規_低用量'] = 0

# 「低用量」または「超低用量」で最初の出荷年月に該当する行に1フラグを設定
qs.loc[qs['ユーザーid'].map(low_dose_first_shipment) == qs['出荷日時'], '新規_低用量'] = 1

# 新カラム「初診年月_低用量」を作成し、1フラグが付与されたレコードの出荷年月を設定
qs['初診年月_低用量'] = pd.NA
qs.loc[qs['新規_低用量'] == 1, '初診年月_低用量'] = qs.loc[qs['新規_低用量'] == 1, '出荷年月']

# 同一ユーザーIDの他のレコードに初診年月をコピー
qs['初診年月_低用量'] = qs.groupby('ユーザーid')['初診年月_低用量'].transform('first')

# インデックスが重複していないことを確認するためにインデックスをリセット
qs.reset_index(drop=True, inplace=True)

# 各ユーザーIDについて「1ヶ月」の最初の出荷年月を計算
low_dose_first_shipment = qs[qs['コース分類4'].isin(['1ヶ月'])].groupby('ユーザーid')['出荷日時'].min()

# 新カラム「新規_1ヶ月」を追加し、初期値を0に設定
qs['新規_1ヶ月'] = 0

# 「1ヶ月」で最初の出荷年月に該当する行に1フラグを設定
qs.loc[qs['ユーザーid'].map(low_dose_first_shipment) == qs['出荷日時'], '新規_1ヶ月'] = 1

# 新カラム「初診年月_1ヶ月」を作成し、1フラグが付与されたレコードの出荷年月を設定
qs['初診年月_1ヶ月'] = pd.NA
qs.loc[qs['新規_1ヶ月'] == 1, '初診年月_1ヶ月'] = qs.loc[qs['新規_1ヶ月'] == 1, '出荷年月']

# 同一ユーザーIDの他のレコードに初診年月をコピー
qs['初診年月_1ヶ月'] = qs.groupby('ユーザーid')['初診年月_1ヶ月'].transform('first')

# インデックスが重複していないことを確認するためにインデックスをリセット
qs.reset_index(drop=True, inplace=True)

# 各ユーザーIDについて「3ヶ月」の最初の出荷年月を計算
low_dose_first_shipment = qs[qs['コース分類4'].isin(['3ヶ月'])].groupby('ユーザーid')['出荷日時'].min()

# 新カラム「新規_3ヶ月」を追加し、初期値を0に設定
qs['新規_3ヶ月'] = 0

# 「3ヶ月」で最初の出荷年月に該当する行に1フラグを設定
qs.loc[qs['ユーザーid'].map(low_dose_first_shipment) == qs['出荷日時'], '新規_3ヶ月'] = 1

# 新カラム「初診年月_3ヶ月」を作成し、1フラグが付与されたレコードの出荷年月を設定
qs['初診年月_3ヶ月'] = pd.NA
qs.loc[qs['新規_3ヶ月'] == 1, '初診年月_3ヶ月'] = qs.loc[qs['新規_3ヶ月'] == 1, '出荷年月']

# 同一ユーザーIDの他のレコードに初診年月をコピー
qs['初診年月_3ヶ月'] = qs.groupby('ユーザーid')['初診年月_3ヶ月'].transform('first')

# インデックスが重複していないことを確認するためにインデックスをリセット
qs.reset_index(drop=True, inplace=True)

# 各ユーザーIDについて「12ヶ月」の最初の出荷年月を計算
low_dose_first_shipment = qs[qs['コース分類4'].isin(['12ヶ月'])].groupby('ユーザーid')['出荷日時'].min()

# 新カラム「新規_12ヶ月」を追加し、初期値を0に設定
qs['新規_12ヶ月'] = 0

# 「12ヶ月」で最初の出荷年月に該当する行に1フラグを設定
qs.loc[qs['ユーザーid'].map(low_dose_first_shipment) == qs['出荷日時'], '新規_12ヶ月'] = 1

# 新カラム「初診年月_12ヶ月」を作成し、1フラグが付与されたレコードの出荷年月を設定
qs['初診年月_12ヶ月'] = pd.NA
qs.loc[qs['新規_12ヶ月'] == 1, '初診年月_12ヶ月'] = qs.loc[qs['新規_12ヶ月'] == 1, '出荷年月']

# 同一ユーザーIDの他のレコードに初診年月をコピー
qs['初診年月_12ヶ月'] = qs.groupby('ユーザーid')['初診年月_12ヶ月'].transform('first')

# インデックスが重複していないことを確認するためにインデックスをリセット
qs.reset_index(drop=True, inplace=True)

# 各ユーザーIDについて「中用量」の最初の出荷年月を計算
low_dose_first_shipment = qs[qs['コース分類4'].isin(['中用量'])].groupby('ユーザーid')['出荷日時'].min()

# 新カラム「新規_中用量」を追加し、初期値を0に設定
qs['新規_中用量'] = 0

# 「中用量」で最初の出荷年月に該当する行に1フラグを設定
qs.loc[qs['ユーザーid'].map(low_dose_first_shipment) == qs['出荷日時'], '新規_中用量'] = 1

# 新カラム「初診年月_中用量」を作成し、1フラグが付与されたレコードの出荷年月を設定
qs['初診年月_中用量'] = pd.NA
qs.loc[qs['新規_中用量'] == 1, '初診年月_中用量'] = qs.loc[qs['新規_中用量'] == 1, '出荷年月']

# 同一ユーザーIDの他のレコードに初診年月をコピー
qs['初診年月_中用量'] = qs.groupby('ユーザーid')['初診年月_中用量'].transform('first')

# インデックスが重複していないことを確認するためにインデックスをリセット
qs.reset_index(drop=True, inplace=True)

# 各ユーザーIDについて「緊急避妊」の最初の出荷年月を計算
low_dose_first_shipment = qs[qs['コース分類4'].isin(['緊急避妊'])].groupby('ユーザーid')['出荷日時'].min()

# 新カラム「新規_緊急避妊」を追加し、初期値を0に設定
qs['新規_緊急避妊'] = 0

# 「緊急避妊」で最初の出荷年月に該当する行に1フラグを設定
qs.loc[qs['ユーザーid'].map(low_dose_first_shipment) == qs['出荷日時'], '新規_緊急避妊'] = 1

# 新カラム「初診年月_緊急避妊」を作成し、1フラグが付与されたレコードの出荷年月を設定
qs['初診年月_緊急避妊'] = pd.NA
qs.loc[qs['新規_緊急避妊'] == 1, '初診年月_緊急避妊'] = qs.loc[qs['新規_緊急避妊'] == 1, '出荷年月']

# 同一ユーザーIDの他のレコードに初診年月をコピー
qs['初診年月_緊急避妊'] = qs.groupby('ユーザーid')['初診年月_緊急避妊'].transform('first')

#QSデータ（医薬品原価）の読み込み
iyakuhin = pd.read_csv('/content/drive/Shareddrives/【分析】QSデータ加工用/01_rawdata/01_master/iyakuhingenka_2409.csv', encoding='shift_jis', low_memory=False)

#iyakuhinのデータリストから処方薬をキーに医薬品原価とシート数をマージ
qs = pd.merge(qs, iyakuhin[['処方薬', '処方薬区分', '先発/GE', '世代', '医薬品原価_税抜', 'シート数']], on='処方薬', how='left')

# 条件を設定
conditions = [
    (qs['コース分類2'] == 'その他単発'),
    (qs['コース分類2'] == '中用量'),
    (qs['コース分類2'] == '緊急避妊'),
    ((qs['コース分類2'].isin(['新定期便', '旧定期便'])) & (qs['請求回数/処方'] == 1)),
    ((qs['コース分類2'].isin(['新定期便', '旧定期便'])) & (qs['コース分類4'] == '3ヶ月')),
    (qs['コース分類2'].isin(['新定期便', '旧定期便']))
]

# 対応する戻り値
choices = [
    '1,3ヶ月処方',
    '中用量',
    '緊急避妊',
    '定期初回',
    '定期4-12回目3シートずつ決済プラン',
    '定期2-12回目1シートずつ決済プラン'
]

# np.selectを使用して新しいカラムを作成
qs['種別'] = np.select(conditions, choices, default='その他')

# 条件を設定
conditions = [
    (qs['種別'] == '1,3ヶ月処方'),
    (qs['種別'].isin(['緊急避妊', '中用量', 'その他'])),
    (qs['種別'] == '定期初回') & (qs['コース分類4'] == '1ヶ月'),
    (qs['種別'] == '定期初回') & (qs['コース分類4'] == '3ヶ月'),
    (qs['種別'] == '定期初回') & (qs['コース分類4'] == '12ヶ月'),
    (qs['種別'] == '定期2-12回目1シートずつ決済プラン'),
    (qs['種別'] == '定期4-12回目3シートずつ決済プラン')
]

# 対応する戻り値
choices = [
    qs['コース分類4'],
    qs['処方薬区分'],
    '定期1回目1シートずつ決済プラン',
    '定期1回目3シートずつ決済プラン',
    '定期1回目12シート一括決済プラン',
    '定期2-12回目1シートずつ決済プラン',
    '定期4-12回目3シートずつ決済プラン'
]

# np.selectを使用して新しいカラムを作成
qs['医療報酬区分'] = np.select(conditions, choices, default='その他')

#QSデータの読み込み
iryouhousyu = pd.read_csv('/content/drive/Shareddrives/【分析】QSデータ加工用/01_rawdata/01_master/iryouhousyu_2409.csv', low_memory=False)

#iryouhousyuのデータリストから医療報酬区分をキーに医療報酬をマージ
qs = pd.merge(qs, iryouhousyu[['医療報酬区分', '医療報酬_税抜']], on='医療報酬区分', how='left')

# '請求id' が重複しているレコードを特定
duplicate_ids = qs[qs.duplicated(subset='請求id', keep=False)]['請求id'].unique()

# 重複している '請求id' かつ '医療報酬区分' が 'プリンペラン' または 'ナウゼリン' のレコードの '医療報酬_税抜' を 0 に設定
qs.loc[(qs['請求id'].isin(duplicate_ids)) & (qs['医療報酬区分'].isin(['プリンペラン', 'ナウゼリン'])), '医療報酬_税抜'] = 0

# # カラムの順番をリストで指定
# new_order = [
#     'ユーザーid','年齢', '年代', '配送先 都道府県', '請求日', '請求ステータス', '請求id','支払方法', '請求回数/処方', '出荷回数/全体', 'ピル種類', '処方コース', 'コース分類1', 'コース分類2', 'コース分類3', 'コース分類4',
#     '診察id', 'ドクターid', '担当ドクター', 'クリニックid', '医療法人名', '処方薬','for biz 企業id', 'for biz 企業名', '出荷日時', '払戻日時',
#     '出荷年月', '初診年月', '新規', '診察', '特典','同梱数',
#     'GMV計_税抜', 'GMV薬代_税抜', 'GMV診察代_税抜', '値引キャンペーン_税抜', '値引クーポン_税抜', '値引特典_税抜', '請求金額_税抜',
#     'GMV計_税込', 'GMV薬代_税込', 'GMV診察代_税込', '値引キャンペーン_税込', '値引クーポン_税込', '値引特典_税込', '請求金額_税込', 'for biz 企業負担割合(%)',	'for biz 企業負担額','ユーザー負担額',
#     '処方薬区分','先発/GE','世代','シート数', '医薬品原価_税抜', '種別', '医療報酬区分', '医療報酬_税抜'
#             ]

# # 新しい順番をDataFrameに適用
# qs = qs[new_order]

# course.csv ファイルからデータを読み込む
course_data = pd.read_csv('/content/drive/Shareddrives/【分析】QSデータ加工用/01_rawdata/01_master/course_2409.csv')

# qs データフレームと course_data を結合する
# コース分類2 と コース分類4 をキーとして結合
qs = qs.merge(course_data[['コース分類2', 'コース分類4', '管理会計用区分', '管理会計用コース']],
              on=['コース分類2', 'コース分類4'],
              how='left')

# ド新規フラグの付け替え
# 優先順位の設定
priority_order = ['安心定期1ヶ月', '安心定期3ヶ月', '安心定期12ヶ月','旧定期1ヶ月','1ヶ月単発', '3ヶ月単発', '中用量', '緊急避妊', 'リベルサス3mg単発1ヶ月', 'リベルサス3mgサブスク1ヶ月', 'リベルサス3mgサブスク3ヶ月', 'リベルサス3mgサブスク6ヶ月', 'リベルサス7mg単発1ヶ月', 'リベルサス7mgサブスク1ヶ月', 'リベルサス7mgサブスク3ヶ月', 'リベルサス7mgサブスク6ヶ月', 'リベルサス14mg単発1ヶ月', 'リベルサス14mgサブスク1ヶ月', 'リベルサス14mgサブスク3ヶ月', 'リベルサス14mgサブスク6ヶ月',  '生理', '便秘・肥満', '便秘', '冷え・むくみ','睡眠','その他（感染症）', 'その他']

# 優先順位を使ってソートするためのカテゴリタイプを作成
qs['管理会計用コース'] = pd.Categorical(qs['管理会計用コース'], categories=priority_order, ordered=True)

# データをユーザーID、出荷日時、請求IDで昇順にソート
qs_sorted = qs.sort_values(by=['ユーザーid', '出荷日時', '請求id'])

# 各ユーザーIDに対して最初の請求レコードを特定（'出荷回数/全体' == 1 の条件を満たすレコードの中から）
first_claim = qs_sorted[qs_sorted['出荷回数/全体'] == 1].drop_duplicates('ユーザーid').index

# 最初の請求レコードに対してのみド新規フラグを1に設定
qs['ド新規'] = 0
qs.loc[qs.index.isin(first_claim), 'ド新規'] = 1

# 同梱数が2以上で、かつ '出荷回数/全体' == 1 の条件を満たすレコードについて優先度の高いレコードを特定
target_qs = qs_sorted[(qs_sorted['同梱数'] >= 2) & (qs_sorted['出荷回数/全体'] == 1)].sort_values(['ユーザーid', '管理会計用コース'])
highest_priority = target_qs.groupby('ユーザーid').head(1).index

# 同梱数が2以上で、かつ '出荷回数/全体' == 1 の条件を満たすレコードについて、ド新規フラグを0に設定
target_records = qs_sorted[(qs_sorted['同梱数'] >= 2) & (qs_sorted['出荷回数/全体'] == 1)].index
qs.loc[qs.index.isin(target_records), 'ド新規'] = 0

# 最高優先順位のレコードに対してのみド新規フラグを1に設定
qs.loc[qs.index.isin(highest_priority), 'ド新規'] = 1

# 「ド新規」が1のレコードの「ユーザーid」と「管理会計用コース」の関係を抽出
initial_prescription = qs[qs['ド新規'] == 1].drop_duplicates('ユーザーid').set_index('ユーザーid')['管理会計用コース']

# 同一「ユーザーid」の全レコードに「初診処方コース」を反映
qs['初診処方コース'] = qs['ユーザーid'].map(initial_prescription)

# 前回処方コースの割当
# 優先順位の設定
priority_order = ['安心定期1ヶ月', '安心定期3ヶ月', '安心定期12ヶ月','旧定期1ヶ月','1ヶ月単発', '3ヶ月単発', '中用量', '緊急避妊', 'リベルサス3mg単発1ヶ月', 'リベルサス3mgサブスク1ヶ月', 'リベルサス3mgサブスク3ヶ月', 'リベルサス3mgサブスク6ヶ月', 'リベルサス7mg単発1ヶ月', 'リベルサス7mgサブスク1ヶ月', 'リベルサス7mgサブスク3ヶ月', 'リベルサス7mgサブスク6ヶ月', 'リベルサス14mg単発1ヶ月', 'リベルサス14mgサブスク1ヶ月', 'リベルサス14mgサブスク3ヶ月', 'リベルサス14mgサブスク6ヶ月',  '生理', '便秘・肥満', '便秘', '冷え・むくみ','睡眠','その他（感染症）', 'その他']

# 管理会計用コースをカテゴリタイプに設定
qs['管理会計用コース'] = pd.Categorical(qs['管理会計用コース'], categories=priority_order, ordered=True)

# ユーザーid、出荷日時、請求id、管理会計用コースで昇順ソート
qs = qs.sort_values(['ユーザーid', '出荷日時', '請求id', '管理会計用コース'], ascending=[True, True, True, False])

# 各ユーザーIDについて、直前の異なる出荷日時のレコードの管理会計用コースを前回処方コースに設定
qs['前回処方コース'] = qs.groupby('ユーザーid')['管理会計用コース'].shift(1)

# 各ユーザーIDについて、直前の異なる出荷日時のレコードの出荷日時を前回出荷日時に設定
qs['前回出荷日時'] = qs.groupby('ユーザーid')['出荷日時'].shift(1)

# ド新規フラグが1の場合、前回処方コースを空白に設定
qs.loc[qs['ド新規'] == 1, '前回処方コース'] = None

# 次に、同一請求IDでド新規フラグが1のレコードの管理会計用コースのデータを取得
new_prescription = qs[qs['ド新規'] == 1][['請求id', '管理会計用コース']].drop_duplicates('請求id').set_index('請求id')

# 新規フラグが1でド新規フラグが0且つ前回処方コースが空白のレコードに対して、当該データを反映
qs.loc[(qs['新規'] == 1) & (qs['ド新規'] == 0) & (qs['前回処方コース'].isna()), '前回処方コース'] = qs['請求id'].map(new_prescription['管理会計用コース'])

# Step 1: 各ユーザーIDと管理会計用コースごとに最も古い出荷年月を求める
first_shipment = qs.groupby(['ユーザーid', '管理会計用コース'], observed=True)['出荷年月'].transform('min')

# Step 2: 新しいカラム「コース別初診年月」を元のDataFrameに追加
qs['コース別初診年月'] = first_shipment

# Step 3: 必要なカラム名を変更
qs.rename(columns={'出荷年月': 'コース別初診年月', '出荷年月': '出荷年月'}, inplace=True)


# 日付形式を変更する関数の定義
def format_date(df, column):
    if column in df.columns:
        # カラムがPeriodDtype型の場合、先にto_timestamp()を使用してdatetime64型に変換
        if isinstance(df[column].dtype, pd.PeriodDtype):
            df[column] = df[column].dt.to_timestamp()

        # 日付形式を変更
        df[column] = pd.to_datetime(df[column]).dt.strftime('%Y年%m月')

# 各日付カラムの形式を変更
format_date(qs, '出荷年月')
format_date(qs, '初診年月')
format_date(qs, 'コース別初診年月')


# ユーザーidが53のレコードの初診年月カラムに出荷年月のデータを反映
qs.loc[qs['ユーザーid'] == 53, '初診年月'] = qs.loc[qs['ユーザーid'] == 53, '出荷年月']

# 同様に初診処方コースカラムに管理会計用コースのデータを反映
qs.loc[qs['ユーザーid'] == 53, '初診処方コース'] = qs.loc[qs['ユーザーid'] == 53, '管理会計用コース']

# ユーザーidが53のレコードの新規とド新規に1を格納
qs.loc[qs['ユーザーid'] == 53, '新規'] = 1
qs.loc[qs['ユーザーid'] == 53, 'ド新規'] = 1

# カラム名の変更
qs.rename(columns={'新規': '旧ド新規', 'ド新規': '新ド新規'}, inplace=True)

# カラムの順番をリストで指定
new_order = [
'ユーザーid',	'年齢',	'年代',	'配送先 都道府県',	'請求日',	'請求ステータス',	'請求id',	'支払方法',	'請求回数/処方',	'出荷回数/全体',	'ピル種類',	'処方コース',	'コース分類1',	'コース分類2',	'コース分類3',	'コース分類4',	'診察id',	'ドクターid',	'担当ドクター',
'クリニックid',	'医療法人名',	'処方薬',	'for biz 企業id',	'for biz 企業名',	'出荷日時',	'払戻日時',	'出荷年月',	'初診年月', '初診処方コース', 'コース別初診年月', '管理会計用区分', '管理会計用コース', '前回出荷日時','前回処方コース', '旧ド新規', '新ド新規', '診察', '特典', '同梱数',
'GMV計_税抜',	'GMV薬代_税抜',	'GMV診察代_税抜',	'値引キャンペーン_税抜', '値引クーポン_税抜', '値引特典_税抜', '請求金額_税抜',
'処方薬区分', '先発/GE', '世代', 'シート数', '医薬品原価_税抜', '種別', '医療報酬区分', '医療報酬_税抜'
            ]
# 新しい順番をDataFrameに適用
qs = qs[new_order]

#表示
qs

# '年代'カラム内の'15~19'を'18~19'に変更
# qs = qs.copy()
# qs['年代'] = qs['年代'].replace('15~19', '18~19')

# 「年代」カラムで '15~19' となっている値を '18~19~' に置換
qs.loc[qs['年代'] == '15~19', '年代'] = '18~19'

# 「年代」カラムで '45~49' となっている値を '45~' に置換
qs.loc[qs['年代'] == '45~49', '年代'] = '45~'

# 「年齢」カラムで 50 歳以上の行の「年代」を '45~' に置換
qs.loc[qs['年齢'] >= 50, '年代'] = '45~'

# ユーザーIdが1001であるレコードをフィルタリング
filtered_qs = qs.loc[qs['ユーザーid'] == 819]

# フィルタリングされたデータフレームを表示
filtered_qs

# 出荷日時と前回出荷日時を日付型に変換
qs.loc[:, '出荷日時'] = pd.to_datetime(qs['出荷日時'], errors='coerce')
qs.loc[:, '前回出荷日時'] = pd.to_datetime(qs['前回出荷日時'], errors='coerce')

# 月単位で前回出荷日時と出荷日時の差を計算
month_diff = (qs['出荷日時'].dt.to_period('M') - qs['前回出荷日時'].dt.to_period('M'))
month_diff = month_diff.apply(lambda x: x.n if pd.notna(x) else None)

# 条件①：旧ド新規が1の場合は「新規」を設定
qs.loc[qs['旧ド新規'] == 1, '取引区分'] = '新規'

# 条件②：旧ド新規が0且つ診察が1かつ管理会計用コースと前回処方コースが一致する場合は「休眠復帰_単純」を設定
condition_2 = (qs['旧ド新規'] == 0) & (qs['診察'] == 1) & (qs['管理会計用コース'] == qs['前回処方コース'])
qs.loc[condition_2, '取引区分'] = '休眠復帰_単純'

# 条件③：月単位で連続している場合は「継続_単純」
condition_3 = (qs['旧ド新規'] == 0) & (qs['管理会計用コース'] == qs['前回処方コース']) & ((month_diff == 1) | (month_diff == 0))
qs.loc[condition_3, '取引区分'] = '継続_単純'

# 条件④：月単位で2ヶ月以上空いている且つ診察が0かつ管理会計用コースと前回処方コースが一致する場合は「継続_間の空いた決済」
condition_4 = (qs['旧ド新規'] == 0) & (qs['診察'] == 0) & (qs['管理会計用コース'] == qs['前回処方コース']) & (month_diff > 1)
qs.loc[condition_4, '取引区分'] = '継続_間の空いた決済'

# 条件⑤：アップセル
condition_5 = (
    (qs['旧ド新規'] == 0) & (qs['診察'] == 1) &
    (((qs['管理会計用コース'] == '安心定期3ヶ月') & (qs['前回処方コース'] == '安心定期1ヶ月')) |
     ((qs['管理会計用コース'] == '安心定期12ヶ月') & (qs['前回処方コース'].isin(['安心定期1ヶ月', '安心定期3ヶ月'])))) &
    (month_diff == 1)
)
qs.loc[condition_5, '取引区分'] = '継続_アップセル'

# 条件⑥：アップセル_休眠復帰
condition_6 = (
    (qs['旧ド新規'] == 0) & (qs['診察'] == 1) &
    (((qs['管理会計用コース'] == '安心定期3ヶ月') & (qs['前回処方コース'] == '安心定期1ヶ月')) |
     ((qs['管理会計用コース'] == '安心定期12ヶ月') & (qs['前回処方コース'].isin(['安心定期1ヶ月', '安心定期3ヶ月'])))) &
    (month_diff > 1)
)
qs.loc[condition_6, '取引区分'] = '休眠復帰_アップセル'

# 条件⑦：ダウンセル
condition_7 = (
    (qs['旧ド新規'] == 0) & (qs['診察'] == 1) &
    (
        ((qs['管理会計用コース'] == '安心定3ヶ月') & (qs['前回処方コース'] == '安心定期12ヶ月')) |
        ((qs['管理会計用コース'].isin(['安心定期1ヶ月', '安心定期3ヶ月'])) & (qs['前回処方コース'] == '安心定期12ヶ月'))
    ) &
    (month_diff == 1)
)
qs.loc[condition_7, '取引区分'] = '継続_ダウンセル'

# 条件⑧：ダウンセル_休眠復帰
condition_8 = (
    (qs['旧ド新規'] == 0) & (qs['診察'] == 1) &
    (
        ((qs['管理会計用コース'] == '安心定3ヶ月') & (qs['前回処方コース'] == '安心定期12ヶ月')) |
        ((qs['管理会計用コース'].isin(['安心定期1ヶ月', '安心定期3ヶ月'])) & (qs['前回処方コース'] == '安心定期12ヶ月'))
    ) &
    (month_diff > 1)
)
qs.loc[condition_8, '取引区分'] = '休眠復帰_ダウンセル'

# '取引区分' カラムに限定して 'na' を NaN に置き換え
qs['取引区分'].replace('na', pd.NA, inplace=True)

# 条件⑨の更新：移行決済（月単位で連続しているか同じ月の場合）
condition_9 = (
    ~(condition_2 | condition_3 | condition_4 | condition_5 | condition_6 | condition_7 | condition_8) &
    ((month_diff == 1) | (month_diff == 0)) &
    qs['取引区分'].isna()
)
qs.loc[condition_9, '取引区分'] = '継続_移行決済'

# '取引区分' カラムに限定して 'na' を NaN に置き換え
qs['取引区分'].replace('na', pd.NA, inplace=True)

# 条件⑩：移行決済_休眠復帰
condition_10 = (
    ~(condition_2 | condition_3 | condition_4 | condition_5 | condition_6 | condition_7 | condition_8 | condition_9) &
    (month_diff > 1) &
    qs['取引区分'].isna()
)
qs.loc[condition_10, '取引区分'] = '休眠復帰_移行決済'

# 更新されたデータフレームの先頭数行を表示
qs.head()

# チャネルデータを読み込む
baitai = pd.read_csv('/content/drive/Shareddrives/【分析】QSデータ加工用/01_rawdata/01_master/channel_2409.csv', encoding='utf-8')

# チャネルマージ用データを読み込む
baitai_merge = pd.read_csv('/content/drive/Shareddrives/【分析】QSデータ加工用/01_rawdata/01_master/baitai_merge_2409.csv', encoding='utf-8')

# 薬コース①と薬コース②をキーとして結合
merged = pd.merge(baitai, baitai_merge, on=['01_コース分類_1', '05_コース分類_5'], how='left')

# カラム名の統一
merged.rename(columns={'ユーザーID': 'ユーザーid'}, inplace=True)

# 日付をdatetimeオブジェクトに変換
merged['出荷日時'] = pd.to_datetime(merged['出荷日時'])

# 必要な形式（yymmdd）に変換して新しいカラムに格納
merged['key'] = merged['出荷日時'].dt.strftime('%y%m%d')

# ユーザーidが数値型の場合は、文字列型に変換する必要がある
merged['key'] = merged['key'].astype(str) + '-' + merged['ユーザーid'].astype(str) +  merged['管理会計用コース'].astype(str)

# スライスされたデータフレームでの操作を避けるために、一度コピーを作成
qs = qs.copy()

# データ型の確認と変換
qs.loc[:, '出荷日時'] = pd.to_datetime(qs['出荷日時'], errors='coerce')

# 必要な形式（yymmdd）に変換して新しいカラムに格納
qs.loc[:, 'key'] = qs['出荷日時'].dt.strftime('%y%m%d')

# ユーザーidが数値型の場合は、文字列型に変換する必要がある
qs.loc[:, 'key'] = qs['key'] + '-' + qs['ユーザーid'].astype(str) + qs['管理会計用コース'].astype(str)

# merged から 'key' と 'Secondary' のカラムを選択
qs = pd.merge(qs, merged[['key', 'Secondary']], on='key', how='left')

# 結合後のデータフレームから 'key' カラムを削除
qs.drop('key', axis=1, inplace=True)

# 結果を表示（qsの最初の数行）
qs.head()

# 新ド新規が1のレコードの媒体Secondary の値を取得
media_mapping = qs[qs['新ド新規'] == 1].set_index('ユーザーid')['Secondary'].to_dict()

# NaN値を置き換える関数
def fill_media(row):
    if pd.isna(row['Secondary']):
        return media_mapping.get(row['ユーザーid'], row['Secondary'])
    return row['Secondary']

# 各行に対してNaN値の置き換えを適用
qs['Secondary'] = qs.apply(fill_media, axis=1)

# 結果の表示
qs.head()

# 出力ファイルのベースパス
base_path = '/content/drive/Shareddrives/【分析】QSデータ加工用/02_outputdata/01_QSコンバートrawdata/qs_convert4'

# 出荷日時カラムを日付型に変換
qs['出荷日時'] = pd.to_datetime(qs['出荷日時'], errors='coerce')

# データフレームの出荷日時を年ごとに分割し、CSVファイルとして出力
for year, group in qs.groupby(qs['出荷日時'].dt.year):
    # CSVファイル名を年で設定
    file_path = f"{base_path}_{year}.csv"
    # utf-8-sigでエンコーディングを指定
    group.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"CSV file for year {year} is written to {file_path}")

"""