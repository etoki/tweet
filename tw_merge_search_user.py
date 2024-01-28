import tweepy
from pprint import pprint
import pandas as pd

# API情報を記入
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAenrwEAAAAAz%2Fj8aUNf%2FVXwYJWbKbGzi3UyWlY%3D8f1i4rTemX6vAcutguS14QybbUUiMUu5G6z9D3tXmoyF8X3NcG"
API_KEY = "OGHUuZIAaswYX3YMXbNOv1bHV"
API_SECRET = "0rw4WWImwkgs7itLD4LyqECLD2OfuZkZ3VAABPgR14hK3BZJ5T"
ACCESS_TOKEN = "1229650988216115200-CntDVVABeE7sF5SPinnEhHmyGoSV6Q"
ACCESS_TOKEN_SECRET = "4vTSdq2gjMgMEQvrBdirNIXwO4G8tmyMWBVngNsFphFkT"


# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                          )
    
    return client

def GetUser(user_id):
    GetUser = ClientInfo().get_user(id=int(user_id), 
                                    user_fields=[
                                        "created_at",
                                        "description",
                                        "location",
                                        "protected",
                                        "public_metrics"]).data
    result  = {
        "user_id": user_id,
        "name": GetUser.name,
        "username": GetUser.username,
        "created_at": GetUser.created_at,
        "location": GetUser.location,
        "protected": GetUser.protected,
        "description": GetUser.description
        # "public_metrics": GetUser.public_metrics
    }
    result.update(GetUser.public_metrics)
    # result = pd.Series(result)
    return result
    

df = pd.read_csv("output.csv")
authors = df["author_id"]

results = []

for author_id in authors:
    results.append(GetUser(author_id))

results = pd.DataFrame(results)
# pprint(results)

merged_df = pd.merge(df, results, left_on='author_id', right_on='user_id', how='inner')
pprint(merged_df)
# 改行、カンマ、全角スペース削除
merged_df = merged_df.replace( '\n', '', regex=True).replace( ',', '', regex=True).replace( '\u3000', ' ', regex=True)
merged_df.to_csv('output_merge.csv', index=False, encoding="utf-8") 

