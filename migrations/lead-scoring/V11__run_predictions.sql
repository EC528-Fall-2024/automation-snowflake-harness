-- run prediction and save results
CREATE OR REPLACE TABLE customer_predictions AS
SELECT 
  email, 
  customer_classification_model!PREDICT(INPUT_DATA => object_construct(*)) AS predictions
FROM customers;
