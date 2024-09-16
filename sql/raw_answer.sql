SELECT 
    a.responseId
    ,q.title
    ,a.text
FROM hexaco_answer a
LEFT JOIN hexaco_question q
ON a.questionId = q.id

INTO OUTFILE '/var/lib/mysql-files/raw_answer_20240908.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
