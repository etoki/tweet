-- まず存在するかチェック
SELECT * FROM app_user_profiles WHERE user_id IN (3594279)

-- なければ入れる
-- insert into app_user_profiles (user_id, app_id, custom_id) VALUES (3594279, 31, 100411186118);
