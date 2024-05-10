select  
    a.id as answer_id
    , text
    , a.userId
    , q.title
    , r.completed
from hexaco_answer a 
left join hexaco_question q 
on a.questionId = q.id 
left join response r
on a.responseId = r.id

where responseId = "c6ca384c-05e2-4f03-a644-c7ad5cf6cae7";
