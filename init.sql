CREATE DATABASE IF NOT EXISTS sentiment_analysis ;

USE sentiment_analysis;

CREATE TABLE IF NOT EXISTS tweet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive BOOLEAN NOT NULL,
    negative BOOLEAN NOT NULL
);
