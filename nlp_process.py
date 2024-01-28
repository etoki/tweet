from pprint import pprint
import pandas as pd
import re

df = pd.read_csv("output_merge.csv")

# テキストデータの前処理
def text_preprocessing(text):
   # 改行コード、タブ、スペース削除
   text = ''.join(text.split())
   # URLの削除
   text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', text)
   # メンション除去 
   text = re.sub(r'@([A-Za-z0-9_]+)', '', text) 
   # 記号の削除
   text = re.sub(r'[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥]', '', text)

   return text

df["text"] = df["text"].map(text_preprocessing)
pprint(df)
