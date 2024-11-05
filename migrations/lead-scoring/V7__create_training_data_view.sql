-- create a view to train the model
CREATE OR REPLACE VIEW customer_training AS
SELECT 
  age_band, 
  household_income, 
  marital_status, 
  household_size, 
  CASE 
    WHEN total_order_value < 10 THEN 'BRONZE'
    WHEN total_order_value <= 25 AND total_order_value > 10 THEN 'SILVER'
    ELSE 'GOLD' 
  END AS segment
FROM customers
WHERE join_date < '2024-02-11'::date;
