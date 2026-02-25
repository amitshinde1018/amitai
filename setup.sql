-- DataStructure067 Database Setup
-- MySQL मध्ये हे run करा

CREATE DATABASE IF NOT EXISTS ds067_db;
USE ds067_db;

CREATE TABLE IF NOT EXISTS users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
