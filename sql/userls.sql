select
    userId
    , user.email
    , FROM_UNIXTIME(startTimestamp, '%Y/%m/%d %H:%i:%s') AS startTimestamp
    , FROM_UNIXTIME(endTimestamp, '%Y/%m/%d %H:%i:%s') AS endTimestamp
    , (endTimestamp - startTimestamp)/60 as diff
    , completed
from response 
inner join user
on response.userId = user.id and user.email is not null
order by startTimestamp

INTO OUTFILE '/var/lib/mysql-files/userls_20240922.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
