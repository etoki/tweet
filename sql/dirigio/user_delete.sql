SELECT id,email,deleted,deleted_time FROM  users
WHERE email LIKE "%chi3.7momo%"
-- WHERE id IN (3437400,3425784,3456153,3459681,3461566)

-- emailの末尾に-deletedを追加
-- deletedを1に変更
-- deleted_timeに0を入れる
;