select
    cal.*
    , FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') AS startTimestamp
    , FROM_UNIXTIME(r.endTimestamp, '%Y/%m/%d %H:%i:%s') AS endTimestamp
    , (r.endTimestamp - r.startTimestamp)/60 as diff
    , r.completed
    , ROW_NUMBER() OVER (ORDER BY r.startTimestamp) as num
from
(

    select
        responseId
        ,firstName
        ,lastName
        ,email
        ,round(avg(case when domain = "Honesty-Humility" then inv end),2) as "Honesty-Humility"
        ,round(avg(case when domain = "Emotionality"     then inv end),2) as "Emotionality"
        ,round(avg(case when domain = "Extraversion"     then inv end),2) as "Extraversion"
        ,round(avg(case when domain = "Agreeableness"    then inv end),2) as "Agreeableness"
        ,round(avg(case when domain = "Conscientiousness" then inv end),2) as "Conscientiousness"
        ,round(avg(case when domain = "Openness"          then inv end),2) as "Openness"
        ,round(avg(case when facet = "Sincerity"    then inv end),2) as "Sincerity"
        ,round(avg(case when facet = "Fairness"    then inv end),2) as "Fairness"
        ,round(avg(case when facet = "Greed-Avoidance"    then inv end),2) as "Greed-Avoidance"
        ,round(avg(case when facet = "Modesty"    then inv end),2) as "Modesty"
        ,round(avg(case when facet = "Fearfulness"    then inv end),2) as "Fearfulness"
        ,round(avg(case when facet = "Anxiety"    then inv end),2) as "Anxiety"
        ,round(avg(case when facet = "Dependence"    then inv end),2) as "Dependence"
        ,round(avg(case when facet = "Sentimentality"    then inv end),2) as "Sentimentality"
        ,round(avg(case when facet = "Social-Self-Esteem"    then inv end),2) as "Social-Self-Esteem"
        ,round(avg(case when facet = "Social-Boldness"    then inv end),2) as "Social-Boldness"
        ,round(avg(case when facet = "Sociability"    then inv end),2) as "Sociability"
        ,round(avg(case when facet = "Liveliness"    then inv end),2) as "Liveliness"
        ,round(avg(case when facet = "Forgiveness"    then inv end),2) as "Forgiveness"
        ,round(avg(case when facet = "Gentleness"    then inv end),2) as "Gentleness"
        ,round(avg(case when facet = "Flexibility"    then inv end),2) as "Flexibility"
        ,round(avg(case when facet = "Patience"    then inv end),2) as "Patience"
        ,round(avg(case when facet = "Organization"    then inv end),2) as "Organization"
        ,round(avg(case when facet = "Diligence"    then inv end),2) as "Diligence"
        ,round(avg(case when facet = "Perfectionism"    then inv end),2) as "Perfectionism"
        ,round(avg(case when facet = "Prudence"    then inv end),2) as "Prudence"
        ,round(avg(case when facet = "Aesthetic-Appreciation"    then inv end),2) as "Aesthetic-Appreciation"
        ,round(avg(case when facet = "Inquisitiveness"    then inv end),2) as "Inquisitiveness"
        ,round(avg(case when facet = "Creativity"    then inv end),2) as "Creativity"
        ,round(avg(case when facet = "Unconventionality"    then inv end),2) as "Unconventionality"
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
left join response r
on cal.responseId = r.id
where 
    r.completed = 1 
order by r.startTimestamp DESC

-- limit 100
INTO OUTFILE '/home/rocky/dev/sql/output.csv'
-- INTO OUTFILE '/var/lib/mysql-files/output.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
