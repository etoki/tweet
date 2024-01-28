import pandas as pd
from pprint import pprint
from transformers import pipeline

# アンケート結果をリストに格納
responses = [
    "製品の品質は素晴らしいです。特にデザインが気に入りました。使いやすさも抜群です。",
    "製品は普通です。期待通りの性能で、特に良い点や悪い点はありませんでした。",
    "製品は期待外れでした。機能が不安定で、操作性も悪いです。購入を後悔しています。"
]

# リストをDataFrameに変換
df = pd.DataFrame({'回答': responses})

# パイプラインを作成
classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# 感情分析を実行
emotions = []
for text in df['回答']:
    results = classifier(text)
    predicted_emotion = results[0]['label']
    highest_prob = results[0]['score']
    emotions.append((predicted_emotion, highest_prob))

# 結果をDataFrameに追加
df['感情'] = [emotion[0] for emotion in emotions]
df['確率'] = [emotion[1] for emotion in emotions]

# 結果を出力
pprint(df)
