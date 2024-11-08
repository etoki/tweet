select
    date
    , sum(narcissism) as narcissism
    , sum(psychopathy) as psychopathy
    , sum(machiavellianism) as machiavellianism

from
(
    select
        cal.*
        , case when HonestyHumility <= 2.5 and Agreeableness <= 3.0 and Extraversion >= 4.0 and Openness >= 3.0 then 1 else null end as "narcissism"
        , case when HonestyHumility <= 2.5 and Agreeableness <= 2.5 and Emotionality <= 2.5 and Extraversion <= 3.0 and Conscientiousness <= 3.0 then 1 else null end as "psychopathy"
        , case when HonestyHumility <= 2.5 and Agreeableness <= 2.5 and Emotionality <= 3.0 and Extraversion <= 3.0 and Openness >= 3.0 then 1 else null end as "machiavellianism"
        , FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') AS startTimestamp
        , FROM_UNIXTIME(r.endTimestamp, '%Y/%m/%d %H:%i:%s') AS endTimestamp
        , (r.endTimestamp - r.startTimestamp)/60 as diff
        , DATE(FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s')) as date
        , ROW_NUMBER() OVER (ORDER BY r.startTimestamp) as num
    from
    (

        select
            responseId
            ,firstName
            ,lastName
            ,email
            ,round(avg(case when domain = "Honesty-Humility" then inv end),2) as "HonestyHumility"
            ,round(avg(case when domain = "Emotionality"     then inv end),2) as "Emotionality"
            ,round(avg(case when domain = "Extraversion"     then inv end),2) as "Extraversion"
            ,round(avg(case when domain = "Agreeableness"    then inv end),2) as "Agreeableness"
            ,round(avg(case when domain = "Conscientiousness" then inv end),2) as "Conscientiousness"
            ,round(avg(case when domain = "Openness"          then inv end),2) as "Openness"
        from
        (
            SELECT 
                q.domain
                , q.facet
                , a.responseId
                , a.userId
                , u.firstName
                , u.lastName
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
            ,firstName
            ,lastName
            ,email
    ) cal
    inner join response r
    on cal.responseId = r.id and r.completed = 1
    order by r.startTimestamp DESC
) dark
-- where 
--     narcissism is not null 
--     or psychopathy is not null
--     or machiavellianism is not null

group by date
order by date DESC

-- limit 30

;