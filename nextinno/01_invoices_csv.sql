with raw_data as (
    SELECT
        usr.id AS "ユーザーID",
        i.id AS "請求ID",
        case i.payment_method_id
            when 1 then 'クレジットカード'
            when 2 then 'NP後払い'
            when 3 then '銀行振り込み'
            when 4 then '代引き'
            when 5 then 'クロネコ後払い'
            when 6 then 'forBiz払い'
        end as "支払い方法",
        shipAddr.prefecture AS "配送先_都道府県",
        i.shipped_at AS "出荷日時",
        i.refunded_at AS "払い戻し日時",
        mv.prescription_name AS "sku_処方名",
        ex.id AS "診察ID",
        chargeDocProf.family_name||' '||chargeDocProf.given_name AS "担当医_氏名",
        chargeDocCli.corporate_name AS "担当医_クリニック_医療法人名",
        chargeDoc.id AS "担当医ID",
        chargeDocCli.id as "担当医_クリニックID",
        i.smaluna_for_biz_company_id as "for Biz 企業ID",
        pp.name AS "定期便プラン名",
        licd.discount_amount AS "クーポン値引額",
        mv.discount_amount AS "キャンペーン値引額",
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
        trunc((li.price + li.prescription_fee + mv.discount_amount)/1.1,0) AS "値引分加算GMV_税抜き価格",
        i.position_per_prescription AS "請求回数/処方",
        (SELECT COUNT(ii.id) FROM kaguya_production.invoices AS ii
            WHERE ii.user_id = i.user_id AND ii.migration_flg = 0 AND ii.state >= 7 AND ii.shipped_at IS NOT NULL AND ii.id <= i.id) as "出荷回数/全体",
        (SELECT COUNT(ii.id) FROM kaguya_production.invoices AS ii
            JOIN kaguya_production.line_items AS li2 ON li2.invoice_id = ii.id
            JOIN kaguya_production.medicine_variants AS mv2 ON mv2.id = li2.medicine_variant_id
            JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (1,2,3,4)
            WHERE ii.user_id = i.user_id AND ii.migration_flg = 0 AND ii.state >= 7 AND ii.shipped_at IS NOT NULL AND ii.id <= i.id) AS "出荷回数/ピル",
        (SELECT COUNT(ii.id) FROM kaguya_production.invoices AS ii
            JOIN kaguya_production.line_items AS li2 ON li2.invoice_id = ii.id
            JOIN kaguya_production.medicine_variants AS mv2 ON mv2.id = li2.medicine_variant_id
            JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (10)
            WHERE ii.user_id = i.user_id AND ii.migration_flg = 0 AND ii.state >= 7 AND ii.shipped_at IS NOT NULL AND ii.id <= i.id) AS "出荷回数/ダイエット",
        (SELECT COUNT(ii.id) FROM kaguya_production.invoices AS ii
            JOIN kaguya_production.line_items AS li2 ON li2.invoice_id = ii.id
            JOIN kaguya_production.medicine_variants AS mv2 ON mv2.id = li2.medicine_variant_id
            JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (5,6,7,8,9)
            WHERE ii.user_id = i.user_id AND ii.migration_flg = 0 AND ii.state >= 7 AND ii.shipped_at IS NOT NULL AND ii.id <= i.id) AS "出荷回数/クロスセル",
        (li.price + li.prescription_fee - COALESCE(liobd.discount_amount, 0) - COALESCE(licd.discount_amount, 0)) AS "請求金額",
        ROW_NUMBER() OVER(partition by i.id order by med.position) as "同梱数",
        liobd.discount_amount AS "for Biz 企業負担額",
        iob.ratio AS "for Biz 企業負担割合(%)",
        (li.price + li.prescription_fee + mv.discount_amount) AS "値引分加算GMV",
        DATEDIFF(YEAR, usrProf.birthday,current_date) AS "年齢",
        mCat.id AS "薬剤カテゴリID",

        /* 06_薬名 */
        CASE 
            WHEN LEFT(sku_処方名, 4) = 'ルナベル' THEN 'ルナベル'
            WHEN LEFT(sku_処方名, 6) = 'ヤーズ配合錠' THEN 'ヤーズ配合錠'
            WHEN LEFT(sku_処方名, 8) = 'ヤーズフレックス' THEN 'ヤーズフレックス'
            WHEN LEFT(sku_処方名, 5) = 'フリウェル' THEN 'フリウェル'
            WHEN LEFT(sku_処方名, 4) = 'ドロエチ' THEN 'ドロエチ'
            WHEN LEFT(sku_処方名, 7) = 'ラベルフィーユ' THEN 'ラベルフィーユ'
            WHEN LEFT(sku_処方名, 6) = 'トリキュラー' THEN 'トリキュラー'
            WHEN LEFT(sku_処方名, 4) = 'アンジュ' THEN 'アンジュ'
            WHEN LEFT(sku_処方名, 5) = 'マーベロン' THEN 'マーベロン'
            WHEN LEFT(sku_処方名, 6) = 'ファボワール' THEN 'ファボワール'
            WHEN LEFT(sku_処方名, 6) = 'プラノバール' THEN 'プラノバール'
            WHEN LEFT(sku_処方名, 4) = 'レボノル' THEN 'レボノル'
            WHEN LEFT(sku_処方名, 4) = 'ノルレボ' THEN 'ノルレボ'
            WHEN LEFT(sku_処方名, 8) = 'ラピッドエスピー' THEN 'ラピッドエスピー'
            WHEN LEFT(sku_処方名, 6) = 'プリンペラン' THEN 'プリンペラン'
            WHEN LEFT(sku_処方名, 5) = 'ナウゼリン' THEN 'ナウゼリン'
            WHEN sku_処方名 = '診察料/通常料金' THEN '診察代'
            WHEN RIGHT(sku_処方名, 2) = '特典' THEN '特典'
            WHEN sku_処方名 = 'デエビゴ錠5mg 1T 分1 30日分' THEN 'デエビゴ'
            WHEN sku_処方名 = 'ルネスタ錠2mg 1T 分1 30日分' THEN 'ルネスタ'
            WHEN sku_処方名 = 'ラメルテオン錠「JG」8mg 1T 分1 30日分' THEN 'ラメルテオン'
            WHEN sku_処方名 = '酸化マグネシウム錠250mg「ケンエー」 3T 分3 30日分' THEN '酸化マグネシウム'
            WHEN sku_処方名 = 'ミヤBM錠 3T 分3 30日分' THEN 'ミヤBM'
            WHEN sku_処方名 = 'グーフィス錠5mg 2T 分1 30日分' THEN 'グーフィス'
            WHEN sku_処方名 = 'ツムラ 当帰芍薬散エキス顆粒 7.5g 分3 28日分' THEN '当帰芍薬散'
            WHEN sku_処方名 = 'ツムラ 桂枝茯苓丸エキス顆粒 7.5g 分3 28日分' THEN '桂枝茯苓丸'
            WHEN sku_処方名 = 'ツムラ 加味逍遙散料エキス顆粒 7.5g 分3 28日分' THEN '加味逍遙散料'
            WHEN sku_処方名 = 'ツムラ 当帰四逆加呉茱萸生姜湯7.5g 分3 28日分' THEN '当帰四逆加呉茱萸生姜湯'
            WHEN sku_処方名 = 'ツムラ 五苓散料エキス顆粒 7.5g 分3 28日分' THEN '五苓散料'
            WHEN sku_処方名 = 'ツムラ 防風通聖散エキス顆粒 7.5g 分3 28日分' THEN '防風通聖散料'
            WHEN LEFT(sku_処方名, 5) = 'リベルサス' THEN 'リベルサス'
            ELSE ''
        END AS "薬名",

        /* コース分類1 */
        CASE 
            WHEN RIGHT(sku_処方名, 16) = '次月以降1シートずつ12回分割)' THEN '旧安心定期'
            WHEN RIGHT(sku_処方名, 12) = '1シートずつ12回分割)' THEN '安心定期1ヶ月'
            WHEN RIGHT(sku_処方名, 17) = '1シートずつ12回分割) (CP)' THEN '安心定期1ヶ月'
            WHEN RIGHT(sku_処方名, 11) = '3シートずつ4回分割)' THEN '安心定期3ヶ月'
            WHEN RIGHT(sku_処方名, 16) = '3シートずつ4回分割) (CP)' THEN '安心定期3ヶ月'
            WHEN RIGHT(sku_処方名, 8) = '12シート一括)' THEN '安心定期12ヶ月'
            WHEN RIGHT(sku_処方名, 13) = '12シート一括) (CP)' THEN '安心定期12ヶ月'
            WHEN LEFT(sku_処方名, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(sku_処方名, 3) = '【3】' THEN '3ヶ月'
            WHEN RIGHT(sku_処方名, 6) = '1 28日分' OR RIGHT(sku_処方名, 4) = '21日分' THEN '1ヶ月'
            WHEN LEFT(sku_処方名, 4) = 'ノルレボ' OR LEFT(sku_処方名, 4) = 'レボノル' THEN '緊急避妊'
            WHEN LEFT(sku_処方名, 6) = 'プリンペラン' OR LEFT(sku_処方名, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(sku_処方名, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN sku_処方名 = '診察料/通常料金' THEN '診察代'
            WHEN 薬剤カテゴリid = 5 THEN '生理'
            WHEN 薬剤カテゴリid = 6 THEN '冷え・むくみ'
            WHEN 薬剤カテゴリid = 7 THEN '便秘・肥満'
            WHEN 薬剤カテゴリid = 8 THEN '睡眠'
            WHEN 薬剤カテゴリid = 9 THEN '便秘'
            WHEN RIGHT(sku_処方名, 2) = '特典' THEN '特典'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット単発6ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット単発6ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット単発6ヶ月'
            ELSE 'N/A'
        END AS "コース分類1",

        /* コース分類2 */
        CASE 
            WHEN RIGHT(sku_処方名, 16) = '次月以降1シートずつ12回分割)' THEN '旧定期便'
            WHEN RIGHT(sku_処方名, 12) = '1シートずつ12回分割)' OR RIGHT(sku_処方名, 11) = '3シートずつ4回分割)' OR RIGHT(sku_処方名, 8) = '12シート一括)' THEN '新定期便'
            WHEN RIGHT(sku_処方名, 17) = '1シートずつ12回分割) (CP)' OR RIGHT(sku_処方名, 16) = '3シートずつ4回分割) (CP)' OR RIGHT(sku_処方名, 13) = '12シート一括) (CP)' THEN '新定期便'
            WHEN LEFT(sku_処方名, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(sku_処方名, 3) = '【3】' OR RIGHT(sku_処方名, 6) = '1 28日分' OR RIGHT(sku_処方名, 4) = '21日分' THEN 'その他単発'
            WHEN LEFT(sku_処方名, 4) = 'ノルレボ' OR LEFT(sku_処方名, 4) = 'レボノル' THEN '緊急避妊'
            WHEN LEFT(sku_処方名, 6) = 'プリンペラン' OR LEFT(sku_処方名, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(sku_処方名, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN sku_処方名 = '診察料/通常料金' THEN '診察代'
            WHEN 薬剤カテゴリid = 5 THEN '生理'
            WHEN 薬剤カテゴリid = 6 THEN '冷え・むくみ'
            WHEN 薬剤カテゴリid = 7 THEN '便秘・肥満'
            WHEN 薬剤カテゴリid = 8 THEN '睡眠'
            WHEN 薬剤カテゴリid = 9 THEN '便秘'
            WHEN RIGHT(sku_処方名, 2) = '特典' THEN '特典'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'ダイエット単発'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 30日分' THEN 'ダイエット単発'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 30日分' THEN 'ダイエット単発'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期'
            ELSE 'N/A'
        END AS "コース分類2",

        /* コース分類3 */
        CASE 
            WHEN LEFT(sku_処方名, 4) = 'アンジュ' OR LEFT(sku_処方名, 6) = 'トリキュラー' OR LEFT(sku_処方名, 6) = 'ファボワール' 
                OR LEFT(sku_処方名, 5) = 'マーベロン' OR LEFT(sku_処方名, 7) = 'ラベルフィーユ' THEN '低用量'
            WHEN LEFT(sku_処方名, 5) = 'フリウェル' OR LEFT(sku_処方名, 4) = 'ドロエチ' OR LEFT(sku_処方名, 8) = 'ヤーズフレックス' 
                OR LEFT(sku_処方名, 6) = 'ヤーズ配合錠' OR LEFT(sku_処方名, 7) = 'ルナベル配合錠' THEN '超低用量'
            WHEN LEFT(sku_処方名, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(sku_処方名, 3) = '【3】' OR RIGHT(sku_処方名, 6) = '1 28日分' OR RIGHT(sku_処方名, 4) = '21日分' THEN 'その他単発'
            WHEN LEFT(sku_処方名, 4) = 'ノルレボ' OR LEFT(sku_処方名, 4) = 'レボノル' THEN '緊急避妊'
            WHEN LEFT(sku_処方名, 6) = 'プリンペラン' OR LEFT(sku_処方名, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(sku_処方名, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN 薬剤カテゴリid = 5 THEN '生理'
            WHEN 薬剤カテゴリid = 6 THEN '冷え・むくみ'
            WHEN 薬剤カテゴリid = 7 THEN '便秘・肥満'
            WHEN 薬剤カテゴリid = 8 THEN '睡眠'
            WHEN 薬剤カテゴリid = 9 THEN '便秘'
            WHEN sku_処方名 = '診察料/通常料金' THEN '診察代'
            WHEN RIGHT(sku_処方名, 2) = '特典' THEN '特典'
            WHEN LEFT(sku_処方名, 6) = 'リベルサス3' THEN 'リベルサス3mg'
            WHEN LEFT(sku_処方名, 6) = 'リベルサス7' THEN 'リベルサス7mg'
            WHEN LEFT(sku_処方名, 7) = 'リベルサス14' THEN 'リベルサス14mg'
            ELSE 'N/A'
        END AS "コース分類3",

        /* コース分類4 */
        CASE 
            WHEN RIGHT(sku_処方名, 16) = '次月以降1シートずつ12回分割)' THEN '1ヶ月'
            WHEN RIGHT(sku_処方名, 12) = '1シートずつ12回分割)' THEN '1ヶ月'
            WHEN RIGHT(sku_処方名, 17) = '1シートずつ12回分割) (CP)' THEN '1ヶ月'
            WHEN RIGHT(sku_処方名, 11) = '3シートずつ4回分割)' THEN '3ヶ月'
            WHEN RIGHT(sku_処方名, 16) = '3シートずつ4回分割) (CP)' THEN '3ヶ月'
            WHEN RIGHT(sku_処方名, 8) = '12シート一括)' THEN '12ヶ月'
            WHEN RIGHT(sku_処方名, 13) = '12シート一括) (CP)' THEN '12ヶ月'
            WHEN LEFT(sku_処方名, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(sku_処方名, 3) = '【3】' THEN '3ヶ月'
            WHEN RIGHT(sku_処方名, 6) = '1 28日分' OR RIGHT(sku_処方名, 4) = '21日分' THEN '1ヶ月'
            WHEN LEFT(sku_処方名, 4) = 'ノルレボ' OR LEFT(sku_処方名, 4) = 'レボノル' THEN '緊急避妊'
            WHEN LEFT(sku_処方名, 6) = 'プリンペラン' OR LEFT(sku_処方名, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(sku_処方名, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN sku_処方名 = '診察料/通常料金' THEN '診察代'
            WHEN 薬剤カテゴリid = 5 THEN '生理'
            WHEN 薬剤カテゴリid = 6 THEN '冷え・むくみ'
            WHEN 薬剤カテゴリid = 7 THEN '便秘・肥満'
            WHEN 薬剤カテゴリid = 8 THEN '睡眠'
            WHEN 薬剤カテゴリid = 9 THEN '便秘'
            WHEN RIGHT(sku_処方名, 2) = '特典' THEN '特典'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'リベルサス3mg単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'リベルサス3mgサブスク1ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'リベルサス3mgサブスク3ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'リベルサス3mgサブスク6ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 30日分' THEN 'リベルサス7mg単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'リベルサス7mgサブスク1ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'リベルサス7mgサブスク3ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'リベルサス7mgサブスク6ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 30日分' THEN 'リベルサス14mg単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'リベルサス14mgサブスク1ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'リベルサス14mgサブスク3ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'リベルサス14mgサブスク6ヶ月'
            ELSE 'N/A'
        END AS "コース分類4",

        /* 処方コース */
        CASE 
            WHEN RIGHT(sku_処方名, 16) = '次月以降1シートずつ12回分割)' THEN '安心定期'
            WHEN RIGHT(sku_処方名, 12) = '1シートずつ12回分割)' THEN '安心定期1ヶ月'
            WHEN RIGHT(sku_処方名, 17) = '1シートずつ12回分割) (CP)' THEN '安心定期1ヶ月'
            WHEN RIGHT(sku_処方名, 11) = '3シートずつ4回分割)' THEN '安心定期3ヶ月'
            WHEN RIGHT(sku_処方名, 16) = '3シートずつ4回分割) (CP)' THEN '安心定期3ヶ月'
            WHEN RIGHT(sku_処方名, 8) = '12シート一括)' THEN '安心定期12ヶ月'
            WHEN RIGHT(sku_処方名, 13) = '12シート一括) (CP)' THEN '安心定期12ヶ月'
            WHEN LEFT(sku_処方名, 6) = 'プラノバール' THEN '中用量'
            WHEN RIGHT(sku_処方名, 3) = '【3】' THEN '3ヶ月'
            WHEN RIGHT(sku_処方名, 6) = '1 28日分' OR RIGHT(sku_処方名, 4) = '21日分' THEN '1ヶ月'
            WHEN LEFT(sku_処方名, 4) = 'ノルレボ' OR LEFT(sku_処方名, 4) = 'レボノル' THEN '緊急避妊'
            WHEN LEFT(sku_処方名, 6) = 'プリンペラン' OR LEFT(sku_処方名, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(sku_処方名, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN sku_処方名 = '診察料/通常料金' THEN '診察代'
            WHEN RIGHT(sku_処方名, 2) = '特典' THEN '特典'
            WHEN 薬剤カテゴリid >= 5 AND 薬剤カテゴリid <= 9 THEN 'クロスセル'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN sku_処方名 = 'リベルサス3mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期6ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN sku_処方名 = 'リベルサス7mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期6ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 30日分' THEN 'ダイエット単発1ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (3シートずつ12回分割)' THEN 'ダイエット定期1ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (9シートずつ4回分割)' THEN 'ダイエット定期3ヶ月'
            WHEN sku_処方名 = 'リベルサス14mg30錠 1T 分1 360日分 (18シートずつ2回分割)' THEN 'ダイエット定期6ヶ月'
            ELSE 'N/A'
        END AS "処方コース",

        /* ピル種類 */
        CASE 
            WHEN RIGHT(sku_処方名, 16) = '次月以降1シートずつ12回分割)' THEN '安心定期'
            WHEN RIGHT(sku_処方名, 12) = '1シートずつ12回分割)' OR RIGHT(sku_処方名, 11) = '3シートずつ4回分割)' OR RIGHT(sku_処方名, 8) = '12シート一括)' THEN '安心定期'
            WHEN RIGHT(sku_処方名, 17) = '1シートずつ12回分割) (CP)' OR RIGHT(sku_処方名, 16) = '3シートずつ4回分割) (CP)' OR RIGHT(sku_処方名, 13) = '12シート一括) (CP)' THEN '安心定期'
            WHEN LEFT(sku_処方名, 5) = 'フリウェル' THEN '低用量'
            WHEN LEFT(sku_処方名, 3) = 'ヤーズ' THEN '低用量'
            WHEN LEFT(sku_処方名, 4) = 'ルナベル' THEN '低用量'
            WHEN LEFT(sku_処方名, 4) = 'アンジュ' THEN '低用量'
            WHEN LEFT(sku_処方名, 6) = 'トリキュラー' THEN '低用量'
            WHEN LEFT(sku_処方名, 6) = 'ファボワール' THEN '低用量'
            WHEN LEFT(sku_処方名, 5) = 'マーベロン' THEN '低用量'
            WHEN LEFT(sku_処方名, 7) = 'ラベルフィーユ' THEN '低用量'
            WHEN LEFT(sku_処方名, 4) = 'ドロエチ' THEN '低用量'
            WHEN LEFT(sku_処方名, 6) = 'プラノバール' THEN '中用量'
            WHEN LEFT(sku_処方名, 4) = 'ノルレボ' OR LEFT(sku_処方名, 4) = 'レボノル' THEN '緊急避妊'
            WHEN LEFT(sku_処方名, 6) = 'プリンペラン' OR LEFT(sku_処方名, 5) = 'ナウゼリン' THEN 'その他'
            WHEN LEFT(sku_処方名, 8) = 'ラピッドエスピー' THEN 'その他（感染症）'
            WHEN sku_処方名 = '診察料/通常料金' THEN '診察代'
            WHEN 薬剤カテゴリid >= 5 AND 薬剤カテゴリid <= 9 THEN 'クロスセル'
            WHEN 薬剤カテゴリid = 10 THEN 'ダイエット'
            WHEN RIGHT(sku_処方名, 2) = '特典' THEN '特典'
            ELSE 'N/A'
        END AS "ピル種類",

        /* 年代 */
        CASE 
            WHEN 年齢 >= 45 THEN '45~49'
            WHEN 年齢 >= 40 THEN '40~44'
            WHEN 年齢 >= 35 THEN '35~39'
            WHEN 年齢 >= 30 THEN '30~34'
            WHEN 年齢 >= 25 THEN '25~29'
            WHEN 年齢 >= 20 THEN '20~24'
            WHEN 年齢 >= 15 THEN '15~19'
            ELSE ''
        END AS "年代"

    FROM
        kaguya_production.invoices AS i
        
        /* line_items */
        LEFT JOIN kaguya_production.line_items AS li ON li.invoice_id = i.id
        LEFT JOIN kaguya_production.medicine_variants AS mv ON mv.id = li.medicine_variant_id
        LEFT JOIN kaguya_production.medicines AS med ON med.id = mv.medicine_id
        LEFT JOIN kaguya_production.medicine_categories AS mCat ON mCat.id = med.category_id
        LEFT JOIN kaguya_production.payment_plans AS pp ON mv.payment_plan_id = pp.id
        
        /* invoices organization_burden */
        LEFT JOIN kaguya_production.invoice_organization_burdens AS iob ON iob.invoice_id = i.id
        
        /* line_item organization_burden_discounts */
        LEFT JOIN kaguya_production.line_item_organization_burden_discounts AS liobd ON liobd.line_item_id = li.id
        
        /* line_item coupon_discounts */
        LEFT JOIN kaguya_production.line_item_coupon_discounts AS licd ON licd.line_item_id = li.id
        
        /* shipping address */
        LEFT JOIN kaguya_production.addresses AS shipAddr ON shipAddr.id = i.shipping_address_id
        
        /* customer */
        JOIN kaguya_production.users AS usr ON usr.id = i.user_id
        JOIN kaguya_production.user_profiles AS usr_prof ON usr_prof.user_id = usr.id
        JOIN kaguya_production.profiles AS usrProf ON usrProf.id = usr_prof.profile_id
        
        /* examination */
        JOIN kaguya_production.prescriptions AS pres ON pres.id = i.prescription_id
        JOIN kaguya_production.examinations AS ex ON ex.id = pres.examination_id
        
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
        
        /* charge doctor's clinic */
        LEFT JOIN kaguya_production.clinic_doctors AS cli_chargeDoc ON cli_chargeDoc.doctor_id = chargeDoc.id
        LEFT JOIN kaguya_production.clinics AS chargeDocCli ON chargeDocCli.id = cli_chargeDoc.clinic_id

    WHERE i.migration_flg = 0
    AND i.requests_on <= CURRENT_DATE 
    ORDER BY i.requests_on ASC
)

SELECT * from raw_data;
