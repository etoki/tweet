/*
INSERT INTO `shops` (`name`, `lat`, `lng`, `intro`, `tel`, `image_url`, `genre_id`, `pickup`, `active`, `slack`, `family_id`, `min_order_time`, `tokusho_company_name`, `tokusho_manager_name`, `tokusho_address`, `tokusho_phone_number`, `asap`, `icon`, `subtitle`, `email`, `default_min_order_time`, `company_id`, `create_time`, `last_order_day`, `last_order_time`, `cashback_flag`, `shop_paid_detail_id`, `plan_id`, `lp_flag`, `icon_url`, `banner_url`, `color`, `plan_start_time`, `shop_paid_method_id`, `delivery_lead_time`, `address`, `delivery_shop_cost`, `delivery_rate`, `display`, `delivery_base_cost`, `delivery_partner_id`, `ubo_id`, `cash_flag`, `point_card_definition_id`, `app_id`, `sort`, `direct_status`, `reserve_days_ago`, `ordee_flag`, `start_diff_time`, `end_diff_time`, `custom_shop_id`, `integrate_google_flag`, `camel_flag`, `invoice_id`, `zip_code`, `picks_charge_rate`)
VALUES
-- 店名 
('サーティワンアイスクリーム 高槻別所', 
0, 0, 'カラフルで種類豊富なフレーバーのアイスで有名なアイスクリーム チェーン店です。\n※PICKSからの注文はアイスマイルの付与対象外となりますのでご了承ください。', '', 'https://picks-public.s3-ap-northeast-1.amazonaws.com/uploads/8/06b3a8a2f9f4fee297d4f8a1ccbf0a6d', 8, 1, 0, '#z-31ice', '31ice', 1800, 'B-Rサーティワンアイスクリーム株式会社', '代表取締役会長 兼 社長CEO ジョン・キム', '', '03-3449-0336', 0, '', '', '', 1800, NULL, NULL, 0, 2359, 1, NULL, 13, NULL, NULL, NULL, NULL, NULL, NULL, 1800, '[\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"\"]', 0, 0, 1, NULL, NULL, NULL, 1, NULL, 31, NULL, 2, 14, 1, 3600, 3600, 
-- 店番
4573, 0, 0, NULL, '', 8.00);
*/


-- SELECT * FROM shops WHERE NAME LIKE "%三田ロードサイド%"
SELECT id, name,custom_shop_id FROM shops WHERE custom_shop_id IN (4562,4563,4564,4565,4566,4567,4568,4569,4570,4571,4572,4573)
-- LIMIT 100
