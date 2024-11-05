-- create the classification model
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION customer_classification_model(
    INPUT_DATA => SYSTEM$REFERENCE('view', 'customer_training'),
    TARGET_COLNAME => 'segment'
);
