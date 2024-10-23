-- File location: migrations/V2__create_database.sql

USE DATABASE TEST;  -- Switch to TEST database
USE SCHEMA PUBLIC;  -- Switch to PUBLIC schema

-- Create a new random table
CREATE TABLE random_table (
    id INT AUTOINCREMENT,
    name STRING,
    value FLOAT
);

-- Insert a row into the random_table
INSERT INTO random_table (name, value)
VALUES ('Test Name', 123.45);

