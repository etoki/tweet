-- custom_shop_idで、まず住所とid確認、idは最後に使う
-- SELECT id, name,custom_shop_id,ACTIVE,address FROM shops WHERE custom_shop_id IN (4464)

-- idで、すでに存在するか確認
 SELECT * FROM delivery_options WHERE partner_id = 'uber_direct' and shop_id IN (6285)

-- 追加クエリ、最初の欄は↑で取得したshops.id
-- INSERT INTO `delivery_options` (`shop_id`, `partner_id`, `original_delivery_option_id`, `active`, `min_price`) VALUES ('6285','uber_direct',NULL, 0, 0);
