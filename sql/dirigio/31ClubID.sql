-- まず存在するかチェック
SELECT * FROM app_user_profiles
WHERE user_id IN (3472004,2545270,3467351,3477414,3484347,3492886)

-- なければ入れる
-- insert into app_user_profiles (user_id, app_id, custom_id) VALUES (3372461, 31, 100267007157);
