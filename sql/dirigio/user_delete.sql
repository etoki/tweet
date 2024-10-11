SELECT id,email,deleted,deleted_time FROM  users
WHERE email LIKE "%teii_cosumen.t08-09.yabainaa--@docomo.ne.jp%"
-- WHERE id IN (1940361,174395,3587988,2225938,3565026)

-- emailの末尾に-deletedを追加
-- deletedを1に変更
-- deleted_timeに0を入れる
;