CREATE DATABASE IF NOT EXISTS sentiment_analysis;

USE sentiment_analysis;

CREATE TABLE IF NOT EXISTS tweet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive BOOLEAN NOT NULL,
    negative BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX (text),
    INDEX (positive),
    INDEX (negative)
);

CREATE TABLE data_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tweet_id INT,
    prediction_positive FLOAT,
    prediction_negative FLOAT,
    actual_sentiment VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tweet_id) REFERENCES tweet(id)
);

CREATE TABLE model_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_type VARCHAR(20) NOT NULL,
    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accuracy FLOAT,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT,
    confusion_matrix JSON,
    model_version VARCHAR(50)
);