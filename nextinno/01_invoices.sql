SELECT
    i.migration_flg AS "migration_flg",
    i.id AS "請求ID",
    pres.id AS "処方ID",
    pres.created_at AS "処方提案日時",
    CASE pres.state
        WHEN 1 THEN '確認待ち' 
        WHEN 2 THEN '承認' 
        WHEN 3 THEN '否認' 
        WHEN 4 THEN '確定' 
    END AS "処方ステータス",
    i.created_at as "処方確定日時",
    case when mv.lots > 1 or mv.payment_plan_id IS NOT NULL then us.id end as "定期便ID",
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
    i.requests_on AS "請求日",
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
        JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (5,6,7,8,9)
        WHERE ii.user_id = i.user_id AND ii.migration_flg = 0 AND ii.state >= 7 AND ii.shipped_at IS NOT NULL AND ii.id <= i.id) AS "出荷回数/クロスセル",
    (SELECT COUNT(ii.id) FROM kaguya_production.invoices AS ii
        JOIN kaguya_production.line_items AS li2 ON li2.invoice_id = ii.id
        JOIN kaguya_production.medicine_variants AS mv2 ON mv2.id = li2.medicine_variant_id
        JOIN kaguya_production.medicines AS m2 ON m2.id = mv2.medicine_id AND m2.category_id IN (10)
        WHERE ii.user_id = i.user_id AND ii.migration_flg = 0 AND ii.state >= 7 AND ii.shipped_at IS NOT NULL AND ii.id <= i.id) AS "出荷回数/ダイエット",
    (SELECT COUNT(ii.id) FROM kaguya_production.invoices AS ii
        WHERE ii.user_id = i.user_id AND ii.migration_flg = 0 AND ii.state >= 7 AND ii.shipped_at IS NOT NULL AND i.shipped_at <= ii.shipped_at) as "最終出荷フラグ",
    ROW_NUMBER() OVER(partition by i.id order by med.position) as "同梱数",
    i.review_started_at AS "NP審査提出日時(最新)",    
    i.denied_at AS "決済失敗日時(最新)",
    i.paid_at AS "決済日時",
    i.audited_at AS "監査完了日時",
    i.shipped_at AS "出荷日時",
    i.canceled_at AS "キャンセル日時",
    i.refunded_at AS "払い戻し日時",
    
    case i.payment_method_id
        when 1 then 'クレジットカード'
        when 2 then 'NP後払い'
        when 3 then '銀行振り込み'
        when 4 then '代引き'
        when 5 then 'クロネコ後払い'
        when 6 then 'forBiz払い'
    end as "支払い方法",
    
    i.stripe_charge_id AS "Stripe決済ID",
    i.np_transaction_id AS "NP取引ID",
    i.smaluna_for_biz_company_id as "for Biz 企業ID",
    i.smaluna_for_biz_company_billing_exempted as "for Biz 請求免除",
        
    mCat.id AS "薬剤カテゴリID",
    mCat.name AS "薬剤カテゴリ名",
    med.id AS "薬剤ID",
    med.name AS "薬剤_表示名",
    mv.id AS "skuID",
    mv.sku AS "sku_表示名",
    mv.prescription_name AS "sku_処方名",
    pp.name AS "定期便プラン名",
    li.id AS "項目ID",
    case li.state
        when 1 then '---'
        when 2 then 'キャンセル'
        when 3 then '監査済'
        when 4 then '払い戻し'
    end AS "項目ステータス",
    li.updated_at AS "項目_最終更新日時",
    (li.price + li.prescription_fee - COALESCE(liobd.discount_amount, 0) - COALESCE(licd.discount_amount, 0)) AS "請求金額",
    (li.price + li.prescription_fee) AS "小計",
    liobd.discount_amount AS "for Biz 企業負担額",
    iob.ratio AS "for Biz 企業負担割合(%)",
    licd.discount_amount AS "クーポン値引額",
    mv.discount_amount AS "キャンペーン値引額",
    (li.price + li.prescription_fee + mv.discount_amount) AS "値引分加算GMV",
    trunc((li.price + li.prescription_fee + mv.discount_amount)/1.1,0) AS "値引分加算GMV_税抜き価格",
    (li.price + li.prescription_fee + mv.discount_amount)-trunc((li.price + li.prescription_fee + mv.discount_amount)/1.1,0) AS "値引分加算GMV_消費税",
    
    coup.id AS "クーポンID",
    coup.name AS "クーポン名",
    coup.key AS "クーポンkey",
    cac.code AS "クーポンコード",
    ex.id AS "診察ID",
    usr.id AS "ユーザーID",
    usr.email AS "メールアドレス",
    usrProf.family_name||' '||usrProf.given_name AS "氏名",
    usrProf.birthday AS "生年月日",
    ph.number as "電話番号",
    DATEDIFF(YEAR, usrProf.birthday,current_date) AS "年齢",
    DATEDIFF(YEAR, usrProf.birthday,i.shipped_at) AS "出荷時年齢",
    shipAddr.id as "配送先_住所ID",
    shipAddr.postal_code AS "配送先_郵便番号",
    shipAddr.prefecture AS "配送先_都道府県",
    shipAddr.city AS "配送先_市区町村",
    shipAddr.town AS "配送先_番地",
    shipAddr.building AS "配送先_建物名",
    shipAddr.created_at as "配送先_登録日時",
    shipAddr.updated_at AS "配送先_更新日時",
    chargeDoc.id AS "担当医ID",
    chargeDoc.email AS "担当医_メールアドレス",
    chargeDocProf.family_name||' '||chargeDocProf.given_name AS "担当医_氏名",
    chargeDocCli.id as "担当医_クリニックID",
    chargeDocCli.name AS "担当医_クリニック名",
    chargeDocCli.corporate_name AS "担当医_クリニック_医療法人名",
    currentIcd.max_assigns_on AS "担当医_担当開始日"
    
FROM
    kaguya_production.invoices AS i
    
    /* line_items */
    LEFT JOIN kaguya_production.line_items AS li ON li.invoice_id = i.id
    LEFT JOIN kaguya_production.medicine_variants AS mv ON mv.id = li.medicine_variant_id
    LEFT JOIN kaguya_production.medicines AS med ON med.id = mv.medicine_id
    LEFT JOIN kaguya_production.medicine_categories AS mCat ON mCat.id = med.category_id
    LEFT JOIN kaguya_production.payment_plans AS pp ON mv.payment_plan_id = pp.id
    
    /* invoices coupon */
    LEFT JOIN kaguya_production.invoice_user_coupons AS iuc ON iuc.invoice_id = i.id
    LEFT JOIN kaguya_production.user_coupons AS uc ON uc.id = iuc.user_coupon_id
    LEFT JOIN kaguya_production.coupons AS coup ON coup.id = uc.coupon_id
    LEFT JOIN kaguya_production.coupon_activation_codes AS cac ON uc.activation_code_id = cac.id
    
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
    
    /* prescribed doctor */
    JOIN kaguya_production.users AS presDoc ON presDoc.id = ex.doctor_id
    JOIN kaguya_production.user_profiles AS presDoc_prof ON presDoc_prof.user_id = presDoc.id
    JOIN kaguya_production.profiles AS presDocProf ON presDocProf.id = presDoc_prof.profile_id
    
    /* prescribed doctor's clinic */
    LEFT JOIN kaguya_production.clinic_doctors AS cli_presDoc ON cli_presDoc.doctor_id = presDoc.id
    LEFT JOIN kaguya_production.clinics AS presDocCli ON presDocCli.id = cli_presDoc.clinic_id
    
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
    
    /* subscritpion */
    LEFT JOIN kaguya_production.user_subscriptions AS us ON us.prescription_id = pres.id
    /* customer's phone */
    LEFT JOIN kaguya_production.user_phones AS uph ON uph.user_id = usr.id
    LEFT JOIN kaguya_production.phones AS ph ON uph.phone_id = ph.id
    
    WHERE i.migration_flg = 0
    AND i.requests_on <= CURRENT_DATE ORDER BY i.requests_on ASC