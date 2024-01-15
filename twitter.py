# ライブラリのインポート
import tweepy
from datetime import datetime,timezone
import pytz
import pandas as pd

# Twitterの認証
# 取得したキーを格納
API_KEY = "***********************"
API_SECRET = "***********************"
ACCESS_TOKEN = "***********************"
ACCESS_TOKEN_SECRET = "***********************"
 
# Tweepy設定

# TwitterAPI認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
# アクセストークン設定
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#　”wait_on_rate_limit = True”　利用制限にひっかかた時に必要時間待機する
api = tweepy.API(auth ,wait_on_rate_limit = True)

# 検索条件の設定
search_word = 'マーケティング'
item_number = 50

#検索条件を元にツイートを抽出
tweets = tweepy.Cursor(api.search_tweets,q=search_word,lang='ja').items(item_number)

#関数:　UTCをJSTに変換する
def change_time_JST(u_time):
    #イギリスのtimezoneを設定するために再定義する
    utc_time = datetime(u_time.year, u_time.month,u_time.day, 
    u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    #タイムゾーンを日本時刻に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # 文字列で返す
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

#抽出したデータから必要な情報を取り出す
#取得したツイートを一つずつ取り出して必要な情報をtweet_dataに格納する
tw_data = []

for tweet in tweets:
    #ツイート時刻とユーザのアカウント作成時刻を日本時刻にする
    tweet_time = change_time_JST(tweet.created_at)
    create_account_time = change_time_JST(tweet.user.created_at)
    #tweet_dataの配列に取得したい情報を入れていく
    tw_data.append([
        tweet.id,
        tweet_time,
        tweet.text,
        tweet.favorite_count, 
        tweet.retweet_count, 
        tweet.user.id, 
        tweet.user.screen_name,
        tweet.user.name,
        tweet.user.description,
        tweet.user.friends_count,
        tweet.user.followers_count,
        create_account_time,
        tweet.user.following,
        tweet.user.profile_image_url,
        tweet.user.profile_background_image_url,
        tweet.user.url
                       ])

#取り出したデータをpandasのDataFrameに変換
#CSVファイルに出力するときの列の名前を定義
labels=[
    'ツイートID',
    'ツイート時刻',
    'ツイート本文',
    'いいね数',
    'リツイート数',
    'ID',
    'ユーザー名',
    'アカウント名',
    '自己紹介文',
    'フォロー数',
    'フォロワー数',
    'アカウント作成日時',
    '自分のフォロー状況',
    'アイコン画像URL',
    'ヘッダー画像URL',
    'WEBサイト'
    ]

#tw_dataのリストをpandasのDataFrameに変換
df = pd.DataFrame(tw_data,columns=labels)

#CSVファイルに出力する
#CSVファイルの名前を決める
file_name='tw_data.csv'

#CSVファイルを出力する
df.to_csv(file_name,encoding='utf-8-sig',index=False)
