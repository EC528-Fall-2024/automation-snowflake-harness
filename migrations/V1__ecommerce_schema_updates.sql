
-- Add index to optimize querying users by email
CREATE INDEX IF NOT EXISTS idx_users_email 
ON ecommerce_schema.users (email);

-- Create payments table
CREATE OR REPLACE TABLE ecommerce_schema.payments (
    id INT AUTOINCREMENT PRIMARY KEY,
    user_id INT,
    order_id INT,
    amount DECIMAL(10, 2),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES ecommerce_schema.users(id),
    FOREIGN KEY (order_id) REFERENCES ecommerce_schema.orders(id)
);

-- Add phone number column to users table
ALTER TABLE ecommerce_schema.users
ADD COLUMN phone_number STRING;

-- Create a role for read-only access
CREATE ROLE IF NOT EXISTS read_only_role;

-- Grant read-only role to SELECT from all tables in ecommerce_schema
GRANT SELECT ON ALL TABLES IN SCHEMA ecommerce_schema TO ROLE read_only_role;
