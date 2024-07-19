-- config { 
--     tags: ["prepare_loogia_params"],
--     type: "operations"
-- }
-- CREATE OR REPLACE VIEW ${constants.PREFIX}_prepare_loogia_params_assertion.${constants.PREFIX}_new_api_carrier_assertion1 AS (
  WITH cap AS (
    SELECT
      DISTINCT
      skill
    FROM
      ${ref("new_api_carrier")} nac
    LEFT JOIN
      ${ref("loogia_master_vehicle")} lmv
    ON
      nac.vehicleId = lmv.id,
    UNNEST(skills) AS skill
  )
  , needs AS (
    SELECT
      DISTINCT
      skill
    FROM
      ${ref("new_api_job")},
      UNNEST(skills) AS skill
  )
  , raw as (
  SELECT
    * -- TODO: 異常値の確認をするのに必要なカラムを設定しておく
  FROM
    needs
  WHERE
    skill NOT IN (SELECT skill FROM cap)
  )
-- )

-- count(1) = 0
-- SELECT
--   IF(
--     (SELECT COUNT(1) FROM ${constants.PREFIX}_prepare_loogia_params_assertion.${constants.PREFIX}_new_api_carrier_assertion1) = 0,
--     'OK',
--     FORMAT(
--       'USER_START:ジョブ割り当たっているスキルに対して対応するドライバーが存在しません。該当するスキル: %t :USER_END',
--       (SELECT STRING_AGG(skill, ', ') from raw)
--     )
--   ) AS result

-- case when is not null
SELECT
  CASE
    WHEN (SELECT STRING_AGG(skill, ', ') FROM raw) IS NOT NULL
    THEN FORMAT(
      'USER_START:ジョブ割り当たっているスキルに対して対応するドライバーが存在しません。該当するスキル: %s :USER_END',
      (SELECT STRING_AGG(skill, ', ') from raw)
    )
    ELSE 'OK'
  END AS result


