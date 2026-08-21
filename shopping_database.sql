-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: ecommerce
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `Customer_ID` int NOT NULL,
  `User_Name` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Cust_Name` varchar(100) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `Phone_No` bigint DEFAULT NULL,
  `Email_ID` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Customer_ID`),
  UNIQUE KEY `User_Name` (`User_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'KANNU','YJ123','YATHARTH JINDAL','U-23',9889977665,'yj@gmail.com'),(2,'Nipun05','12345678','Nipun Goel','A-23',9899922334,'nipungoel@gmail.com'),(3,'SS22','1133355555','Sahibjeet Singh','A-09,MAJLIS PARK',9887755441,'sahibsingh23@gmail.com'),(4,'TA','TA123','Tanishq aggrawal','A-23',9877442233,'tanishqaggrawal@gmail.com'),(5,'Sarthak07','1234','Sarthak Jindal','A-09 Majlis park',8766544332,'sarthak07@gmail.com');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbacks`
--

DROP TABLE IF EXISTS `feedbacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedbacks` (
  `Customer_ID` int DEFAULT NULL,
  `Feedback` varchar(255) DEFAULT NULL,
  `Seller_ID` int DEFAULT NULL,
  `Product_ID` int DEFAULT NULL,
  `Seller_Name` varchar(100) DEFAULT NULL,
  KEY `Customer_ID` (`Customer_ID`),
  CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`Customer_ID`) REFERENCES `customers` (`Customer_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbacks`
--

LOCK TABLES `feedbacks` WRITE;
/*!40000 ALTER TABLE `feedbacks` DISABLE KEYS */;
INSERT INTO `feedbacks` VALUES (1,'Good book',1,101,'Alakh Pandey'),(2,'Bad service',101,102,'Alakh Pandey'),(3,'GOOD',1,102,'Alakh Pandey'),(3,'GOOD',2,111,'Udit Singh'),(5,'GOOD',101,102,'PW');
/*!40000 ALTER TABLE `feedbacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `Transaction_ID` int NOT NULL,
  `Customer_ID` int DEFAULT NULL,
  `Product_ID` int DEFAULT NULL,
  `Date_of_Dispatch` date DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Transaction_ID`),
  KEY `Customer_ID` (`Customer_ID`),
  KEY `Product_ID` (`Product_ID`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`Customer_ID`) REFERENCES `customers` (`Customer_ID`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`Product_ID`) REFERENCES `products` (`Product_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,101,'2026-01-04',25,349.00,8725.00),(2,2,102,'2026-01-05',5,349.00,1745.00),(3,2,101,'2026-01-05',10,349.00,3490.00),(4,2,111,'2026-01-05',25,250.00,6250.00),(5,3,111,'2026-01-05',2,250.00,500.00),(6,3,102,'2026-01-05',25,349.00,8725.00),(7,3,101,'2026-01-05',2,349.00,698.00),(8,5,102,'2026-06-27',5,349.00,1745.00);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `Product_ID` int NOT NULL,
  `Category` varchar(50) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Brand_Name` varchar(100) DEFAULT NULL,
  `Seller_ID` int DEFAULT NULL,
  PRIMARY KEY (`Product_ID`),
  KEY `Seller_ID` (`Seller_ID`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`Seller_ID`) REFERENCES `seller` (`Seller_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (101,'JEE BOOKS','HC VERMA PHYSICS VOL 1',13,349.00,'PW',1),(102,'JEE BOOKS','HC VERMA PHYSICS VOL 2',15,349.00,'PW',1),(103,'JEE BOOKS','CHEMISTRY FOR JEE MAINS PYQ 2019-2024',35,149.00,'PW',1),(111,'BOOKS','NEET CHEMISTRY PYQS 2019-2025',23,250.00,'ALLEN',2);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seller`
--

DROP TABLE IF EXISTS `seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seller` (
  `Seller_ID` int NOT NULL,
  `Seller_Name` varchar(100) DEFAULT NULL,
  `Brand_Name` varchar(100) DEFAULT NULL,
  `User_Name` varchar(50) DEFAULT NULL,
  `Password` varchar(50) DEFAULT NULL,
  `Phone_No` bigint DEFAULT NULL,
  `Email_ID` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Seller_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seller`
--

LOCK TABLES `seller` WRITE;
/*!40000 ALTER TABLE `seller` DISABLE KEYS */;
INSERT INTO `seller` VALUES (1,'Alakh Pandey','PW','PW123','122333',8900889976,'pw123@gmail.com'),(2,'Usit Singh','ALLEN','ALLEN22','123',8989898966,'usitallen12@gmail.com');
/*!40000 ALTER TABLE `seller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sfeedback`
--

DROP TABLE IF EXISTS `sfeedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sfeedback` (
  `Seller_ID` int DEFAULT NULL,
  `Feedback` varchar(255) DEFAULT NULL,
  `Rating` int DEFAULT NULL,
  KEY `Seller_ID` (`Seller_ID`),
  CONSTRAINT `sfeedback_ibfk_1` FOREIGN KEY (`Seller_ID`) REFERENCES `seller` (`Seller_ID`),
  CONSTRAINT `sfeedback_chk_1` CHECK ((`Rating` between 1 and 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sfeedback`
--

LOCK TABLES `sfeedback` WRITE;
/*!40000 ALTER TABLE `sfeedback` DISABLE KEYS */;
INSERT INTO `sfeedback` VALUES (1,'Good',4),(1,'GOOD',3),(2,'Average',3);
/*!40000 ALTER TABLE `sfeedback` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-28 10:20:05
