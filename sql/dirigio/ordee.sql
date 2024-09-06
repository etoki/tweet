SELECT id,user_id,STATUS
FROM orders 
WHERE 
id IN (1964448)
AND STATUS = 3
-- LIMIT 100

-- statusが3となっていることを確認し、2に変更する