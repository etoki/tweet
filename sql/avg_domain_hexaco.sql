select
    domain
    ,round(avg(inv),2) as avg
from
(
    SELECT 
        q.domain
        , a.responseId
        , r.completed
        , case when q.inversion = 1 then 6 - a.text else a.text end as inv
    FROM hexaco_answer a
    LEFT JOIN hexaco_question q
    ON a.questionId = q.id
    left join response r
    on a.responseId = r.id
) raw
group by
    domain;
