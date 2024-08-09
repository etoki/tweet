SELECT id,email,deleted,deleted_time FROM  users
WHERE email IS NOT null
-- WHERE email LIKE "%n.naomi5563@icloud.cm%"
LIMIT 100
;