from pprint import pprint
import pandas as pd
import re

df = pd.read_csv("output_merge.csv")

#@title 使用する品詞とストップワードの指定
#@markdown  ※include_pos：使用する品詞，stopwords：表示させない単語 ← それぞれ任意に追加と削除が可能
include_pos = ('NOUN', 'PROPN', 'VERB', 'ADJ') #@param {type:"raw"}
stop_words = ('する', 'ある', 'ない', 'いう', 'もの', 'こと', 'よう', 'なる', 'ほう', 'いる', 'くる', 'お', 'つ', 'とき','ところ', '為', '他', '物', '時', '中', '方', '目', '回', '事', '点', 'ため') #@param {type:"raw"}

# テキストデータの前処理
def text_preprocessing(text):
   # 改行コード、タブ、スペース削除
   text = ''.join(text.split())
   # URLの削除
   text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', text)
   # メンション除去 
   text = re.sub(r'@([A-Za-z0-9_]+)', '', text) 
   text = re.sub(r'RT', '', text) 
   # 記号の削除
   text = re.sub(r'[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥]', '', text)

   return text

df["text"] = df["text"].map(text_preprocessing)
pprint(df)
