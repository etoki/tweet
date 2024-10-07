with 
    raw as (
        select
            r.userId
            , u.email
            , FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') AS st
            , FROM_UNIXTIME(r.endTimestamp, '%Y/%m/%d %H:%i:%s') AS et
            , (r.endTimestamp - r.startTimestamp)/60 as diff
            , r.completed
        from response r
        inner join user u
        on 
            r.userId = u.id 
            and u.email is not null
            and r.completed = 1
            and FROM_UNIXTIME(r.startTimestamp, '%Y/%m/%d %H:%i:%s') <= "2024/09/16 00:00:00"

        order by r.startTimestamp
    )

select distinct email from raw

INTO OUTFILE '/var/lib/mysql-files/userls_hexaco_comp.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
