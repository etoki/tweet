-- insert into coupons (title, description, price, status, custom_code, app_id, pos_code)
-- VALUES (`クーポン内容`, `利用条件`, `割引額（クーポン内容から）`, 1, `31ギフトID`, 31, `値引きコード`);

/*
INSERT INTO coupons (title, description, price, status, custom_code, app_id, pos_code) 
VALUES (
'フレッシュパックスーパー 400円OFF', 
'【クーポン内容】
フレッシュパックスーパーを400円OFFでご購入いただけます。

※店舗または31モバイルオーダーにて、いずれか1回のみ１コまでご利用いただけます。
※31デリバリー以外の各種デリバリーサービスではご利用いただけません。
※他のクーポン・特典との併用はできません。
※値引き、または増量キャンペーン商品にはご利用いただけません。
※高速道路SA内や映画館内などの一部店舗では、ご利用いただけません。
※フィーチャーフォン・パソコン・画面を印刷した紙、バーコードをスクリーンショットした画像ではご利用いただけません。',
400, 1, 229, 31, 83);
*/

-- 入ってるか確認
-- SELECT id,title, description, price, status, custom_code, app_id, pos_code, item_only_coupon_id FROM coupons ORDER BY id DESC LIMIT 50

-- item_only_coupon_id作成
-- SELECT * FROM item_only_coupons ORDER BY id DESC LIMIT 10;
-- insert into item_only_coupons (food_min, food_max, topping_min, topping_max) VALUES (1, NULL, 0, NULL);

-- food_only_coupons作成
-- SELECT * FROM food_only_coupons ORDER BY id DESC LIMIT 10;
-- insert into food_only_coupons (item_only_coupon_id, food_id) VALUES (82, 60301);


-- item_only_coupon_idをいれる
SELECT id,title, description, price, status, custom_code, app_id, pos_code, item_only_coupon_id FROM coupons ORDER BY id DESC LIMIT 50


