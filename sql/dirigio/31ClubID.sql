-- まず存在するかチェック
SELECT * FROM app_user_profiles WHERE user_id IN (3479969,3506748)

-- なければ入れる
-- insert into app_user_profiles (user_id, app_id, custom_id) VALUES (3479969, 31, 200105324501);
