/*
-- Query: SHOW CREATE TABLE orders
-- Date: 2024-11-28 23:25
*/
INSERT INTO `` (`Table`,`Create Table`) VALUES ('orders','CREATE TABLE `orders` (\n  `userid` int NOT NULL,\n  `ono` int NOT NULL AUTO_INCREMENT,\n  `shipAddress` varchar(50) DEFAULT NULL,\n  `shipCity` varchar(30) DEFAULT NULL,\n  `shipZip` int DEFAULT NULL,\n  PRIMARY KEY (`ono`),\n  UNIQUE KEY `ono` (`ono`),\n  UNIQUE KEY `ono_UNIQUE` (`ono`),\n  KEY `userid_idx` (`userid`),\n  CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `members` (`userid`)\n) ENGINE=InnoDB AUTO_INCREMENT=135 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci');
