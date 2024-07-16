CREATE DATABASE trivial_compute;
USE trivial_compute;

CREATE TABLE Categories (
    categoryID INT AUTO_INCREMENT PRIMARY KEY,
    categoryName VARCHAR(255) NOT NULL
);

CREATE TABLE Questions (
    questionID INT AUTO_INCREMENT PRIMARY KEY,
    questionContent TEXT NOT NULL,
    answerContent TEXT NOT NULL,
    categoryID INT,
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID)
);

INSERT INTO Categories (categoryName) VALUES ('Science');
INSERT INTO Categories (categoryName) VALUES ('History');
INSERT INTO Categories (categoryName) VALUES ('Geography');

INSERT INTO Questions (questionContent, answerContent, categoryID) VALUES
('What is the chemical symbol for water?', 'H2O', 1),
('Who was the first president of the United States?', 'George Washington', 2),
('What is the capital of France?', 'Paris', 3);

SELECT * FROM Questions;

SELECT Questions.questionID, Questions.questionContent, Questions.answerContent, Categories.categoryName
FROM Questions
JOIN Categories ON questions.categoryID = Categories.categoryID;