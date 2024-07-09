CREATE DATABASE IF NOT EXISTS testDB;
USE testDB;
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    enabled BOOLEAN,
    price DECIMAL(10, 2)
);
INSERT INTO tasks (name, description, status, enabled, price)
VALUES ('Task 1', 'Description 1', 'Pending', true, 10.5),
    ('Task 2', 'Description 2', 'Completed', false, 20.5),
    ('Task 3', 'Description 3', 'Pending', true, 30.5);