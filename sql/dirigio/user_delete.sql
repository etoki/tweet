SELECT id,email,deleted,deleted_time FROM  users
-- WHERE email LIKE "%yuyu.mimi0816@i.softbank.jp%"
WHERE id IN (3576094)

-- emailの末尾に-deletedを追加
-- deletedを1に変更
-- deleted_timeに0を入れる
;