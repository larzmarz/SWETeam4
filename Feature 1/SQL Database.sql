CREATE DATABASE geektext;
USE geektext;

CREATE TABLE publishers (
    PublisherID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    DiscountPercent INT
);
