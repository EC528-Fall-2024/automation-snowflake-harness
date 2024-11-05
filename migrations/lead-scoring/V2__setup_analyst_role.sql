-- set up analyst role
CREATE ROLE analyst;

GRANT USAGE ON DATABASE lead_scoring_demo TO ROLE analyst;
GRANT USAGE ON SCHEMA lead_scoring_demo.DEMO TO ROLE analyst;
GRANT USAGE ON WAREHOUSE lead_scoring_demo_WH TO ROLE analyst;
GRANT CREATE TABLE ON SCHEMA lead_scoring_demo.DEMO TO ROLE analyst;
GRANT CREATE VIEW ON SCHEMA lead_scoring_demo.DEMO TO ROLE analyst;
GRANT CREATE SNOWFLAKE.ML.CLASSIFICATION ON SCHEMA lead_scoring_demo.DEMO TO ROLE analyst;

GRANT ROLE analyst TO USER krish;
