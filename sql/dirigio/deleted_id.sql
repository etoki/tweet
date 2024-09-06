-- delete from app_user_profiles WHERE app_id = 31 and user_id in (select id from users where deleted > 0 or (from_unixtime(create_time) < '2024/08/29 15:45' and authed_mail is NULL))

-- 消されたか確認
SELECT * FROM app_user_profiles WHERE user_id IN (3378789)
