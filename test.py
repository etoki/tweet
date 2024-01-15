import requests
import pandas as pd

API_KEY = "OGHUuZIAaswYX3YMXbNOv1bHV"
API_SECRET = "0rw4WWImwkgs7itLD4LyqECLD2OfuZkZ3VAABPgR14hK3BZJ5T"
ACCESS_TOKEN = "1229650988216115200-CntDVVABeE7sF5SPinnEhHmyGoSV6Q"
ACCESS_TOKEN_SECRET = "4vTSdq2gjMgMEQvrBdirNIXwO4G8tmyMWBVngNsFphFkT"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAenrwEAAAAAz%2Fj8aUNf%2FVXwYJWbKbGzi3UyWlY%3D8f1i4rTemX6vAcutguS14QybbUUiMUu5G6z9D3tXmoyF8X3NcG"

SEARCH_KEYWORD = "税"  # 取得したいキーワードを設定
MAX_RESULTS = 10  # 収集する最大ポスト数を設定

URL = f"https://api.twitter.com/2/tweets/search/recent?query={SEARCH_KEYWORD}&tweet.fields=public_metrics,author_id&max_results={MAX_RESULTS}"
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

def convert_to_dataframe(tweets):
    # tweetsのリストからDataFrameを生成
    data = {
        "tweet_id": [tweet["id"] for tweet in tweets],
        "text": [tweet["text"] for tweet in tweets],
        "author_id": [tweet["author_id"] for tweet in tweets],
        "retweets": [tweet["public_metrics"]["retweet_count"] for tweet in tweets],
        "likes": [tweet["public_metrics"]["like_count"] for tweet in tweets],
    }
    df = pd.DataFrame(data)
    return df

def get_tweets_with_keyword():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Request returned {response.status_code}: {response.text}")

    response_data = response.json()
    tweets = response_data['data']

    # ポストデータをPandasのDataFrameに変換
    df = convert_to_dataframe(tweets)

    return df

# 取得したデータを出力
if __name__ == "__main__":
    tweets_df = get_tweets_with_keyword()
    print(tweets_df)
