/*
-- Query: SHOW CREATE TABLE books
-- Date: 2024-11-28 23:24
*/
INSERT INTO `` (`Table`,`Create Table`) VALUES ('books','CREATE TABLE `books` (\n  `isbn` char(10) NOT NULL,\n  `author` varchar(100) NOT NULL,\n  `title` varchar(200) NOT NULL,\n  `price` float NOT NULL,\n  `subject` varchar(100) NOT NULL,\n  PRIMARY KEY (`isbn`),\n  UNIQUE KEY `isbn_UNIQUE` (`isbn`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci');
