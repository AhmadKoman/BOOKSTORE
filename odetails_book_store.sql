/*
-- Query: SHOW CREATE TABLE odetails
-- Date: 2024-11-28 23:25
*/
INSERT INTO `` (`Table`,`Create Table`) VALUES ('odetails','CREATE TABLE `odetails` (\n  `ono` int NOT NULL,\n  `isbn` char(10) NOT NULL,\n  `qty` int NOT NULL,\n  `amount` float NOT NULL,\n  PRIMARY KEY (`isbn`,`ono`),\n  KEY `isbn_idx` (`isbn`),\n  KEY `ono_idx` (`ono`),\n  CONSTRAINT `isbn` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`),\n  CONSTRAINT `ono` FOREIGN KEY (`ono`) REFERENCES `orders` (`ono`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci');
