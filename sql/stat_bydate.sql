select 
    date
    , count(*) as ans
    , count(distinct userId) as u_ans
    , avg((endTimestamp - startTimestamp)/60) as avg_diff
    , sum(completed) as comp
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
        ,DATE(FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s')) as date
    from response r
    left JOIN user u
    ON r.userId = u.id
) raw
group by date
order by date DESC
;