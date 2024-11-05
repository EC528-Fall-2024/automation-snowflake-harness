-- create the example customer table
CREATE OR REPLACE TABLE customers AS
SELECT 
  'user' || seq4() || '_' || uniform(1, 3, random(1)) || '@email.com' AS email,
  dateadd(minute, uniform(1, 525600, random(2)), ('2023-03-11'::timestamp)) AS join_date,
  round(18 + uniform(0, 10, random(3)) + uniform(0, 50, random(4)), -1) + 5 * uniform(0, 1, random(5)) AS age_band,
  CASE 
    WHEN uniform(1, 6, random(6)) = 1 THEN 'Less than $20,000'
    WHEN uniform(1, 6, random(6)) = 2 THEN '$20,000 to $34,999'
    WHEN uniform(1, 6, random(6)) = 3 THEN '$35,000 to $49,999'
    WHEN uniform(1, 6, random(6)) = 4 THEN '$50,000 to $74,999'
    WHEN uniform(1, 6, random(6)) = 5 THEN '$75,000 to $99,999'
    ELSE 'Over $100,000' 
  END AS household_income,
  CASE 
    WHEN uniform(1, 10, random(7)) < 4 THEN 'Single'
    WHEN uniform(1, 10, random(7)) < 8 THEN 'Married'
    WHEN uniform(1, 10, random(7)) < 10 THEN 'Divorced'
    ELSE 'Widowed' 
  END AS marital_status,
  greatest(round(normal(2.6, 1.4, random(8))), 1) AS household_size,
  0::float AS total_order_value
FROM table(generator(rowcount => 100000));
