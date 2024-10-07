select 
    date
    -- ,sum(case when surveyType = 'hexaco'      then 1 end) as 'hexaco'
    ,sum(case when surveyType = 'hexaco-jp'   then 1 end) as 'hexaco-jp60'
    ,sum(case when surveyType = 'hexaco-jp24' then 1 end) as 'hexaco-jp24'

    , count(*) as ans
    , count(distinct userId) as u_ans
    , avg((endTimestamp - startTimestamp)/60) as avg_diff

    ,sum(case when completed = 1 then 1 end) as 'comp_all'
    ,sum(case when completed = 1 and surveyType = 'hexaco-jp'   then 1 end) as 'comp_60'
    ,sum(case when completed = 1 and surveyType = 'hexaco-jp24' then 1 end) as 'comp_24'
    , sum(completed)/count(*) as comp_rate

    , count(DISTINCT email) as uu
    , count(DISTINCT email)/count(distinct userId) as auth_rate
from
(
    select 
        r.id as responseId
        ,userId
        ,startTimestamp
        ,endTimestamp
        ,completed
        ,email
        ,surveyType
        ,DATE(FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s')) as date
    from response r
    left JOIN user u
    ON r.userId = u.id
) raw
where
    date >= "2024/09/17"
group by date
order by date DESC
;