from pprint import pprint
import spacy
import ginza
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

nlp = spacy.load("ja_ginza")
ginza.set_split_mode(nlp, 'C') # 分割単位C

# 行毎に出現する単語をリストに追加
words_list=[]  #行毎の単語リスト
for doc in nlp.pipe(df["text"]):
    sep_word=[token.lemma_ for token in doc if token.pos_ in include_pos and token.lemma_ not in stop_words]
    words_list.append(sep_word)
    # pprint(words_list)

#行毎の意見 → 単語に分解し、カラムに格納
df['separate_words'] = [s for s in words_list]
pprint(df['separate_words'])


#@title 共起ネットワーク
#@markdown  **<font color= "Crimson">ガイド</font>：ネットワーク表示の濃淡は min_edge_frequency で変更できます。表示にみにくさを感じた場合は値を大きく、より細かく表示したい場合は値を小さくしてください。**

min_edge_frequency = 1 #@param {type:"slider", min:1, max:20, step:1}

import nlplot
import plotly
from plotly.subplots import make_subplots
from plotly.offline import iplot

npt = nlplot.NLPlot(df, target_col='separate_words')

npt.build_graph(
    #stopwords=stopwords,
    min_edge_frequency=min_edge_frequency)
# The number of nodes and edges to which this output is plotted.
# If this number is too large, plotting will take a long time, so adjust the [min_edge_frequency] well.
# >> node_size:70, edge_size:166
fig_co_network = npt.co_network(
    title='Co-occurrence network',
    sizing=100,
    node_size='adjacency_frequency',
    color_palette='hls',
    width=1100,
    height=700,
    save=False
)
iplot(fig_co_network)

