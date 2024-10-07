-- Create user if not exists
CREATE USER IF NOT EXISTS 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS auth;

-- Grant privileges (this will not throw an error if the user already has privileges)
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

-- Use the auth database
USE auth;

-- Create table if not exists
CREATE TABLE IF NOT EXISTS user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password)
SELECT 'gabriel.faglioni@example.com', 'admin123'
WHERE NOT EXISTS (
  SELECT 1 FROM user WHERE email = 'gabriel.faglioni@example.com'
);