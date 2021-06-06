mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: capstone
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance_log`
--

DROP TABLE IF EXISTS `attendance_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `subject_id` varchar(20) DEFAULT NULL,
  `group_code` varchar(20) DEFAULT NULL,
  `semester` int NOT NULL,
  `teacher_id` int NOT NULL,
  `device_id` int NOT NULL,
  `attendance_time` varchar(30) DEFAULT NULL,
  `image_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_log`
--

LOCK TABLES `attendance_log` WRITE;
/*!40000 ALTER TABLE `attendance_log` DISABLE KEYS */;
INSERT INTO `attendance_log` VALUES (24,1752041,'CO3025','CC01',201,2,1,'2021-04-22 11:32:24','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752041%2Fattendance%2Fphotos%2F2021-04-22%2011:32:24.jpg?generation=1619065945786924&alt=media&token=104d213e-6ded-4beb-b2cb-15d977602233'),(25,1752139,'CO3025','CC01',201,2,1,'2021-04-22 11:50:52','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752139%2Fattendance%2Fphotos%2F2021-04-22%2011:50:52.jpg?generation=1619067052466941&alt=media&token=c3e35eb1-662f-4e2c-bce7-5e7a48f90e0b'),(26,1752015,'CO3025','CC01',201,2,1,'2021-04-22 11:51:16','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752015%2Fattendance%2Fphotos%2F2021-04-22%2011:51:16.jpg?generation=1619067077014712&alt=media&token=05d182ea-2087-4b13-8da6-cbb03224c8f5'),(27,1752522,'CO3025','CC01',201,2,1,'2021-04-22 11:51:42','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752522%2Fattendance%2Fphotos%2F2021-04-22%2011:51:42.jpg?generation=1619067102965813&alt=media&token=6ad0c5f0-33a4-46d9-9221-29633ff7b328'),(28,2053234,'CO3025','CC01',201,2,1,'2021-04-22 11:51:56','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F2053234%2Fattendance%2Fphotos%2F2021-04-22%2011:51:56.jpg?generation=1619067116942433&alt=media&token=2a26cc13-d5f2-4919-86ff-f8eb8b144d3a'),(29,1752394,'CO3025','CC01',201,2,1,'2021-04-22 11:52:19','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752394%2Fattendance%2Fphotos%2F2021-04-22%2011:52:19.jpg?generation=1619067139553950&alt=media&token=b73d5851-69ab-43dd-bc87-99c619247439'),(30,1752089,'CO3025','CC01',201,2,1,'2021-04-22 11:52:39','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752089%2Fattendance%2Fphotos%2F2021-04-22%2011:52:39.jpg?generation=1619067160218193&alt=media&token=c8824401-38c1-4297-8779-9e4242d9ef4e'),(31,1752516,'CO3025','CC01',201,2,1,'2021-04-22 11:52:59','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752516%2Fattendance%2Fphotos%2F2021-04-22%2011:52:59.jpg?generation=1619067179388205&alt=media&token=e0dd1a09-a33f-4351-ad6a-4758f369f223'),(32,1752494,'CO3025','CC01',201,2,1,'2021-04-22 11:53:13','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752494%2Fattendance%2Fphotos%2F2021-04-22%2011:53:13.jpg?generation=1619067193839783&alt=media&token=81672dc0-9d0e-4cfb-bcb4-3f4a782c29e9'),(33,1752259,'CO3025','CC01',201,2,1,'2021-04-22 11:57:22','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752259%2Fattendance%2Fphotos%2F2021-04-22%2011:57:22.jpg?generation=1619067480729084&alt=media&token=3e8250ce-71f0-40ef-8988-a956bcb960a2'),(35,1952684,'CO2004','CC02',201,2,1,'2021-04-26 15:13:09','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952684%2Fattendance%2Fphotos%2F2021-04-26%2015:13:09.jpg?generation=1619424790779861&alt=media&token=c46f0e53-4ca4-4cb3-a5a5-1a1c56e8be93'),(36,1852827,'CO2004','CC02',201,2,1,'2021-04-26 15:13:31','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1852827%2Fattendance%2Fphotos%2F2021-04-26%2015:13:31.jpg?generation=1619424812302240&alt=media&token=aa127446-cde8-41e3-81f1-f643e5b3276f'),(37,1911940,'CO2004','CC02',201,2,1,'2021-04-26 15:14:14','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1911940%2Fattendance%2Fphotos%2F2021-04-26%2015:14:14.jpg?generation=1619424855065192&alt=media&token=890da26d-f57e-4cbc-b265-1cf0842da266'),(38,1752384,'CO2004','CC02',201,2,1,'2021-04-26 15:14:59','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752384%2Fattendance%2Fphotos%2F2021-04-26%2015:14:59.jpg?generation=1619424899959624&alt=media&token=a36365a7-3651-4617-9969-c0555bf8e166'),(39,1810490,'CO2004','CC02',201,2,1,'2021-04-26 15:15:08','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1810490%2Fattendance%2Fphotos%2F2021-04-26%2015:15:08.jpg?generation=1619424908559579&alt=media&token=d28f8876-7a22-4317-b9af-4e0b4f7e0cb2'),(40,1952410,'CO2004','CC02',201,2,1,'2021-04-26 15:15:19','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952410%2Fattendance%2Fphotos%2F2021-04-26%2015:15:19.jpg?generation=1619424920431953&alt=media&token=262aaa8c-857c-45b3-b937-6c2c37653911'),(41,1952512,'CO2004','CC02',201,2,1,'2021-04-26 15:15:36','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952512%2Fattendance%2Fphotos%2F2021-04-26%2015:15:36.jpg?generation=1619424936835096&alt=media&token=04377b13-1a04-4772-b095-88ca643156e0'),(42,1952139,'CO2004','CC02',201,2,1,'2021-04-26 15:15:54','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952139%2Fattendance%2Fphotos%2F2021-04-26%2015:15:54.jpg?generation=1619424954589272&alt=media&token=ef772775-d50c-4551-894c-c73ea9263970'),(43,1952315,'CO2004','CC02',201,2,1,'2021-04-26 15:16:06','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952315%2Fattendance%2Fphotos%2F2021-04-26%2015:16:06.jpg?generation=1619424967282235&alt=media&token=fc83493f-417d-43ce-ba5a-6d2cefdf2a48'),(44,1952536,'CO2004','CC02',201,2,1,'2021-04-26 15:16:30','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952536%2Fattendance%2Fphotos%2F2021-04-26%2015:16:30.jpg?generation=1619424990939794&alt=media&token=b1a91aeb-175c-4c0d-9564-91af08d87527'),(45,1852502,'CO2004','CC02',201,2,1,'2021-04-26 15:16:41','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1852502%2Fattendance%2Fphotos%2F2021-04-26%2015:16:41.jpg?generation=1619425002039316&alt=media&token=fc844128-385c-4e5d-aa8c-130076e5463d'),(46,1850059,'CO2004','CC02',201,2,1,'2021-04-26 15:17:06','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1850059%2Fattendance%2Fphotos%2F2021-04-26%2015:17:06.jpg?generation=1619425026566256&alt=media&token=af192b27-fdd4-41ec-a0bd-68c4fb18e1f1'),(47,1852136,'CO2004','CC02',201,2,1,'2021-04-26 15:18:19','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1852136%2Fattendance%2Fphotos%2F2021-04-26%2015:18:19.jpg?generation=1619425100472521&alt=media&token=97d229a4-5978-4e69-ae89-0b879275fa6d'),(48,1752160,'CO2004','CC02',201,2,1,'2021-04-26 15:18:33','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752160%2Fattendance%2Fphotos%2F2021-04-26%2015:18:33.jpg?generation=1619425113891106&alt=media&token=7ab86d37-4991-4da9-a410-78e0b37a999e'),(49,1852618,'CO2004','CC02',201,2,1,'2021-04-26 15:18:47','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1852618%2Fattendance%2Fphotos%2F2021-04-26%2015:18:47.jpg?generation=1619425127571684&alt=media&token=c2cdd815-352d-427b-9ae7-47aa741d2496'),(50,1952240,'CO2004','CC02',201,2,1,'2021-04-26 15:19:07','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952240%2Fattendance%2Fphotos%2F2021-04-26%2015:19:07.jpg?generation=1619425148040757&alt=media&token=57989e70-f57f-485b-bbd7-21795abe74b9'),(51,1952418,'CO2004','CC02',201,2,1,'2021-04-26 15:19:18','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952418%2Fattendance%2Fphotos%2F2021-04-26%2015:19:18.jpg?generation=1619425158563297&alt=media&token=6dbb5944-e986-4888-8640-21042d5e2ae2'),(52,1852086,'CO2004','CC02',201,2,1,'2021-04-26 15:19:35','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1852086%2Fattendance%2Fphotos%2F2021-04-26%2015:19:35.jpg?generation=1619425176225911&alt=media&token=35444707-4675-4de3-bb73-792b4851804f'),(53,1852006,'CO2004','CC02',201,2,1,'2021-04-26 15:20:20','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1852006%2Fattendance%2Fphotos%2F2021-04-26%2015:20:20.jpg?generation=1619425220839958&alt=media&token=e802e6e8-d507-4dca-b7e8-bbf7feef7bbc'),(54,1852374,'CO2004','CC02',201,2,1,'2021-04-26 15:20:34','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1852374%2Fattendance%2Fphotos%2F2021-04-26%2015:20:34.jpg?generation=1619425235331621&alt=media&token=8717b4f6-9fca-4687-aa08-0fe85cce5fcc'),(55,1952037,'CO2004','CC02',201,2,1,'2021-04-26 15:20:51','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952037%2Fattendance%2Fphotos%2F2021-04-26%2015:20:51.jpg?generation=1619425252277462&alt=media&token=a75ae095-336d-4e21-9efb-9e5a920c8620'),(56,1952858,'CO2004','CC02',201,2,1,'2021-04-26 15:20:58','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952858%2Fattendance%2Fphotos%2F2021-04-26%2015:20:58.jpg?generation=1619425259326670&alt=media&token=a1ddb6d9-0a46-48a8-b174-cd66ded96eda'),(57,1952017,'CO2004','CC02',201,2,1,'2021-04-26 15:21:16','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952017%2Fattendance%2Fphotos%2F2021-04-26%2015:21:16.jpg?generation=1619425276749825&alt=media&token=2e14a9b7-005e-4616-804d-681c12358280'),(58,1952092,'CO2004','CC02',201,2,1,'2021-04-26 15:21:23','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952092%2Fattendance%2Fphotos%2F2021-04-26%2015:21:23.jpg?generation=1619425283701900&alt=media&token=1263a828-fdad-42d8-8133-94b07b43708b'),(59,1952088,'CO2004','CC02',201,2,1,'2021-04-26 15:21:33','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1952088%2Fattendance%2Fphotos%2F2021-04-26%2015:21:33.jpg?generation=1619425293982064&alt=media&token=7e1e2f9e-8eec-442b-b221-d8c89c9db0e4'),(73,1752041,'CO3025','CC01',201,2,1,'2021-04-27 10:18:15','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752041%2Fattendance%2Fphotos%2F2021-04-27%2010:18:15.jpg?generation=1619493496595085&alt=media&token=04524617-ee44-4cf4-95d0-0deac15590fa'),(74,1712187,'CO3025','CC01',201,2,1,'2021-04-27 10:18:29','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1712187%2Fattendance%2Fphotos%2F2021-04-27%2010:18:29.jpg?generation=1619493510202717&alt=media&token=6d7d7911-97f9-4b08-add4-99aca1bf4f06'),(75,2053234,'CO3025','CC01',201,2,1,'2021-04-27 10:18:59','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F2053234%2Fattendance%2Fphotos%2F2021-04-27%2010:18:59.jpg?generation=1619493539638241&alt=media&token=353839df-b856-40b4-b027-0f18d481a9c1'),(76,1752139,'CO3025','CC01',201,2,1,'2021-04-27 10:19:22','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752139%2Fattendance%2Fphotos%2F2021-04-27%2010:19:22.jpg?generation=1619493563082236&alt=media&token=67518137-b096-4779-87d8-7b0e9b004118'),(77,1752259,'CO3025','CC01',201,2,1,'2021-04-27 10:20:17','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752259%2Fattendance%2Fphotos%2F2021-04-27%2010:20:17.jpg?generation=1619493617813806&alt=media&token=43ae2402-7efa-444e-9dbb-ac41cff337ef'),(78,1752044,'CO3025','CC01',201,2,1,'2021-04-27 10:22:41','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752044%2Fattendance%2Fphotos%2F2021-04-27%2010:22:41.jpg?generation=1619494002606227&alt=media&token=da944758-c12a-4be8-bf85-82cd9289bb46'),(79,1752089,'CO3025','CC01',201,2,1,'2021-04-27 10:29:22','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752089%2Fattendance%2Fphotos%2F2021-04-27%2010:29:22.jpg?generation=1619494163344531&alt=media&token=ad393dcf-1821-4d40-a669-adc1030d4651'),(80,1752494,'CO3025','CC01',201,2,1,'2021-04-27 10:30:03','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752494%2Fattendance%2Fphotos%2F2021-04-27%2010:30:03.jpg?generation=1619494203388491&alt=media&token=11ca3cfa-cbe8-4fbe-a161-159aa8353671'),(81,1752516,'CO3025','CC01',201,2,1,'2021-04-27 10:30:35','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752516%2Fattendance%2Fphotos%2F2021-04-27%2010:30:35.jpg?generation=1619494235526812&alt=media&token=740455d9-44f8-4388-b9a2-665a11fec8e9'),(82,1752394,'CO3025','CC01',201,2,1,'2021-04-27 10:34:46','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752394%2Fattendance%2Fphotos%2F2021-04-27%2010:34:46.jpg?generation=1619494487329110&alt=media&token=25c19cbc-6673-4051-ad5d-667a78313f8e'),(83,1752067,'CO3025','CC01',201,2,1,'2021-04-27 10:35:02','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752067%2Fattendance%2Fphotos%2F2021-04-27%2010:35:02.jpg?generation=1619494503348528&alt=media&token=5c509275-1279-49fe-8ddd-601cf7397e2d'),(84,1652595,'CO3025','CC01',201,2,1,'2021-04-27 10:38:15','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1652595%2Fattendance%2Fphotos%2F2021-04-27%2010:38:15.jpg?generation=1619494695498571&alt=media&token=18170691-5873-4c79-907a-2ee0f8193607'),(85,1752015,'CO3025','CC01',201,2,1,'2021-04-27 10:47:39','https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752015%2Fattendance%2Fphotos%2F2021-04-27%2010:47:39.jpg?generation=1619495261569689&alt=media&token=48cc0168-eda0-4c2b-aff3-b70b5f25ddbd');
/*!40000 ALTER TABLE `attendance_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `id` int NOT NULL,
  `name` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'raspA');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollment`
--

DROP TABLE IF EXISTS `enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollment` (
  `user_id` int NOT NULL,
  `subject_id` varchar(15) NOT NULL,
  `group_code` varchar(10) NOT NULL,
  `semester` int NOT NULL,
  PRIMARY KEY (`user_id`,`subject_id`,`group_code`,`semester`),
  KEY `FK_subject_reference` (`subject_id`,`group_code`,`semester`),
  CONSTRAINT `FK_subject_reference` FOREIGN KEY (`subject_id`, `group_code`, `semester`) REFERENCES `subject` (`id`, `group_code`, `semester`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_user_reference` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollment`
--

LOCK TABLES `enrollment` WRITE;
/*!40000 ALTER TABLE `enrollment` DISABLE KEYS */;
INSERT INTO `enrollment` VALUES (1552423,'CO2004','CC02',201),(1652228,'CO2004','CC02',201),(1652342,'CO2004','CC02',201),(1752160,'CO2004','CC02',201),(1752176,'CO2004','CC02',201),(1752241,'CO2004','CC02',201),(1752384,'CO2004','CC02',201),(1752443,'CO2004','CC02',201),(1752637,'CO2004','CC02',201),(1810490,'CO2004','CC02',201),(1814498,'CO2004','CC02',201),(1850059,'CO2004','CC02',201),(1852006,'CO2004','CC02',201),(1852086,'CO2004','CC02',201),(1852136,'CO2004','CC02',201),(1852145,'CO2004','CC02',201),(1852330,'CO2004','CC02',201),(1852374,'CO2004','CC02',201),(1852471,'CO2004','CC02',201),(1852502,'CO2004','CC02',201),(1852580,'CO2004','CC02',201),(1852618,'CO2004','CC02',201),(1852827,'CO2004','CC02',201),(1911940,'CO2004','CC02',201),(1952017,'CO2004','CC02',201),(1952037,'CO2004','CC02',201),(1952088,'CO2004','CC02',201),(1952092,'CO2004','CC02',201),(1952139,'CO2004','CC02',201),(1952240,'CO2004','CC02',201),(1952315,'CO2004','CC02',201),(1952317,'CO2004','CC02',201),(1952410,'CO2004','CC02',201),(1952418,'CO2004','CC02',201),(1952512,'CO2004','CC02',201),(1952521,'CO2004','CC02',201),(1952536,'CO2004','CC02',201),(1952669,'CO2004','CC02',201),(1952684,'CO2004','CC02',201),(1952777,'CO2004','CC02',201),(1952858,'CO2004','CC02',201),(1953018,'CO2004','CC02',201),(1953046,'CO2004','CC02',201),(1953087,'CO2004','CC02',201),(1614058,'CO3025','CC01',201),(1652595,'CO3025','CC01',201),(1712187,'CO3025','CC01',201),(1752015,'CO3025','CC01',201),(1752041,'CO3025','CC01',201),(1752044,'CO3025','CC01',201),(1752067,'CO3025','CC01',201),(1752089,'CO3025','CC01',201),(1752139,'CO3025','CC01',201),(1752169,'CO3025','CC01',201),(1752244,'CO3025','CC01',201),(1752255,'CO3025','CC01',201),(1752259,'CO3025','CC01',201),(1752290,'CO3025','CC01',201),(1752335,'CO3025','CC01',201),(1752394,'CO3025','CC01',201),(1752494,'CO3025','CC01',201),(1752516,'CO3025','CC01',201),(1752522,'CO3025','CC01',201),(1752567,'CO3025','CC01',201),(1752637,'CO3025','CC01',201),(2053234,'CO3025','CC01',201);
/*!40000 ALTER TABLE `enrollment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `register`
--

DROP TABLE IF EXISTS `register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `register` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `image_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `register_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=381 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `register`
--

LOCK TABLES `register` WRITE;
/*!40000 ALTER TABLE `register` DISABLE KEYS */;
INSERT INTO `register` VALUES (277,1712187,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1712187%2Fregister%2Fphotos%2F0.jpg?generation=1618910597075937&alt=media'),(278,1712187,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1712187%2Fregister%2Fphotos%2F1.jpg?generation=1618910599261040&alt=media'),(279,1752015,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752015%2Fregister%2Fphotos%2F0.jpg?generation=1618909976464755&alt=media'),(280,1752015,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752015%2Fregister%2Fphotos%2F1.jpg?generation=1618909978970310&alt=media'),(281,1752041,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752041%2Fregister%2Fphotos%2F0.jpg?generation=1618910318497475&alt=media'),(282,1752044,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752044%2Fregister%2Fphotos%2F0.jpg?generation=1618909284683413&alt=media'),(283,1752044,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752044%2Fregister%2Fphotos%2F1.jpg?generation=1618909287023877&alt=media'),(284,1752067,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752067%2Fregister%2Fphotos%2F0.jpg?generation=1618910488579676&alt=media'),(285,1752067,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752067%2Fregister%2Fphotos%2F1.jpg?generation=1618910491029333&alt=media'),(286,1752089,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752089%2Fregister%2Fphotos%2F0.jpg?generation=1618910608046330&alt=media'),(287,1752089,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752089%2Fregister%2Fphotos%2F1.jpg?generation=1618910610256887&alt=media'),(288,1752139,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752139%2Fregister%2Fphotos%2F0.jpg?generation=1618909539328983&alt=media'),(289,1752139,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752139%2Fregister%2Fphotos%2F1.jpg?generation=1618909541466871&alt=media'),(290,1752259,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752259%2Fregister%2Fphotos%2F0.jpg?generation=1618910203306224&alt=media'),(291,1752259,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752259%2Fregister%2Fphotos%2F1.jpg?generation=1618910205616203&alt=media'),(292,1752394,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752394%2Fregister%2Fphotos%2F0.jpg?generation=1618909207559713&alt=media'),(293,1752394,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752394%2Fregister%2Fphotos%2F1.jpg?generation=1618909210038155&alt=media'),(294,1752494,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752494%2Fregister%2Fphotos%2F0.jpg?generation=1618909373180142&alt=media'),(295,1752494,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752494%2Fregister%2Fphotos%2F1.jpg?generation=1618909375369304&alt=media'),(296,1752516,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752516%2Fregister%2Fphotos%2F0.jpg?generation=1618910057840666&alt=media'),(297,1752516,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752516%2Fregister%2Fphotos%2F1.jpg?generation=1618910060526213&alt=media'),(298,1752522,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752522%2Fregister%2Fphotos%2F0.jpg?generation=1618909425671377&alt=media'),(299,1752522,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1752522%2Fregister%2Fphotos%2F1.jpg?generation=1618909427779430&alt=media'),(300,2053234,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F2053234%2Fregister%2Fphotos%2F0.jpg?generation=1618909419232793&alt=media'),(301,2053234,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F2053234%2Fregister%2Fphotos%2F1.jpg?generation=1618909421720712&alt=media'),(302,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F0.jpg?generation=1618909170953893&alt=media'),(303,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F1.jpg?generation=1618909173351333&alt=media'),(304,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F10.jpg?generation=1619261157976254&alt=media'),(305,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F11.jpg?generation=1619259288144586&alt=media'),(306,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F12.jpg?generation=1619257541002982&alt=media'),(307,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F13.jpg?generation=1619260823803828&alt=media'),(308,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F14.jpg?generation=1619255496561657&alt=media'),(309,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F15.jpg?generation=1619260071131488&alt=media'),(310,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F16.jpg?generation=1619259292514397&alt=media'),(311,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F17.jpg?generation=1619256504460573&alt=media'),(312,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F18.jpg?generation=1619258263173572&alt=media'),(313,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F19.jpg?generation=1619257039772795&alt=media'),(314,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F2.jpg?generation=1618909003753691&alt=media'),(315,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F20.jpg?generation=1619255794072554&alt=media'),(316,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F21.jpg?generation=1619257090482499&alt=media'),(317,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F22.jpg?generation=1619255180143548&alt=media'),(318,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F23.jpg?generation=1619255547698417&alt=media'),(319,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F24.jpg?generation=1619256000194116&alt=media'),(320,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F25.jpg?generation=1619256034802311&alt=media'),(321,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F26.jpg?generation=1619254680001850&alt=media'),(322,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F27.jpg?generation=1619261679145370&alt=media'),(323,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F28.jpg?generation=1619256801723520&alt=media'),(324,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F29.jpg?generation=1619258804409659&alt=media'),(325,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F3.jpg?generation=1618909005685431&alt=media'),(326,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F30.jpg?generation=1619256518006243&alt=media'),(327,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F31.jpg?generation=1619254329712447&alt=media'),(328,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F32.jpg?generation=1619254612358524&alt=media'),(329,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F33.jpg?generation=1619256004653579&alt=media'),(330,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F34.jpg?generation=1619257033548999&alt=media'),(331,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F35.jpg?generation=1619260900254424&alt=media'),(332,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F36.jpg?generation=1619254356523327&alt=media'),(333,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F37.jpg?generation=1619258467950869&alt=media'),(334,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F38.jpg?generation=1619256289572208&alt=media'),(335,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F39.jpg?generation=1619257518871176&alt=media'),(336,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F4.jpg?generation=1619255675364129&alt=media'),(337,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F40.jpg?generation=1619259361299129&alt=media'),(338,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F41.jpg?generation=1619259696242520&alt=media'),(339,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F42.jpg?generation=1619260841476459&alt=media'),(340,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F43.jpg?generation=1619259020886288&alt=media'),(341,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F44.jpg?generation=1619256941493799&alt=media'),(342,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F45.jpg?generation=1619261709672277&alt=media'),(343,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F46.jpg?generation=1619254539347903&alt=media'),(344,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F47.jpg?generation=1619255428535579&alt=media'),(345,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F48.jpg?generation=1619256154937264&alt=media'),(346,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F49.jpg?generation=1619261713712534&alt=media'),(347,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F5.jpg?generation=1619257141339856&alt=media'),(348,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F50.jpg?generation=1619255198321906&alt=media'),(349,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F51.jpg?generation=1619254102287154&alt=media'),(350,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F52.jpg?generation=1619256144444015&alt=media'),(351,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F53.jpg?generation=1619253697919129&alt=media'),(352,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F54.jpg?generation=1619258392476319&alt=media'),(353,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F55.jpg?generation=1619256041904692&alt=media'),(354,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F56.jpg?generation=1619255235845051&alt=media'),(355,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F57.jpg?generation=1619260778416971&alt=media'),(356,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F58.jpg?generation=1619261770866030&alt=media'),(357,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F59.jpg?generation=1619254164406611&alt=media'),(358,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F6.jpg?generation=1619254749111239&alt=media'),(359,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F60.jpg?generation=1619258675809869&alt=media'),(360,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F61.jpg?generation=1619256052365774&alt=media'),(361,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F62.jpg?generation=1619255397223739&alt=media'),(362,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F63.jpg?generation=1619259512911088&alt=media'),(363,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F64.jpg?generation=1619254160263176&alt=media'),(364,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F65.jpg?generation=1619260372884515&alt=media'),(365,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F66.jpg?generation=1619256762457646&alt=media'),(366,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F67.jpg?generation=1619253836166491&alt=media'),(367,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F68.jpg?generation=1619256175720444&alt=media'),(368,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F69.jpg?generation=1619263077384594&alt=media'),(369,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F7.jpg?generation=1619262197645262&alt=media'),(370,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F70.jpg?generation=1619260849371948&alt=media'),(371,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F71.jpg?generation=1619258056263825&alt=media'),(372,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F72.jpg?generation=1619260634277833&alt=media'),(373,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F73.jpg?generation=1619259431649761&alt=media'),(374,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F74.jpg?generation=1619261769162701&alt=media'),(375,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F75.jpg?generation=1619256579628035&alt=media'),(376,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F76.jpg?generation=1619259702525517&alt=media'),(377,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F77.jpg?generation=1619258378812849&alt=media'),(378,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F78.jpg?generation=1619255870455348&alt=media'),(379,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F79.jpg?generation=1619261758708163&alt=media'),(380,1614058,'https://firebasestorage.googleapis.com/v0/b/capstone-bk.appspot.com/o/student%2F1614058%2Fregister%2Fphotos%2F8.jpg?generation=1619256777652428&alt=media');
/*!40000 ALTER TABLE `register` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'STUDENT'),(2,'TEACHER'),(3,'ADMIN');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int DEFAULT NULL,
  `device_id` int DEFAULT NULL,
  `subject_id` varchar(15) NOT NULL,
  `group_code` varchar(10) NOT NULL,
  `semester` int NOT NULL,
  `start_time` varchar(30) DEFAULT NULL,
  `end_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `subject_id` (`subject_id`,`group_code`,`semester`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`),
  CONSTRAINT `schedule_ibfk_2` FOREIGN KEY (`subject_id`, `group_code`, `semester`) REFERENCES `subject` (`id`, `group_code`, `semester`),
  CONSTRAINT `schedule_ibfk_3` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=193 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (183,2,1,'CO3025','CC01',201,'2021-04-22 10:33:49','2021-04-22 12:10:00'),(187,2,1,'CO2004','CC02',201,'2021-04-26 15:00:44','2021-04-26 16:00:00'),(189,2,1,'CO2004','CC02',201,'2021-04-26 18:00:45','2021-04-26 20:00:00'),(190,2,1,'CO3025','CC01',201,'2021-04-27 10:00:08','2021-04-27 11:50:00'),(191,2,1,'CO3025','CC01',201,'2021-04-27 16:20:39','2021-04-27 16:40:00'),(192,2,1,'CO3025','CC01',201,'2021-04-29 10:00:31','2021-04-29 11:55:00');
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `id` varchar(15) NOT NULL,
  `group_code` varchar(10) NOT NULL,
  `semester` int NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`,`group_code`,`semester`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES ('CO2004','CC02',201,'Data Structures and Algorithms'),('CO3025','CC01',201,'System Design and Analysis');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_subject`
--

DROP TABLE IF EXISTS `teacher_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_subject` (
  `user_id` int NOT NULL,
  `subject_id` varchar(15) NOT NULL,
  `group_code` varchar(10) NOT NULL,
  `semester` int NOT NULL,
  PRIMARY KEY (`user_id`,`subject_id`,`group_code`,`semester`),
  KEY `subject_id` (`subject_id`,`group_code`,`semester`),
  CONSTRAINT `teacher_subject_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `teacher_subject_ibfk_2` FOREIGN KEY (`subject_id`, `group_code`, `semester`) REFERENCES `subject` (`id`, `group_code`, `semester`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_subject`
--

LOCK TABLES `teacher_subject` WRITE;
/*!40000 ALTER TABLE `teacher_subject` DISABLE KEYS */;
INSERT INTO `teacher_subject` VALUES (2,'CO2004','CC02',201),(2,'CO3025','CC01',201);
/*!40000 ALTER TABLE `teacher_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (0,'$2a$10$Wr0zXQsuv0He7phdsy/.fumh9DU2p7C9mxZFYJvMwNkh/nUZaFK7a'),(1,'$2a$10$7PcYgfOoDVIBp6XH7EjfKumEUbKvjwrHhPc46H4OejG4bmzkFp7Lm'),(2,'$2a$10$3uD1Tq8igj9tAcCwx20B4e8QUuejz8PpoDG8.cFKTs0ZsQKCqqrnG'),(1552423,'$2a$10$bTleCoVLzianETBhxGYxJukfpTPN1KH6DVpEN5mea6DQFo7uTuEoC'),(1614058,'$2a$10$H1B.kOLTCUbOlF3ndx.Rv.0f4fgRM5/t1GiEitCER2srMKvDzQSku'),(1652228,'$2a$10$4DBn7D0X82ShxcyqJUDI/uezdQhIQUQ.gF1a6LLEdruNDrx/aet2S'),(1652342,'$2a$10$36KQN/x5DiAnE4ivFArqbeG2u83Hsi.hrOVNESMzrA3HnFAdxBOdK'),(1652595,'$2a$10$B2zJaNS6XkDbZ4LnUr0iMuPKJrF.bLSexo3zLSVG0hgb8ghwwOiHa'),(1712187,'$2a$10$CD3BzhTKHQmzgqCMC6Y2q.MpDeaxb2O3vSS2Mhe.lrRw0/QS0/7HS'),(1752015,'$2a$10$u5jNRBHK1e33ejMmMstGquqkz2xIV5ZbBVtZQS/zNNopuu1FsK1h.'),(1752041,'$2a$10$.WiMaDXJbhl04fRxcGT9g.LjUoHAu9G1VtEKimAOhb6F2T1bbH4/6'),(1752044,'$2a$10$Vc0vTGR2K2lvjmlBup9byOtvoB1fFA0hOSrHKNSLTybG8HdmEzVu2'),(1752067,'$2a$10$tHLvkVFf4/mKtv2NClwlZ.QNdckZxsW4H1Z5GBAFqL1z96q54C3o.'),(1752089,'$2a$10$2ofgl3oYSiUir/jRg0u88.8ola98OJjYvsa4RYOzER4k4kjzYzwCW'),(1752139,'$2a$10$O9zPZRfUxOz/wxmMTAu6YuRBXpZD.4RySfepklxA8lvpl/3lMkbDu'),(1752160,'$2a$10$NrkGk4.4ryX5vF1eeegHWezgT0GtcAKvfGOmj7AG4tDwmiqtNttyC'),(1752169,'$2a$10$IeBkrEq.lFSPTkwv39t59uI4ZS1K2/q1NHEpJAIF7CKQgbIrr5A4C'),(1752176,'$2a$10$JrDUv4gDVmPPTnHE00.tp.sqJtpUfYJ0sniO6wrIo6ITgB2seTUU6'),(1752241,'$2a$10$yYrngzzlihl1FwriWNTbY.KsPlZqYDY.2fwDAFsDtTDk0hN3XkyLS'),(1752244,'$2a$10$ut1AlKbl/uHA3FEGb36OPOcRFPmRbTC29ZmgB7rZ/usb5dGLkLnUC'),(1752255,'$2a$10$49ORYAMg6gXLil976izu/uB4OJp.AqT7ZqOO.vQ1GZpxpFxSQamDC'),(1752259,'$2a$10$ICtSa1lTQNGwFB0iGRF9R.cNIUZOXMf/J8ux/Dopmq.I7tTcR/RBm'),(1752290,'$2a$10$CK7IvRBgMBzzgiVDWQ7tAepglbesdfOwhO87b7xYlrEviO/TDEDm6'),(1752335,'$2a$10$v2BAsnEu1yWOtmUiD3LvEOsPF0S3RBDxP8exA/WczCrLZzcJlsbJe'),(1752384,'$2a$10$nnVgxTsa9kVUKYR.tZZi2O1Tjbv3w/6iGQUUSsy.cgpoH2O/BL1AG'),(1752394,'$2a$10$iwIP7IiwKT69bpkNNLRAXOExA9gjwYvqJY..X4NEiVJLHsO4RBjEe'),(1752443,'$2a$10$ONgpvrjhwdnK10zRm6TJ0utLcNet89/BVSN/xOqGZRkcGFtRHktfu'),(1752494,'$2a$10$cB7hfED6BqGFVVmH074mgO7awTmYYKPI3mV0fSJS42/k3KUrENI1G'),(1752516,'$2a$10$kJHZuKajL4WR37giaSB2VemY8/JlZVj7SReEdFIczhaiPEj8qDLAq'),(1752522,'$2a$10$.UMHUY8nGWzCicOcLQfCreZyI9WzCsL3l88POnVZQ4PuuTUmJtHVG'),(1752567,'$2a$10$.YatNOQ9Su1bISDUOUb9Qe6eyyCZsGgRc1MfEiw8rXGARLGwP7ezW'),(1752637,'$2a$10$IYw6J2PT2MIuiOylVMpus.gttZVwwhjMz1WNZqNHimhpxVL7w8H8m'),(1810490,'$2a$10$uxMvjmVmmWuidCq9BCz9veXTuwztHdtdP5czrf.am8NobXf0nWumC'),(1814498,'$2a$10$TTFR8Cm25Tu2Z0MA9JW8A.x/bjTbDfb/0ZYkhbj1rKMSn7R67srw2'),(1850059,'$2a$10$EAdkCwe6ZkmAWs.SX0ihMuEjK6X5HWKVOU9E/9QI4fxeDtip1GYc6'),(1852006,'$2a$10$nGbjhHV4O5sORGzmTqs2.e.xhU7Z57Z5P54WHnCeFcaeJ0NP7LpPi'),(1852086,'$2a$10$wrML.JWhwfMRt3cbQxsjRe82WOlYNWUtabIBtx351iz/JHJoaJqp2'),(1852136,'$2a$10$u.4p2JsFXZvNa9NVUgnq1ux2ZyXeA7jyABN./S3fZvVq0/a/JBWcm'),(1852145,'$2a$10$OIuyrJMm67cc1JyoKxiDDekJhBQ4DqVvnQkn7f8HOcO7OzNLXO0Rq'),(1852330,'$2a$10$yEqdE757fB4JNdZxnqSRxudD5H03JxgOpU8I1ZuBvM12/Pz9Ug1v2'),(1852374,'$2a$10$RjOM82OjMz98x5OYeDJAWOqh6Qr6GuTp14Ucvabcj9J5qx2mF8ndK'),(1852471,'$2a$10$Bcf81WpIzBA412yZ91E8r.Sb.wLzbrb61cJpsFQ2.Bag5d74tIYt2'),(1852502,'$2a$10$enLWtyqVcO5TRINLQ.Sib.Wdgw4lMYDrCN.mTdqeae26z8H9yElf2'),(1852580,'$2a$10$vDWjwRfrzpT0CM2KvsoVS.bG.lYSr8DbI9AQWuKpegtYElHUzd3aq'),(1852618,'$2a$10$/cn9/of.WwgGOCZQs5ULU.VHAWyqcjF8IP3jg0xMuiq/LiQqexF9O'),(1852827,'$2a$10$.WMPvb58R3QvCBfaSmpR6uTkZjdNHRXobRz0keCuivyHU5eiIXp6W'),(1911940,'$2a$10$HzuYQxwMlBnQKUir5Bah2udpdol.LPRsp2cxAOe0tesNG9hgGUPr.'),(1952017,'$2a$10$KKAJMMXbZLf8cJDH1wNCBenzWukVB51TvgaSuPEHYfdWXOIurSQJ.'),(1952037,'$2a$10$09BLYhYWaMS9aXJ4EebP4e6UqvKBhnoP8U6RVJbs6jrIx15Gy9obi'),(1952088,'$2a$10$feJR3z6p46MSjo63933KQOb3EsmxMu0.ll56mRhJA1u97FUDzu87G'),(1952092,'$2a$10$n4CJtoUA.Y3kP.hR3IM6ZeBy0G9hr234H06yXI5yrVfQ2um4Ohv9q'),(1952139,'$2a$10$SypeBBniObqnCcb/jcrFkO0jy1.uDFZl4eibDtane1Onv4nqmeNFu'),(1952240,'$2a$10$ZwiovTL/VF6ULrtYxSBWk.XOsKS./knIi4BG9I6ff94McSW17QE5.'),(1952315,'$2a$10$3/Qdgrb61Uu5NoLVvYMzse/rGLXRuTYZ5Q2NMjYBw/QFg8.MoFp5S'),(1952317,'$2a$10$rU4RKMK/fsKG9ocHguF9puTa2wHIis8O1rRUV.F9mTI9/vcnspBa6'),(1952410,'$2a$10$FcqJOIkWovK1VGEQ09sf0.t.PnjpfAhSKtidFDpEf2cw1rk8n9K4i'),(1952418,'$2a$10$08OE/P0k5Xq0pnMA1MJEOu/ECQbIc52zIeC.eilHqEpqsa.fE.NzW'),(1952512,'$2a$10$SF85gjvISLBwFn2cgxk9ze27XgPl4/kxp4cakLaV5YBmr394xjwj.'),(1952521,'$2a$10$AgnOH8p7kP2yP4zNneNIJOWiVOYf6eGu0NerF5jDW/y5IVeRKnnCu'),(1952536,'$2a$10$3cR4GqYW/xTFAKprqCf.HeoW22GdFt1zW2vEB57dhdvzY5uxJMwam'),(1952669,'$2a$10$ELqQ69MUIloVZmQQt.eCPO/y15BFCpQb3ZVPm2SzJlHCRty9YoWpy'),(1952684,'$2a$10$NfWy5FvUA5eKbFOKaxVwDeytlHl/sVW5BnCUUCT4LcQ3p3d.Mqgsu'),(1952777,'$2a$10$5KTkPS8AxGN9uJZblW77P.QF7H9s4cB13sOXLDvrbCZvZtxWxBHM6'),(1952858,'$2a$10$/rlZGrzy6NMUuxUJJE9J5eKoKqU87WqV4pzfhDeaPmcyijOUFdx4O'),(1953018,'$2a$10$iVS4x/JmsFN260x0rKzOVujz5toVBDaBrpIT6IGJWLweTa9w6wtoe'),(1953046,'$2a$10$VqzGgk3ME6SKjdVIh1dgVO.D.4LeBptbXdGz1bFwDcT5njcAN3IKq'),(1953087,'$2a$10$gxhZRZx4VZoQEwXLMZ6Dpe.2agUkCR2MSdLspD6Trh43chXt.tX/6'),(2053234,'$2a$10$.T0diJtjB06P7m6vwjnQvev4thA6wJmfZN7Vqo00uOX1d4R4px9Ve');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` VALUES (3,1,3),(413,2,2),(436,1614058,1),(437,1652595,1),(438,1712187,1),(439,1752015,1),(440,1752041,1),(441,1752044,1),(442,1752067,1),(443,1752089,1),(444,1752139,1),(445,1752169,1),(446,1752244,1),(447,1752255,1),(448,1752259,1),(449,1752290,1),(450,1752335,1),(451,1752394,1),(452,1752494,1),(453,1752516,1),(454,1752522,1),(455,1752567,1),(456,1752637,1),(457,2053234,1),(458,1852471,1),(459,1952315,1),(460,1852502,1),(461,1652342,1),(462,1952317,1),(463,1952088,1),(464,1952092,1),(465,1852580,1),(466,1952858,1),(467,1952418,1),(468,1911940,1),(469,1952410,1),(470,1752443,1),(471,1852086,1),(472,1953018,1),(473,1952139,1),(474,1953046,1),(475,1814498,1),(476,1952512,1),(477,1953087,1),(478,1952521,1),(479,1552423,1),(480,1850059,1),(481,1952536,1),(482,1752176,1),(483,1852330,1),(484,1752160,1),(485,1852618,1),(486,1852136,1),(487,1810490,1),(488,1752384,1),(489,1852827,1),(490,1852006,1),(491,1952017,1),(492,1952037,1),(493,1952240,1),(494,1952669,1),(495,1852374,1),(496,1952684,1),(497,1852145,1),(498,1652228,1),(499,1752241,1),(500,1952777,1);
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-08 11:35:39
