-- Create a simple test table in Snowflake
CREATE OR REPLACE TABLE test_table (
    id INT AUTOINCREMENT,
    name STRING,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into the test table
INSERT INTO test_table (name) VALUES ('Sample Data 1'), ('Sample Data 2');

-- Verify the data insertion (optional)
SELECT * FROM test_table;