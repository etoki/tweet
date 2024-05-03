select count(*) from (
select
    cal.*
    ,DENSE_RANK() OVER (ORDER BY h DESC) as r_h
    ,DENSE_RANK() OVER (ORDER BY e DESC) as r_e
    ,DENSE_RANK() OVER (ORDER BY x DESC) as r_x
    ,DENSE_RANK() OVER (ORDER BY a DESC) as r_a
    ,DENSE_RANK() OVER (ORDER BY c DESC) as r_c
    ,DENSE_RANK() OVER (ORDER BY o DESC) as r_o
    -- , FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') AS startTimestamp
    -- , FROM_UNIXTIME(r.endTimestamp, '%Y/%m/%d %H:%i:%s') AS endTimestamp
    -- , (r.endTimestamp - r.startTimestamp)/60 as diff
    -- , r.completed
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
order by r.startTimestamp
)a