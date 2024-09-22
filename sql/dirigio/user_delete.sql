SELECT id,email,deleted,deleted_time FROM  users
-- WHERE email LIKE "%springraincgtyouruanyanss92217@au.com%"
WHERE id IN (3512461,3514554)

-- emailの末尾に-deletedを追加
-- deletedを1に変更
-- deleted_timeに0を入れる
;