SELECT id,email,deleted,deleted_time FROM  users
-- WHERE email LIKE "%odatskktaymt2020%"
WHERE id IN (1685701)

-- emailの末尾に-deletedを追加
-- deletedを1に変更
-- deleted_timeに0を入れる
;