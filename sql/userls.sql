select
    userId
    , user.email
    , FROM_UNIXTIME(startTimestamp, '%Y/%m/%d %H:%i:%s') AS startTimestamp
    , FROM_UNIXTIME(endTimestamp, '%Y/%m/%d %H:%i:%s') AS endTimestamp
    , (endTimestamp - startTimestamp)/60 as diff
    , completed
from response 
left join user
on response.userId = user.id 
order by startTimestamp;