select * from hexaco_question q where surveyType = "hexaco-jp"
-- where surveyType = "hexaco-jp24"

INTO OUTFILE '/var/lib/mysql-files/current_hexaco-jp_ques.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
