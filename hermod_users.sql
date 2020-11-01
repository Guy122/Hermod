-- MySQL dump 10.13  Distrib 5.7.32, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: hermod
-- ------------------------------------------------------
-- Server version	5.7.32-0ubuntu0.18.04.1

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `mdn` varchar(45) NOT NULL,
  `networkName` varchar(45) DEFAULT NULL,
  `accountId` varchar(45) DEFAULT NULL,
  `subscriptionType` int(11) DEFAULT NULL,
  `payType` int(11) DEFAULT NULL,
  `pairingInd` tinyint(4) DEFAULT NULL,
  `corporateName` varchar(45) DEFAULT NULL,
  `subsClientType` int(11) DEFAULT NULL,
  `addPackageInfo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`mdn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('+9728878010','DD879','HFC_LAB555',2,0,1,'HFC_LAB',1,'{\"tierPkgId\":\"TIER2\"}'),('+9728878012','DD00','HFC_LAB',2,0,1,'HFC_LAB',1,'{\"tierPkgId\":\"TIER2\"}'),('+9728878017','DD8889','HFC_LAB',2,0,1,'HFC_LAB',1,'{tierPkgId:TIER2}'),('87288780171','DD8889','HFC_LAB',2,0,1,'HFC_LAB',1,'{tierPkgId:TIER2}'),('97288780171','DD8889','HFC_LAB',2,0,1,'HFC_LAB',1,'{tierPkgId:TIER2}'),('972887801711','DD8889','HFC_LAB',2,0,1,'HFC_LAB',1,'{tierPkgId:TIER2}');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-01 16:33:05
