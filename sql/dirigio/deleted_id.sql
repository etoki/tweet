-- delete from app_user_profiles WHERE app_id = 31 and user_id in (select id from users where deleted > 0 or (from_unixtime(create_time) < '2024/09/12 15:00' and authed_mail is NULL))

-- 消されたか確認
SELECT * FROM app_user_profiles 
WHERE user_id IN (3437400,3425784,3456153,3459681,3461566)
