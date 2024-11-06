CREATE DATABASE  IF NOT EXISTS `master_pol` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `master_pol`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: master_pol
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `access_log`
--

DROP TABLE IF EXISTS `access_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `access_log` (
  `access_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `door_id` int DEFAULT NULL,
  `access_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`access_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `access_log_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_log`
--

LOCK TABLES `access_log` WRITE;
/*!40000 ALTER TABLE `access_log` DISABLE KEYS */;
INSERT INTO `access_log` VALUES (1,1,1,'2024-10-29 20:05:45'),(2,2,2,'2024-10-29 20:05:45');
/*!40000 ALTER TABLE `access_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `fio` varchar(255) DEFAULT NULL,
  `date_of_birthday` date DEFAULT NULL,
  `s_n_passport` text,
  `bank_details` text,
  `family_status` varchar(50) DEFAULT NULL,
  `health_status` text,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'Иванов Иван Иванович','1990-01-15','1234 567890','Сбербанк','Женат','Здоров'),(2,'Петрова Анна Сергеевна','1985-07-22','9876 543210','Тинькофф','Не замужем','Здоров'),(3,'Сидоров Сергей Петрович','1978-03-30','5678 123456','ВТБ','Разведен','Здоров');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `human_resources`
--

DROP TABLE IF EXISTS `human_resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `human_resources` (
  `hr_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `work_permit` text,
  PRIMARY KEY (`hr_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `human_resources_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `human_resources`
--

LOCK TABLES `human_resources` WRITE;
/*!40000 ALTER TABLE `human_resources` DISABLE KEYS */;
INSERT INTO `human_resources` VALUES (1,1,'Разрешение A'),(2,2,'Разрешение B');
/*!40000 ALTER TABLE `human_resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managers`
--

DROP TABLE IF EXISTS `managers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `managers` (
  `manager_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` text,
  `phone` text,
  `email` text,
  PRIMARY KEY (`manager_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managers`
--

LOCK TABLES `managers` WRITE;
/*!40000 ALTER TABLE `managers` DISABLE KEYS */;
INSERT INTO `managers` VALUES (1,'Алексеев Алексей','Поиск партнера A, B','Изменение рейтинга A, B','Обработка заявки A, B'),(2,'Григорьев Григорий','Поиск партнера C','Изменение рейтинга C','Обработка заявки D');
/*!40000 ALTER TABLE `managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials` (
  `material_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(100) DEFAULT NULL,
  `marriage` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`material_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials`
--

LOCK TABLES `materials` WRITE;
/*!40000 ALTER TABLE `materials` DISABLE KEYS */;
INSERT INTO `materials` VALUES (3,'Тип материала 1','0,10%'),(4,'Тип материала 2','0,95%'),(5,'Тип материала 3','0,28%'),(6,'Тип материала 4','0,55%'),(7,'Тип материала 5','0,34%');
/*!40000 ALTER TABLE `materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partners`
--

DROP TABLE IF EXISTS `partners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partners` (
  `partner_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` text,
  `inn` varchar(12) DEFAULT NULL,
  `fio` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`partner_id`),
  CONSTRAINT `partners_chk_1` CHECK ((`rating` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partners`
--

LOCK TABLES `partners` WRITE;
/*!40000 ALTER TABLE `partners` DISABLE KEYS */;
INSERT INTO `partners` VALUES (8,'ЗАО','База Строитель','652050, Кемеровская область, город Юрга, ул. Лесная, 15','2222455179','Иванова Александра Ивановна','493 123 45 67','aleksandraivanova@ml.ru',7),(9,'ООО','Паркет 29','164500, Архангельская область, город Северодвинск, ул. Строителей, 18','3333888520','Петров Василий Петрович','987 123 56 78','vppetrov@vl.ru',7),(10,'ПАО','Стройсервис','188910, Ленинградская область, город Приморск, ул. Парковая, 21','4440391035','Соловьев Андрей Николаевич','812 223 32 00','ansolovev@st.ru',7),(11,'ОАО','Ремонт и отделка','143960, Московская область, город Реутов, ул. Свободы, 51','1111520857','Воробьева Екатерина Валерьевна','444 222 33 11','ekaterina.vorobeva@ml.ru',5),(12,'ЗАО','МонтажПро','309500, Белгородская область, город Старый Оскол, ул. Рабочая, 122','5552431140','Степанов Степан Сергеевич','912 888 33 33','stepanov@stepan.ru',9);
/*!40000 ALTER TABLE `partners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_type`
--

DROP TABLE IF EXISTS `product_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_type` (
  `type_id` int NOT NULL AUTO_INCREMENT,
  `type_product` varchar(45) DEFAULT NULL,
  `ratio` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_type`
--

LOCK TABLES `product_type` WRITE;
/*!40000 ALTER TABLE `product_type` DISABLE KEYS */;
INSERT INTO `product_type` VALUES (1,'Ламинат','2,35'),(2,'Массивная доска','5,15'),(3,'Паркетная доска','4,34'),(4,'Пробковое покрытие','1,5');
/*!40000 ALTER TABLE `product_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product` varchar(255) DEFAULT NULL,
  `partnier_name` varchar(255) DEFAULT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  `date_sale` date DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (4,'Паркетная доска Ясень темный однополосная 14 мм','База Строитель','15500','2023-03-23'),(5,'Ламинат Дуб дымчато-белый 33 класс 12 мм','База Строитель','12350','2023-12-18'),(6,'Ламинат Дуб серый 32 класс 8 мм с фаской','База Строитель','37400','2024-06-07'),(7,'Инженерная доска Дуб Французская елка однополосная 12 мм','Паркет 29','35000','2022-12-02'),(8,'Пробковое напольное клеевое покрытие 32 класс 4 мм','Паркет 29','1250','2023-05-17'),(9,'Ламинат Дуб дымчато-белый 33 класс 12 мм','Паркет 29','1000','2024-06-07'),(10,'Паркетная доска Ясень темный однополосная 14 мм','Паркет 29','7550','2024-07-01'),(11,'Паркетная доска Ясень темный однополосная 14 мм','Стройсервис','7250','2023-01-22'),(12,'Инженерная доска Дуб Французская елка однополосная 12 мм','Стройсервис','2500','2024-07-05'),(13,'Ламинат Дуб серый 32 класс 8 мм с фаской','Ремонт и отделка','59050','2023-03-20'),(14,'Ламинат Дуб дымчато-белый 33 класс 12 мм','Ремонт и отделка','37200','2024-03-12'),(15,'Пробковое напольное клеевое покрытие 32 класс 4 мм','Ремонт и отделка','4500','2024-05-14'),(16,'Ламинат Дуб дымчато-белый 33 класс 12 мм','МонтажПро','50000','2023-09-19'),(17,'Ламинат Дуб серый 32 класс 8 мм с фаской','МонтажПро','670000','2023-11-10'),(18,'Паркетная доска Ясень темный однополосная 14 мм','МонтажПро','35000','2024-04-15'),(19,'Инженерная доска Дуб Французская елка однополосная 12 мм','МонтажПро','25002','2024-06-12');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requests`
--

DROP TABLE IF EXISTS `requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `partner_id` int DEFAULT NULL,
  `manager_id` int DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `production_date` date DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `status` enum('Создана','Ожидает оплаты','В производстве','Готова к отправке','Завершена') DEFAULT NULL,
  PRIMARY KEY (`request_id`),
  KEY `partner_id` (`partner_id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`partner_id`) REFERENCES `partners` (`partner_id`),
  CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`manager_id`) REFERENCES `managers` (`manager_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requests`
--

LOCK TABLES `requests` WRITE;
/*!40000 ALTER TABLE `requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_history`
--

DROP TABLE IF EXISTS `sales_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_history` (
  `sale_id` int NOT NULL AUTO_INCREMENT,
  `partner_id` int NOT NULL,
  `product_id` int NOT NULL,
  `price` int NOT NULL,
  `sale_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sale_id`),
  KEY `partner_id` (`partner_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `sales_history_ibfk_1` FOREIGN KEY (`partner_id`) REFERENCES `partners` (`partner_id`) ON DELETE CASCADE,
  CONSTRAINT `sales_history_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_history`
--

LOCK TABLES `sales_history` WRITE;
/*!40000 ALTER TABLE `sales_history` DISABLE KEYS */;
INSERT INTO `sales_history` VALUES (3,10,7,70000,'2024-12-12 00:00:00'),(4,10,9,150000,'2024-05-05 00:00:00');
/*!40000 ALTER TABLE `sales_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `supplier_id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(50) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `inn` varchar(12) DEFAULT NULL,
  `supply_history` text,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'Оптовик','Поставщик 1','123456789012','Поставлено 100 единиц товара'),(2,'Розничный','Поставщик 2','987654321012','Поставлено 200 единиц товара'),(3,'Розничный','Поставщик 3','987654321015','Поставлено 200 единиц товара');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse`
--

DROP TABLE IF EXISTS `warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse` (
  `warehouse_id` int NOT NULL AUTO_INCREMENT,
  `material_id` int DEFAULT NULL,
  `incoming_date` date DEFAULT NULL,
  `outgoing_date` date DEFAULT NULL,
  `current_stock` int DEFAULT NULL,
  PRIMARY KEY (`warehouse_id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `warehouse_ibfk_1` FOREIGN KEY (`material_id`) REFERENCES `materials` (`material_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse`
--

LOCK TABLES `warehouse` WRITE;
/*!40000 ALTER TABLE `warehouse` DISABLE KEYS */;
/*!40000 ALTER TABLE `warehouse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'master_pol'
--

--
-- Dumping routines for database 'master_pol'
--
/*!50003 DROP FUNCTION IF EXISTS `calculate_discount` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `calculate_discount`(total_sales DECIMAL(10,2)) RETURNS decimal(5,2)
    DETERMINISTIC
BEGIN
    DECLARE discount DECIMAL(5,2);
    IF total_sales < 10000 THEN
        SET discount = 0;
    ELSEIF total_sales >= 10000 AND total_sales < 50000 THEN
        SET discount = 5;
    ELSEIF total_sales >= 50000 AND total_sales < 300000 THEN
        SET discount = 10;
    ELSE
        SET discount = 15;
    END IF;
    RETURN discount;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-06 17:23:47
