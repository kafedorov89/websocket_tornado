CREATE DATABASE  IF NOT EXISTS `electrolab` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `electrolab`;
-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: electrolab
-- ------------------------------------------------------
-- Server version	5.5.46-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `main_standtask_data`
--

DROP TABLE IF EXISTS `main_standtask_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_standtask_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `standtask_name` varchar(100) DEFAULT NULL,
  `standtask_id` int(11) NOT NULL,
  `conn_json` longtext,
  `rope_json` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_standtask_data`
--

LOCK TABLES `main_standtask_data` WRITE;
/*!40000 ALTER TABLE `main_standtask_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_standtask_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_standtask_state`
--

DROP TABLE IF EXISTS `main_standtask_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_standtask_state` (
  `id` int(11) NOT NULL,
  `standtask_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_rope_json` longtext,
  `activate` tinyint(1) DEFAULT NULL,
  `complete` tinyint(1) DEFAULT NULL,
  `error` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_standtask_state`
--

LOCK TABLES `main_standtask_state` WRITE;
/*!40000 ALTER TABLE `main_standtask_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_standtask_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_training_log`
--

DROP TABLE IF EXISTS `main_training_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_training_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `training_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `complete` tinyint(1) DEFAULT NULL,
  `event_list` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_training_log`
--

LOCK TABLES `main_training_log` WRITE;
/*!40000 ALTER TABLE `main_training_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_training_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_training_param_state`
--

DROP TABLE IF EXISTS `main_training_param_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_training_param_state` (
  `id` varchar(100) NOT NULL,
  `bool_value` tinyint(1) DEFAULT NULL,
  `int_value` int(11) DEFAULT NULL,
  `float_value` float DEFAULT NULL,
  `string_value` varchar(500) DEFAULT NULL,
  `vector3_value` varchar(300) DEFAULT NULL,
  `vector2_value` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_training_param_state`
--

LOCK TABLES `main_training_param_state` WRITE;
/*!40000 ALTER TABLE `main_training_param_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_training_param_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_training_state`
--

DROP TABLE IF EXISTS `main_training_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_training_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `training_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `online` tinyint(1) DEFAULT NULL,
  `activate` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_training_state`
--

LOCK TABLES `main_training_state` WRITE;
/*!40000 ALTER TABLE `main_training_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_training_state` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-06  4:39:56
