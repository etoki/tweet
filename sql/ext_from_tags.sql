select "No","email","Honesty-Humility","Emotionality","Extraversion","Agreeableness","Conscientiousness","Openness","start_time","end_time","answer_time","surveyType"
union all
select
    ROW_NUMBER() OVER (ORDER BY r.startTimestamp) as num
    , cal.email
    , cal.h
    , cal.e
    , cal.x
    , cal.a
    , cal.c
    , cal.o
    , FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') AS start_time
    , FROM_UNIXTIME(r.endTimestamp, '%Y/%m/%d %H:%i:%s') AS end_time
    , (r.endTimestamp - r.startTimestamp)/60 as answer_time
    , r.surveyType
from
(
    select
        responseId
        ,email
        ,round(avg(case when domain = "Honesty-Humility" then inv end),2) as h
        ,round(avg(case when domain = "Emotionality"     then inv end),2) as e
        ,round(avg(case when domain = "Extraversion"     then inv end),2) as x
        ,round(avg(case when domain = "Agreeableness"    then inv end),2) as a
        ,round(avg(case when domain = "Conscientiousness" then inv end),2) as c
        ,round(avg(case when domain = "Openness"          then inv end),2) as o
    from
    (
        SELECT 
            q.domain
            , q.inversion
            , a.responseId
            , a.userId
            , u.email
            , case when q.inversion = 1 then 6 - a.text else a.text end as inv
        FROM hexaco_answer a
        LEFT JOIN hexaco_question q
        ON a.questionId = q.id
        left join user u
        on a.userId = u.id
    ) raw
    group by
        responseId
        ,email
) cal
left join response r
on cal.responseId = r.id
inner join response_tags rt
on r.id = rt.responseId and rt.tags LIKE '%"musubite"%'

INTO OUTFILE '/var/lib/mysql-files/musubite_20241025.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
