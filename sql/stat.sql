select 
    count(*) as ans
    , count(distinct r.userId) as u_ans
    , avg((r.endTimestamp - r.startTimestamp)/60) as avg_diff
    , sum(r.completed) as comp
    , sum(r.completed)/count(*) as comp_rate
    , count(DISTINCT u.email) as uu
    , count(DISTINCT u.email)/count(distinct r.userId) as auth_rate
from response r
left JOIN
user u
ON r.userId = u.id
;