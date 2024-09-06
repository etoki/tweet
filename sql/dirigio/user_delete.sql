SELECT id,email,deleted,deleted_time FROM  users
WHERE email LIKE "%eichan-mii-enachan_16.95.48@ezweb.ne.jp%"
-- WHERE id IN (209821,3391257,3407987)

-- emailの末尾に-deletedを追加
-- deletedを1に変更
-- deleted_timeに0を入れる
;