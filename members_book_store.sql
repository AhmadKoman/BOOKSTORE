/*
-- Query: SHOW CREATE TABLE members
-- Date: 2024-11-28 23:24
*/
INSERT INTO `` (`Table`,`Create Table`) VALUES ('members','CREATE TABLE `members` (\n  `fname` varchar(50) NOT NULL,\n  `lname` varchar(50) NOT NULL,\n  `address` varchar(50) NOT NULL,\n  `city` varchar(30) NOT NULL,\n  `zip` int NOT NULL,\n  `phone` varchar(15) DEFAULT NULL,\n  `email` varchar(40) NOT NULL,\n  `password` varchar(200) NOT NULL,\n  `userid` int NOT NULL AUTO_INCREMENT,\n  PRIMARY KEY (`userid`),\n  UNIQUE KEY `userid_UNIQUE` (`userid`),\n  UNIQUE KEY `email_UNIQUE` (`email`),\n  UNIQUE KEY `email` (`email`)\n) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci');
