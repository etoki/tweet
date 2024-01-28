from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
from pprint import pprint

# アンケート結果をリストに格納
responses = [
    "製品の品質は素晴らしいです。特にデザインが気に入りました。使いやすさも抜群です。",
    "製品は普通です。期待通りの性能で、特に良い点や悪い点はありませんでした。",
    "製品は期待外れでした。機能が不安定で、操作性も悪いです。購入を後悔しています。"
]

# リストをDataFrameに変換
df = pd.DataFrame({'回答': responses})

# モデルの読み込み
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 感情分析の結果を格納するリスト
emotion_results = []

# 各回答に対して感情分析を実行
for text in df['回答']:
    # テキストの前処理とトークン化
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # モデルに入力データを渡して感情分析を実行
    outputs = model(**inputs)
    probs = outputs.logits.softmax(dim=1)[0]

    # 感情ラベルと確率を取得
    emotion_labels = ['very negative', 'negative', 'neutral', 'positive', 'very positive']
    results = [(label.replace('LABEL_', '').replace('_', ' ').capitalize(), prob.item()) for label, prob in zip(emotion_labels, probs)]

    # 最も高い確率である結果を取得
    predicted_emotion, highest_prob = max(results, key=lambda x: x[1])

    # 結果をリストに追加
    emotion_results.append((predicted_emotion, highest_prob))

# 感情分析の結果をDataFrameに追加
df['感情'] = [result[0] for result in emotion_results]
df['確率'] = [result[1] for result in emotion_results]

# 結果を出力
pprint(df)
