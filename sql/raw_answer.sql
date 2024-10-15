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
    -- and r.surveyType = 'hexaco-jp'
    and r.surveyType = 'hexaco-jp24'
    and FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') >= "2024/10/08 00:00:00"
    and r.completed = 1 

-- INTO OUTFILE '/var/lib/mysql-files/raw_answer_hexaco-jp_ver5.csv' 
INTO OUTFILE '/var/lib/mysql-files/raw_answer_hexaco-jp24_ver1.csv' 
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
