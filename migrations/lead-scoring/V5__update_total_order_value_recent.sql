-- set total order value for more recent customers
UPDATE customers
SET total_order_value = round(
  (CASE 
    WHEN uniform(1, 3, random(9)) < 3 THEN 0
    ELSE abs(normal(10, 3, random(10))) +
      CASE WHEN marital_status = 'Married' THEN normal(5, 2, random(11)) ELSE 0 END +
      CASE WHEN household_size > 2 THEN normal(5, 2, random(11)) ELSE 0 END +
      CASE WHEN household_income IN ('$50,000 to $74,999', '$75,000 to $99,999', 'Over $100,000') THEN normal(5, 2, random(11)) ELSE 0 END
  END), 2)
WHERE join_date >= '2024-02-11'::date;
