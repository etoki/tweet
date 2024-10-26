-- まず存在するかチェック
 SELECT * FROM app_user_profiles WHERE user_id IN (3511519)
-- SELECT * FROM app_user_profiles WHERE custom_id IN (100435752955)

-- なければ入れる
-- insert into app_user_profiles (user_id, app_id, custom_id) VALUES (3590185, 31, 200101416691);
