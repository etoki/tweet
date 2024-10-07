SELECT 
    -- a.responseId
    a.userId
    ,q.title
    ,a.text
    ,facet
    ,inversion
    ,case when inversion = 1 then 6 - a.text else a.text end as res
    , FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') AS startTimestamp

FROM hexaco_answer a
LEFT JOIN hexaco_question q
ON a.questionId = q.id

inner join response r
on 
    a.responseId = r.id 
    and r.surveyType = 'hexaco-jp'
    and FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') >= "2024/10/05 00:00:00"
    and r.completed = 1 

-- INTO OUTFILE '/var/lib/mysql-files/raw_answer_20240908.csv' -- to 若林先生
-- INTO OUTFILE '/var/lib/mysql-files/raw_answer_hexaco-jp_ver1.csv' -- HEXACO-JP ver1の信頼性チェック 
-- INTO OUTFILE '/var/lib/mysql-files/raw_answer_hexaco-jp_ver2.csv' -- HEXACO-JP ver2の信頼性チェック 
-- INTO OUTFILE '/var/lib/mysql-files/raw_answer_hexaco-jp_ver3.csv' -- HEXACO-JP ver3の信頼性チェック 
INTO OUTFILE '/var/lib/mysql-files/raw_answer_hexaco-jp_ver4.csv' -- HEXACO-JP ver4の信頼性チェック 
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
