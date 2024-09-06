-- まず存在するかチェック
SELECT * FROM app_user_profiles WHERE user_id = 3372461;

-- なければ入れる
-- insert into app_user_profiles (user_id, app_id, custom_id) VALUES (3372461, 31, 100267007157);
