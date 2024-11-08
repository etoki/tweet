WITH base_query AS (
    SELECT
        usr.id AS "ユーザーID",
        i.id AS "請求ID",
        COALESCE(
            CASE i.payment_method_id
                WHEN 1 THEN 'クレジットカード'
                WHEN 2 THEN 'NP後払い'
                WHEN 3 THEN '銀行振り込み'
                WHEN 4 THEN '代引き'
                WHEN 5 THEN 'クロネコ後払い'
                WHEN 6 THEN 'forBiz払い'
            END,
            'クーポン払い'
        ) AS "支払方法",
        shipAddr.prefecture AS "配送先 都道府県",
        CASE 
            WHEN RIGHT(mv.prescription_name, 16) = '次月以降1シートずつ12回分割)' THEN '安心定期'
            WHEN RIGHT(mv.prescription_name, 12) = '1シートずつ12回分割)' 
                OR RIGHT(mv.prescription_name, 11) = '3シートずつ4回分割)' 
                OR RIGHT(mv.prescription_name, 8) = '12シート一括)' THEN '安心定期'
            WHEN RIGHT(mv.prescription_name, 17) = '1シートずつ12回分割) (CP)' 
                OR RIGHT(mv.prescription_name, 16) = '3シートずつ4回分割) (CP)' 
                OR RIGHT(mv.prescription_name, 13) = '12シート一括) (CP)' THEN '安心定期'
            WHEN LEFT(mv.prescription_name, 5) = 'フリウェル' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 3) = 'ヤーズ' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 4) = 'ルナベル' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 4) = 'アンジュ' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 6) = 'トリキュラー' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 6) = 'ファボワール' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 5) = 'マーベロン' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 7) = 'ラベルフィーユ' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 4) = 'ドロエチ' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 6) = 'プラノバール' THEN '中用量'
            WHEN LEFT(mv.prescription_name, 4) IN ('ノルレボ', 'レボノル') THEN '緊急避妊'
            WHEN LEFT(mv.prescription_name, 6) = 'プリンペラン' 
                OR LEFT(mv.prescription_name, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(mv.prescription_name, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN mv.prescription_name = '診察料/通常料金' THEN '診察代'
            WHEN med.category_id BETWEEN 5 AND 9 THEN 'クロスセル'
            WHEN med.category_id = 10 THEN 'ダイエット'
            WHEN RIGHT(mv.prescription_name, 2) = '特典' THEN '特典'
            ELSE 'N/A'
        END AS "ピル種類",
        CASE 
            WHEN RIGHT(mv.prescription_name, 16) = '次月以降1シートずつ12回分割)' THEN '旧安心定期'
            WHEN RIGHT(mv.prescription_name, 12) = '1シートずつ12回分割)' THEN '安心定期1ヶ月'
            WHEN RIGHT(mv.prescription_name, 17) = '1シートずつ12回分割) (CP)' THEN '安心定期1ヶ月'
            WHEN RIGHT(mv.prescription_name, 11) = '3シートずつ4回分割)' THEN '安心定期3ヶ月'
            WHEN RIGHT(mv.prescription_name, 16) = '3シートずつ4回分割) (CP)' THEN '安心定期3ヶ月'
            WHEN RIGHT(mv.prescription_name, 8) = '12シート一括)' THEN '安心定期12ヶ月'
            WHEN RIGHT(mv.prescription_name, 13) = '12シート一括) (CP)' THEN '安心定期12ヶ月'
            WHEN LEFT(mv.prescription_name, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(mv.prescription_name, 3) = '【3】' THEN '3ヶ月'
            WHEN RIGHT(mv.prescription_name, 6) = '1 28日分' OR RIGHT(mv.prescription_name, 4) = '21日分' THEN '1ヶ月'
            WHEN LEFT(mv.prescription_name, 4) IN ('ノルレボ', 'レボノル') THEN '緊急避妊'
            WHEN LEFT(mv.prescription_name, 6) = 'プリンペラン' OR LEFT(mv.prescription_name, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(mv.prescription_name, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN mv.prescription_name = '診察料/通常料金' THEN '診察代'
            WHEN med.category_id = 5 THEN '生理'
            WHEN med.category_id = 6 THEN '冷え・むくみ'
            WHEN med.category_id = 7 THEN '便秘・肥満'
            WHEN med.category_id = 8 THEN '睡眠'
            WHEN med.category_id = 9 THEN '便秘'
            WHEN RIGHT(mv.prescription_name, 2) = '特典' THEN '特典'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット単発6ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット単発6ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット単発6ヶ月'
            ELSE 'N/A'
        END AS "コース分類1",
        CASE 
            WHEN RIGHT(mv.prescription_name, 16) = '次月以降1シートずつ12回分割)' THEN '旧定期便'
            WHEN RIGHT(mv.prescription_name, 12) = '1シートずつ12回分割)' 
                OR RIGHT(mv.prescription_name, 11) = '3シートずつ4回分割)' 
                OR RIGHT(mv.prescription_name, 8) = '12シート一括)' THEN '新定期便'
            WHEN RIGHT(mv.prescription_name, 17) = '1シートずつ12回分割) (CP)' 
                OR RIGHT(mv.prescription_name, 16) = '3シートずつ4回分割) (CP)' 
                OR RIGHT(mv.prescription_name, 13) = '12シート一括) (CP)' THEN '新定期便'
            WHEN LEFT(mv.prescription_name, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(mv.prescription_name, 3) = '【3】' 
                OR RIGHT(mv.prescription_name, 6) = '1 28日分' 
                OR RIGHT(mv.prescription_name, 4) = '21日分' THEN 'その他単発'
            WHEN LEFT(mv.prescription_name, 4) IN ('ノルレボ', 'レボノル') THEN '緊急避妊'
            WHEN LEFT(mv.prescription_name, 6) = 'プリンペラン' 
                OR LEFT(mv.prescription_name, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(mv.prescription_name, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN mv.prescription_name = '診察料/通常料金' THEN '診察代'
            WHEN med.category_id = 5 THEN '生理'
            WHEN med.category_id = 6 THEN '冷え・むくみ'
            WHEN med.category_id = 7 THEN '便秘・肥満'
            WHEN med.category_id = 8 THEN '睡眠'
            WHEN med.category_id = 9 THEN '便秘'
            WHEN RIGHT(mv.prescription_name, 2) = '特典' THEN '特典'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'ダイエット単発'
            WHEN mv.prescription_name IN (
                'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)',
                'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)',
                'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)',
                'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)',
                'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)',
                'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)',
                'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)',
                'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)',
                'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)'
            ) THEN 'ダイエット定期'
            WHEN mv.prescription_name IN (
                'リベルサス7mg30錠 1T 分1 30日分',
                'リベルサス14mg30錠 1T 分1 30日分'
            ) THEN 'ダイエット単発'
            ELSE 'N/A'
        END AS "コース分類2",
        CASE 
            WHEN LEFT(mv.prescription_name, 4) = 'アンジュ' 
                OR LEFT(mv.prescription_name, 6) = 'トリキュラー'
                OR LEFT(mv.prescription_name, 6) = 'ファボワール'
                OR LEFT(mv.prescription_name, 5) = 'マーベロン'
                OR LEFT(mv.prescription_name, 7) = 'ラベルフィーユ' THEN '低用量'
            WHEN LEFT(mv.prescription_name, 5) = 'フリウェル'
                OR LEFT(mv.prescription_name, 4) = 'ドロエチ'
                OR LEFT(mv.prescription_name, 8) = 'ヤーズフレックス'
                OR LEFT(mv.prescription_name, 6) = 'ヤーズ配合錠'
                OR LEFT(mv.prescription_name, 7) = 'ルナベル配合錠' THEN '超低用量'
            WHEN LEFT(mv.prescription_name, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(mv.prescription_name, 3) = '【3】'
                OR RIGHT(mv.prescription_name, 6) = '1 28日分'
                OR RIGHT(mv.prescription_name, 4) = '21日分' THEN 'その他単発'
            WHEN LEFT(mv.prescription_name, 4) IN ('ノルレボ', 'レボノル') THEN '緊急避妊'
            WHEN LEFT(mv.prescription_name, 6) = 'プリンペラン'
                OR LEFT(mv.prescription_name, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(mv.prescription_name, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN med.category_id = 5 THEN '生理'
            WHEN med.category_id = 6 THEN '冷え・むくみ'
            WHEN med.category_id = 7 THEN '便秘・肥満'
            WHEN med.category_id = 8 THEN '睡眠'
            WHEN med.category_id = 9 THEN '便秘'
            WHEN mv.prescription_name = '診察料/通常料金' THEN '診察代'
            WHEN RIGHT(mv.prescription_name, 2) = '特典' THEN '特典'
            WHEN LEFT(mv.prescription_name, 6) = 'リベルサス3' THEN 'リベルサス3mg'
            WHEN LEFT(mv.prescription_name, 6) = 'リベルサス7' THEN 'リベルサス7mg'
            WHEN LEFT(mv.prescription_name, 7) = 'リベルサス14' THEN 'リベルサス14mg'
            ELSE 'N/A'
        END AS "コース分類3",
        CASE 
            -- まず最初に評価する項目
            WHEN RIGHT(mv.prescription_name, 12) = '1シートずつ12回分割)' 
                OR RIGHT(mv.prescription_name, 17) = '1シートずつ12回分割) (CP)' 
                OR RIGHT(mv.prescription_name, 16) = '次月以降1シートずつ12回分割)' 
                OR RIGHT(mv.prescription_name, 6) = '1 28日分' 
                OR RIGHT(mv.prescription_name, 4) = '21日分' THEN '1ヶ月'
            WHEN RIGHT(mv.prescription_name, 11) = '3シートずつ4回分割)' 
                OR RIGHT(mv.prescription_name, 16) = '3シートずつ4回分割) (CP)' 
                OR RIGHT(mv.prescription_name, 3) = '【3】' THEN '3ヶ月'
            WHEN RIGHT(mv.prescription_name, 8) = '12シート一括)' 
                OR RIGHT(mv.prescription_name, 13) = '12シート一括) (CP)' THEN '12ヶ月'
            WHEN LEFT(mv.prescription_name, 6) = 'プラノバール' THEN '中用量'
            WHEN LEFT(mv.prescription_name, 4) IN ('ノルレボ', 'レボノル') THEN '緊急避妊'
            -- リベルサス関連の条件
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'リベルサス3mg単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'リベルサス3mgサブスク1ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'リベルサス3mgサブスク3ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'リベルサス3mgサブスク6ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 30日分' THEN 'リベルサス7mg単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'リベルサス7mgサブスク1ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'リベルサス7mgサブスク3ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'リベルサス7mgサブスク6ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 30日分' THEN 'リベルサス14mg単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'リベルサス14mgサブスク1ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'リベルサス14mgサブスク3ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'リベルサス14mgサブスク6ヶ月'
            -- その他のカテゴリ
            WHEN med.category_id = 5 THEN '生理'
            WHEN med.category_id = 9 THEN '便秘'
            WHEN med.category_id = 7 THEN '便秘・肥満'
            WHEN med.category_id = 6 THEN '冷え・むくみ'
            WHEN med.category_id = 8 THEN '睡眠'
            WHEN LEFT(mv.prescription_name, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN LEFT(mv.prescription_name, 6) = 'プリンペラン' 
                OR LEFT(mv.prescription_name, 5) = 'ナウゼリン' THEN 'その他'
            WHEN RIGHT(mv.prescription_name, 2) = '特典' THEN '特典'
            WHEN mv.prescription_name = '診察料/通常料金' THEN '診察代'
            ELSE 'N/A'
        END AS "コース分類4",
        CASE 
            WHEN RIGHT(mv.prescription_name, 16) = '次月以降1シートずつ12回分割)' THEN '安心定期'
            WHEN RIGHT(mv.prescription_name, 12) = '1シートずつ12回分割)' THEN '安心定期1ヶ月'
            WHEN RIGHT(mv.prescription_name, 17) = '1シートずつ12回分割) (CP)' THEN '安心定期1ヶ月'
            WHEN RIGHT(mv.prescription_name, 11) = '3シートずつ4回分割)' THEN '安心定期3ヶ月'
            WHEN RIGHT(mv.prescription_name, 16) = '3シートずつ4回分割) (CP)' THEN '安心定期3ヶ月'
            WHEN RIGHT(mv.prescription_name, 8) = '12シート一括)' THEN '安心定期12ヶ月'
            WHEN RIGHT(mv.prescription_name, 13) = '12シート一括) (CP)' THEN '安心定期12ヶ月'
            WHEN LEFT(mv.prescription_name, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(mv.prescription_name, 3) = '【3】' THEN '3ヶ月'
            WHEN RIGHT(mv.prescription_name, 6) = '1 28日分' OR RIGHT(mv.prescription_name, 4) = '21日分' THEN '1ヶ月'
            WHEN LEFT(mv.prescription_name, 4) IN ('ノルレボ', 'レボノル') THEN '緊急避妊'
            WHEN LEFT(mv.prescription_name, 6) = 'プリンペラン' OR LEFT(mv.prescription_name, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(mv.prescription_name, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN mv.prescription_name = '診察料/通常料金' THEN '診察代'
            WHEN RIGHT(mv.prescription_name, 2) = '特典' THEN '特典'
            WHEN med.category_id BETWEEN 5 AND 9 THEN 'クロスセル'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN mv.prescription_name = 'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期6ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN mv.prescription_name = 'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期6ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN mv.prescription_name = 'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期6ヶ月'
            ELSE 'N/A'
        END AS "処方コース",
        CASE 
            WHEN LEFT(mv.prescription_name, 4) = 'ルナベル' THEN 'ルナベル'
            WHEN LEFT(mv.prescription_name, 6) = 'ヤーズ配合錠' THEN 'ヤーズ配合錠'
            WHEN LEFT(mv.prescription_name, 8) = 'ヤーズフレックス' THEN 'ヤーズフレックス'
            WHEN LEFT(mv.prescription_name, 5) = 'フリウェル' THEN 'フリウェル'
            WHEN LEFT(mv.prescription_name, 4) = 'ドロエチ' THEN 'ドロエチ'
            WHEN LEFT(mv.prescription_name, 7) = 'ラベルフィーユ' THEN 'ラベルフィーユ'
            WHEN LEFT(mv.prescription_name, 6) = 'トリキュラー' THEN 'トリキュラー'
            WHEN LEFT(mv.prescription_name, 4) = 'アンジュ' THEN 'アンジュ'
            WHEN LEFT(mv.prescription_name, 5) = 'マーベロン' THEN 'マーベロン'
            WHEN LEFT(mv.prescription_name, 6) = 'ファボワール' THEN 'ファボワール'
            WHEN LEFT(mv.prescription_name, 6) = 'プラノバール' THEN 'プラノバール'
            WHEN LEFT(mv.prescription_name, 4) = 'レボノル' THEN 'レボノル'
            WHEN LEFT(mv.prescription_name, 4) = 'ノルレボ' THEN 'ノルレボ'
            WHEN LEFT(mv.prescription_name, 8) = 'ラピッドエスピー' THEN 'ラピッドエスピー'
            WHEN LEFT(mv.prescription_name, 6) = 'プリンペラン' THEN 'プリンペラン'
            WHEN LEFT(mv.prescription_name, 5) = 'ナウゼリン' THEN 'ナウゼリン'
            WHEN mv.prescription_name = '診察料/通常料金' THEN '診察代'
            WHEN RIGHT(mv.prescription_name, 2) = '特典' THEN '特典'
            WHEN mv.prescription_name = 'デエビゴ錠5mg 1T 分1 30日分' THEN 'デエビゴ'
            WHEN mv.prescription_name = 'ルネスタ錠2mg 1T 分1 30日分' THEN 'ルネスタ'
            WHEN mv.prescription_name = 'ラメルテオン錠「JG」8mg 1T 分1 30日分' THEN 'ラメルテオン'
            WHEN mv.prescription_name = '酸化マグネシウム錠250mg「ケンエー」 3T 分3 30日分' THEN '酸化マグネシウム'
            WHEN mv.prescription_name = 'ミヤBM錠 3T 分3 30日分' THEN 'ミヤBM'
            WHEN mv.prescription_name = 'グーフィス錠5mg 2T 分1 30日分' THEN 'グーフィス'
            WHEN mv.prescription_name = 'ツムラ 当帰芍薬散エキス顆粒 7.5g 分3 28日分' THEN '当帰芍薬散'
            WHEN mv.prescription_name = 'ツムラ 桂枝茯苓丸エキス顆粒 7.5g 分3 28日分' THEN '桂枝茯苓丸'
            WHEN mv.prescription_name = 'ツムラ 加味逍遙散料エキス顆粒 7.5g 分3 28日分' THEN '加味逍遙散料'
            WHEN mv.prescription_name = 'ツムラ 当帰四逆加呉茱萸生姜湯7.5g 分3 28日分' THEN '当帰四逆加呉茱萸生姜湯'
            WHEN mv.prescription_name = 'ツムラ 五苓散料エキス顆粒 7.5g 分3 28日分' THEN '五苓散料'
            WHEN mv.prescription_name = 'ツムラ 防風通聖散エキス顆粒 7.5g 分3 28日分' THEN '防風通聖散料'
            WHEN LEFT(mv.prescription_name, 5) = 'リベルサス' THEN 'リベルサス'
            ELSE ''
        END AS "06_薬名",
        CAST(i.requests_on AS DATETIME) AS "請求日",
        CAST(i.shipped_at AS DATETIME) AS "出荷日時",
        i.refunded_at AS "払戻日時",
        mv.prescription_name AS "処方薬",
        ex.id AS "診察ID",
        chargeDocProf.family_name || ' ' || chargeDocProf.given_name AS "担当ドクター",
        chargeDocCli.corporate_name AS "医療法人名",
        chargeDoc.id AS "ドクターid",
        chargeDocCli.id AS "クリニックid",
        i.smaluna_for_biz_company_id AS "for Biz 企業ID",
        pp.name AS "定期便プラン名",
        COALESCE(licd.discount_amount, 0) AS "値引クーポン_税込",
        mv.discount_amount AS "値引キャンペーン_税込",
        CASE i.state
            WHEN 1 THEN '未決済'
            WHEN 2 THEN 'キャンセル'
            WHEN 3 THEN '審査中'
            WHEN 4 THEN '決済失敗'
            WHEN 5 THEN '決済済'
            WHEN 6 THEN '監査済'
            WHEN 7 THEN '発送済'
            WHEN 8 THEN '払い戻し済'
        END AS "請求ステータス",
        TRUNC((li.price + li.prescription_fee + mv.discount_amount)/1.1, 0) AS "GMV薬代_税抜",
        i.position_per_prescription AS "請求回数/処方",
        (SELECT COUNT(ii.id) 
        FROM kaguya_production.invoices AS ii
        WHERE ii.user_id = i.user_id 
        AND ii.migration_flg = 0 
        AND ii.state >= 7 
        AND ii.shipped_at IS NOT NULL 
        AND ii.id <= i.id) AS "出荷回数/全体",
        (SELECT COUNT(ii.id) 
        FROM kaguya_production.invoices AS ii
        JOIN kaguya_production.line_items AS li2 ON li2.invoice_id = ii.id
        JOIN kaguya_production.medicine_variants AS mv2 ON mv2.id = li2.medicine_variant_id
        JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (1,2,3,4)
        WHERE ii.user_id = i.user_id 
        AND ii.migration_flg = 0 
        AND ii.state >= 7 
        AND ii.shipped_at IS NOT NULL 
        AND ii.id <= i.id) AS "出荷回数/ピル",
        (SELECT COUNT(ii.id) 
        FROM kaguya_production.invoices AS ii
        JOIN kaguya_production.line_items AS li2 ON li2.invoice_id = ii.id
        JOIN kaguya_production.medicine_variants AS mv2 ON mv2.id = li2.medicine_variant_id
        JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (10)
        WHERE ii.user_id = i.user_id 
        AND ii.migration_flg = 0 
        AND ii.state >= 7 
        AND ii.shipped_at IS NOT NULL 
        AND ii.id <= i.id) AS "出荷回数/ダイエット",
        (SELECT COUNT(ii.id) 
        FROM kaguya_production.invoices AS ii
        JOIN kaguya_production.line_items AS li2 ON li2.invoice_id = ii.id
        JOIN kaguya_production.medicine_variants AS mv2 ON mv2.id = li2.medicine_variant_id
        JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (5,6,7,8,9)
        WHERE ii.user_id = i.user_id 
        AND ii.migration_flg = 0 
        AND ii.state >= 7 
        AND ii.shipped_at IS NOT NULL 
        AND ii.id <= i.id) AS "出荷回数/クロスセル",
        (li.price + li.prescription_fee - COALESCE(liobd.discount_amount, 0) - COALESCE(licd.discount_amount, 0)) AS "請求金額_raw",
        ROW_NUMBER() OVER(PARTITION BY i.id ORDER BY med.position) AS "同梱数",
        COALESCE(liobd.discount_amount, 0) AS "for biz 企業負担額",
        COALESCE(iob.ratio, 0) AS "for biz 企業負担割合(%)",
        DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) AS "年齢",
        CASE 
            WHEN DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) >= 45 THEN '45~49'
            WHEN DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) >= 40 THEN '40~44'
            WHEN DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) >= 35 THEN '35~39'
            WHEN DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) >= 30 THEN '30~34'
            WHEN DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) >= 25 THEN '25~29'
            WHEN DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) >= 20 THEN '20~24'
            WHEN DATEDIFF(YEAR, usrProf.birthday, CURRENT_DATE) >= 15 THEN '15~19'
            ELSE ''
        END AS "年代",
        CASE WHEN i.position_per_prescription = 1 THEN 1 ELSE 0 END AS "診察",
        CASE WHEN EXISTS (
            SELECT 1
            FROM kaguya_production.invoices i2
            LEFT JOIN kaguya_production.line_items li2 ON li2.invoice_id = i2.id
            LEFT JOIN kaguya_production.medicine_variants mv2 ON mv2.id = li2.medicine_variant_id
            WHERE i2.id = i.id 
            AND RIGHT(mv2.prescription_name, 2) = '特典'
        ) THEN 1 ELSE 0 END AS "特典",
        CASE WHEN (
            SELECT COUNT(ii.id) 
            FROM kaguya_production.invoices AS ii
            WHERE ii.user_id = i.user_id 
            AND ii.migration_flg = 0 
            AND ii.state >= 7 
            AND ii.shipped_at IS NOT NULL 
            AND ii.id <= i.id
        ) = 1 THEN 1 ELSE 0 END AS "新規",
        0 AS "GMV計_税抜",
        0 AS "GMV診察代_税抜",
        0 AS "値引キャンペーン_税抜",
        0 AS "値引クーポン_税抜",
        0 AS "値引特典_税抜",
        0 AS "請求金額_税抜",
        0 AS "GMV計_税込",
        0 AS "GMV薬代_税込",
        0 AS "値引特典_税込",
        0 AS "請求金額_税込",
        -- 最初の出荷日時を各ユーザーに対して取得し、それを初診年月日として使用
        FIRST_VALUE(
            CASE WHEN (
                SELECT COUNT(ii.id) 
                FROM kaguya_production.invoices AS ii
                WHERE ii.user_id = i.user_id 
                AND ii.migration_flg = 0 
                AND ii.state >= 7 
                AND ii.shipped_at IS NOT NULL 
                AND ii.id <= i.id
            ) = 1 THEN i.shipped_at END
        ) OVER (PARTITION BY usr.id ORDER BY i.shipped_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS "初診年月日",
        TO_CHAR(
            FIRST_VALUE(
                CASE WHEN (
                    SELECT COUNT(ii.id) 
                    FROM kaguya_production.invoices AS ii
                    WHERE ii.user_id = i.user_id 
                    AND ii.migration_flg = 0 
                    AND ii.state >= 7 
                    AND ii.shipped_at IS NOT NULL 
                    AND ii.id <= i.id
                ) = 1 THEN i.shipped_at END
            ) OVER (PARTITION BY usr.id ORDER BY i.shipped_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
            'YYYY-MM'
        ) AS "初診年月",
        -- 出荷年月の修正
        TO_CHAR(i.shipped_at, 'YYYY-MM') AS "出荷年月"

    FROM kaguya_production.invoices AS i
    LEFT JOIN kaguya_production.line_items AS li ON li.invoice_id = i.id
    LEFT JOIN kaguya_production.medicine_variants AS mv ON mv.id = li.medicine_variant_id
    LEFT JOIN kaguya_production.medicines AS med ON med.id = mv.medicine_id
    LEFT JOIN kaguya_production.addresses AS shipAddr ON shipAddr.id = i.shipping_address_id
    JOIN kaguya_production.users AS usr ON usr.id = i.user_id
    JOIN kaguya_production.user_profiles AS usr_prof ON usr_prof.user_id = usr.id
    JOIN kaguya_production.profiles AS usrProf ON usrProf.id = usr_prof.profile_id
    JOIN kaguya_production.prescriptions AS pres ON pres.id = i.prescription_id
    JOIN kaguya_production.examinations AS ex ON ex.id = pres.examination_id
    LEFT JOIN kaguya_production.payment_plans AS pp ON mv.payment_plan_id = pp.id
    LEFT JOIN kaguya_production.line_item_coupon_discounts AS licd ON licd.line_item_id = li.id
    LEFT JOIN kaguya_production.line_item_organization_burden_discounts AS liobd ON liobd.line_item_id = li.id
    LEFT JOIN kaguya_production.invoice_organization_burdens AS iob ON iob.invoice_id = i.id

    /* charge doctor */
    LEFT JOIN (
        SELECT icd1.invoice_id, icd1.doctor_id, icd1.assigns_on AS max_assigns_on
        FROM kaguya_production.invoice_charge_doctors AS icd1
        WHERE NOT EXISTS (
            SELECT 1
            FROM kaguya_production.invoice_charge_doctors AS icd2
            WHERE icd1.invoice_id = icd2.invoice_id
            AND icd2.assigns_on <= CURRENT_DATE
            AND icd1.assigns_on < icd2.assigns_on
        )
    ) AS currentIcd ON i.id = currentIcd.invoice_id
    LEFT JOIN kaguya_production.users AS chargeDoc ON chargeDoc.id = currentIcd.doctor_id
    LEFT JOIN kaguya_production.user_profiles AS chargeDoc_prof ON chargeDoc_prof.user_id = chargeDoc.id
    LEFT JOIN kaguya_production.profiles AS chargeDocProf ON chargeDocProf.id = chargeDoc_prof.profile_id
    LEFT JOIN kaguya_production.clinic_doctors AS cli_chargeDoc ON cli_chargeDoc.doctor_id = chargeDoc.id
    LEFT JOIN kaguya_production.clinics AS chargeDocCli ON chargeDocCli.id = cli_chargeDoc.clinic_id

    WHERE i.migration_flg = 0
    AND i.requests_on <= CURRENT_DATE 
    ORDER BY usr.id ASC, i.requests_on ASC
)

SELECT 
    base.*,
    CASE 
        WHEN base."コース分類4" = '診察代' THEN 0
        WHEN base."コース分類4" != '診察代' AND 
            base."コース分類4" = FIRST_VALUE(base."コース分類4") OVER (
                PARTITION BY base."請求ID" 
                ORDER BY base."コース分類4" 
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) THEN 
            FIRST_VALUE(
                CASE 
                    WHEN base."コース分類4" = '診察代' 
                    THEN (base."請求金額_raw" + base."値引クーポン_税込" + base."for biz 企業負担額")
                    ELSE NULL 
                END
            ) OVER (
                PARTITION BY base."請求ID" 
                ORDER BY 
                    CASE WHEN base."コース分類4" = '診察代' THEN 0 ELSE 1 END
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            )
        ELSE 0
    END AS "GMV診察代_税込"
FROM base_query base;
