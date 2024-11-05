-- create warehouse, database, and schema
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE WAREHOUSE lead_scoring_demo_WH 
  WITH WAREHOUSE_SIZE = 'SMALL' 
  STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = 15;

CREATE DATABASE lead_scoring_demo;
CREATE SCHEMA lead_scoring_demo.DEMO;
