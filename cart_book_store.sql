/*
-- Query: SHOW CREATE TABLE cart
-- Date: 2024-11-28 23:24
*/
INSERT INTO `` (`Table`,`Create Table`) VALUES ('cart','CREATE TABLE `cart` (\n  `useri` int NOT NULL,\n  `isb` char(10) NOT NULL,\n  `qty` int NOT NULL,\n  PRIMARY KEY (`useri`,`isb`),\n  KEY `isbn_idx` (`isb`),\n  CONSTRAINT `isb` FOREIGN KEY (`isb`) REFERENCES `books` (`isbn`),\n  CONSTRAINT `useri` FOREIGN KEY (`useri`) REFERENCES `members` (`userid`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci');
