SELECT id,email,deleted,deleted_time FROM  users
WHERE email LIKE "%k15_chimako.4848%"
-- WHERE id IN (3472004,2545270,3467351,3477414,3484347,3492886)

-- emailの末尾に-deletedを追加
-- deletedを1に変更
-- deleted_timeに0を入れる
;