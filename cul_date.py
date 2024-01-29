from datetime import datetime, timedelta

# 現在の日時を取得
current_datetime = datetime.now()

# 7日と9時間前の日時を計算
start_delta = timedelta(days=7, hours=9)
start_time = current_datetime - start_delta

# 23時59分59秒を足す
# 最低でも10秒前にしないといけない、APIの条件
end_delta = timedelta(days=1, seconds=-10) 
end_time = start_time + end_delta

# 指定されたフォーマットで7日9時間前の日時を表示、確認のためだけ
formatted_start_datetime = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
formatted_end_datetime = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
print("開始時間:", formatted_start_datetime)
print("終了時間:", formatted_end_datetime)

# 1日ずつ足して7回処理する
for i in range(7):
    # 日付を1日増やす
    new_start_date = start_time + timedelta(days=i)
    new_end_date   = end_time   + timedelta(days=i)
    
    # 新しい日付を文字列に変換して出力
    new_start_date_str = new_start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    new_end_date_str   = new_end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    print("回数：", i)
    print(new_start_date_str)
    print(new_end_date_str)

