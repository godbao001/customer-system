mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: 10.0.1.70    Database: hsay_20260303
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `category_groups`
--

DROP TABLE IF EXISTS `category_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) NOT NULL COMMENT '分类组名称',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1=正常, 0=停用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_default` tinyint DEFAULT '0',
  `color` varchar(50) DEFAULT '' COMMENT '颜色',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_groups`
--

LOCK TABLES `category_groups` WRITE;
/*!40000 ALTER TABLE `category_groups` DISABLE KEYS */;
INSERT INTO `category_groups` VALUES (1,'小规模活动',0,1,'2026-03-03 13:37:15','2026-03-03 13:37:15',0,''),(2,'自定义',0,1,'2026-03-03 13:38:05','2026-03-03 13:38:05',0,'');
/*!40000 ALTER TABLE `category_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `field_config`
--

DROP TABLE IF EXISTS `field_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `field_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `field_type` varchar(50) NOT NULL COMMENT '字段类型: express_method/express_fee_type',
  `field_name` varchar(100) NOT NULL COMMENT '字段显示名称',
  `field_value` varchar(200) NOT NULL COMMENT '字段值',
  `sort_order` int DEFAULT NULL COMMENT '排序',
  `status` int DEFAULT NULL COMMENT '状态: 1=启用, 0=停用',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_default` int DEFAULT '0',
  `color` varchar(20) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `field_config`
--

LOCK TABLES `field_config` WRITE;
/*!40000 ALTER TABLE `field_config` DISABLE KEYS */;
INSERT INTO `field_config` VALUES (5,'express_method','滴滴','',97,1,'2026-03-06 16:45:40','2026-03-06 17:11:48',0,''),(6,'express_method','自提','',98,1,'2026-03-06 16:45:47','2026-03-06 17:00:39',0,''),(7,'express_method','顺丰快递','',99,1,'2026-03-06 16:47:58','2026-03-06 17:11:48',1,''),(8,'express_method','送货','',0,1,'2026-03-06 17:00:53','2026-03-06 17:11:34',0,''),(9,'business_model','直营店','',99,1,'2026-03-06 18:36:59','2026-03-09 17:34:00',0,'bg-danger'),(10,'business_model','加盟店','98',98,1,'2026-03-06 18:37:13','2026-03-09 17:35:41',1,''),(11,'business_model','办公地点','',50,1,'2026-03-06 18:37:26','2026-03-09 17:35:41',0,'bg-primary');
/*!40000 ALTER TABLE `field_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_logs`
--

DROP TABLE IF EXISTS `operation_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT '操作人ID',
  `username` varchar(50) DEFAULT NULL COMMENT '操作人用户名',
  `user_name` varchar(50) DEFAULT NULL COMMENT '操作人姓名',
  `category` varchar(50) NOT NULL COMMENT '操作分类: login/ logout/ shop/ product/ order/ user/ role/ system',
  `action` varchar(100) NOT NULL COMMENT '操作动作',
  `detail` text COMMENT '操作详情',
  `ip` varchar(50) DEFAULT NULL COMMENT 'IP地址',
  `result` varchar(20) DEFAULT NULL COMMENT '操作结果: success/ fail',
  `created_at` datetime DEFAULT NULL COMMENT '操作时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_logs`
--

LOCK TABLES `operation_logs` WRITE;
/*!40000 ALTER TABLE `operation_logs` DISABLE KEYS */;
INSERT INTO `operation_logs` VALUES (1,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 13:04:02'),(2,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 13:05:08'),(3,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 13:05:18'),(4,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 13:05:22'),(5,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 13:05:39'),(6,7,'xuzhiming','徐志铭','shop','停用店铺','店铺名称: 地方发的发','10.0.1.75','success','2026-03-12 13:11:25'),(7,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 13:16:28'),(8,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 13:16:34'),(9,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 13:16:39'),(10,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 13:16:44'),(11,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 13:16:49'),(12,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 13:17:45'),(13,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 13:18:20'),(14,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 13:18:27'),(15,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 13:18:33'),(16,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 13:19:35'),(17,7,'xuzhiming','徐志铭','user','修改用户角色','用户名: zhaoxin','10.0.1.75','success','2026-03-12 13:19:46'),(18,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 13:23:35'),(19,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 13:25:03'),(20,7,'xuzhiming','徐志铭','user','重置密码','用户名: zhaoxin','10.0.1.75','success','2026-03-12 13:46:37'),(21,7,'xuzhiming','徐志铭','user','停用用户','用户名: zhaoxin','10.0.1.75','success','2026-03-12 13:46:43'),(22,7,'xuzhiming','徐志铭','user','启用用户','用户名: zhaoxin','10.0.1.75','success','2026-03-12 13:46:48'),(23,7,'xuzhiming','徐志铭','user','修改用户角色','用户名: zhaoxin','10.0.1.75','success','2026-03-12 13:46:56'),(24,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 14:40:53'),(25,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 14:40:54'),(26,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 14:51:41'),(27,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 14:51:46'),(28,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 14:51:54'),(29,7,'xuzhiming','徐志铭','shop','添加店铺','店铺名称: dfdsdsdsgsgsd','10.0.1.75','success','2026-03-12 14:52:07'),(30,7,'xuzhiming','徐志铭','shop','停用店铺','店铺名称: dfdsdsdsgsgsd','10.0.1.75','success','2026-03-12 14:52:14'),(31,7,'xuzhiming','徐志铭','logout','退出登录','用户: 徐志铭(xuzhiming)','10.0.1.75','success','2026-03-12 14:53:01'),(32,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 14:53:03'),(33,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 14:56:37'),(34,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 14:59:18'),(35,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 15:01:03'),(36,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 15:56:36'),(37,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 15:56:42'),(38,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 16:04:02'),(39,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 16:04:13'),(40,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-12 16:05:15'),(41,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:05:42'),(42,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:07:00'),(43,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:07:07'),(44,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:07:43'),(45,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:09:25'),(46,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:10:17'),(47,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 卤当当p','10.0.1.75','success','2026-03-12 16:14:28'),(48,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 有间卤铺','10.0.1.75','success','2026-03-12 16:14:35'),(49,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 卤萌主j','10.0.1.75','success','2026-03-12 16:14:49'),(50,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 卤人甲uu','10.0.1.75','success','2026-03-12 16:15:03'),(51,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 辣友记方法','10.0.1.75','success','2026-03-12 16:21:55'),(52,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 老枝花卤','10.0.1.75','success','2026-03-12 16:22:02'),(53,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:29:00'),(54,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:29:07'),(55,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 16:29:13'),(56,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:31:51'),(57,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:32:05'),(58,7,'xuzhiming','徐志铭','logout','退出登录','用户: 徐志铭(xuzhiming)','10.0.1.75','success','2026-03-12 16:33:28'),(59,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:33:40'),(60,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 16:33:46'),(61,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:35:27'),(62,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:35:50'),(63,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:36:49'),(64,NULL,'','','logout','退出登录','用户: ()','10.0.1.75','success','2026-03-12 16:37:20'),(65,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:37:23'),(66,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:37:30'),(67,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 16:37:37'),(68,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:37:54'),(69,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 16:37:59'),(70,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:39:24'),(71,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:39:40'),(72,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:40:29'),(73,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:40:57'),(74,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:40:58'),(75,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 16:41:02'),(76,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 16:44:06'),(77,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 16:47:32'),(78,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 16:47:39'),(79,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-12 17:04:59'),(80,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:05:04'),(81,7,'xuzhiming','徐志铭','order','删除订单','订单号: ORD20260310170257992284','10.0.1.75','success','2026-03-12 17:14:55'),(82,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:21:55'),(83,7,'xuzhiming','徐志铭','order','删除订单','订单号: ORD20260306180732193710','10.0.1.75','success','2026-03-12 17:22:03'),(84,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:26:47'),(85,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260312172717910534, 店铺: 南开大悦城22店','10.0.1.75','success','2026-03-12 17:27:17'),(86,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:30:25'),(87,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:36:59'),(88,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:44:30'),(89,7,'xuzhiming','徐志铭','order','更新订单状态','订单号: ORD20260312172717910534, 下单未确认 → 确认未付款','10.0.1.75','success','2026-03-12 17:46:46'),(90,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:49:19'),(91,7,'xuzhiming','徐志铭','order','更新订单状态','订单号: ORD20260312172717910534, 确认未付款 → 付款未制作','10.0.1.75','success','2026-03-12 17:50:29'),(92,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:54:30'),(93,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:56:56'),(94,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 17:58:29'),(95,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 17:59:38'),(96,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 18:02:54'),(97,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 18:04:33'),(98,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 18:07:15'),(99,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','127.0.0.1','success','2026-03-12 18:10:23'),(100,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-12 18:10:44'),(101,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-16 17:50:00'),(102,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 17:50:05'),(103,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 17:53:25'),(104,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-16 17:54:22'),(105,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 17:55:23'),(106,7,'xuzhiming','徐志铭','shop','添加店铺','店铺名称: 是大扶桑岛国','10.0.1.75','success','2026-03-16 17:55:30'),(107,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 是大扶桑岛国','10.0.1.75','success','2026-03-16 17:55:35'),(108,7,'xuzhiming','徐志铭','shop','编辑店铺','店铺名称: 是大扶桑岛国','10.0.1.75','success','2026-03-16 17:55:46'),(109,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260316175558172024, 店铺: 是大扶桑岛国','10.0.1.75','success','2026-03-16 17:55:59'),(110,7,'xuzhiming','徐志铭','order','更新订单状态','订单号: ORD20260316175558172024, 下单未确认 → 确认未付款','10.0.1.75','success','2026-03-16 17:56:07'),(111,7,'xuzhiming','徐志铭','order','更新订单状态','订单号: ORD20260316175558172024, 确认未付款 → 付款未制作','10.0.1.75','success','2026-03-16 17:56:13'),(112,7,'xuzhiming','徐志铭','product','添加产品','产品名称: 地方是短发','10.0.1.75','success','2026-03-16 17:57:03'),(113,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:03:22'),(114,7,'xuzhiming','徐志铭','shop','添加店铺','店铺名称: 是的发送','10.0.1.75','success','2026-03-16 18:03:26'),(115,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:08:20'),(116,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:13:41'),(117,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260316181413527136, 店铺: 南开大悦城32店','10.0.1.75','success','2026-03-16 18:14:13'),(118,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260316181426874742, 店铺: 南开大悦城店4','10.0.1.75','success','2026-03-16 18:14:27'),(119,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260316181431500953, 店铺: 小鲜卤','10.0.1.75','success','2026-03-16 18:14:32'),(120,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260316181437222969, 店铺: 是的发送','10.0.1.75','success','2026-03-16 18:14:37'),(121,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260316181443971388, 店铺: 南开大悦城2店','10.0.1.75','success','2026-03-16 18:14:44'),(122,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:26:31'),(123,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:26:42'),(124,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-16 18:26:45'),(125,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:26:49'),(126,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-16 18:27:31'),(127,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:27:33'),(128,NULL,'','','login','用户登录','密码错误','127.0.0.1','fail','2026-03-16 18:28:41'),(129,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:29:10'),(130,NULL,'','','login','用户登录','密码错误','10.0.1.75','fail','2026-03-16 18:31:15'),(131,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:31:20'),(132,7,'xuzhiming','徐志铭','shop','添加店铺','店铺名称: sdfsdfsdfdf','10.0.1.75','success','2026-03-16 18:31:36'),(133,7,'xuzhiming','徐志铭','order','创建订单','订单号: ORD20260316183156530529, 店铺: sdfsdfsdfdf','10.0.1.75','success','2026-03-16 18:31:57'),(134,7,'xuzhiming','徐志铭','order','删除订单','订单号: ORD20260316183156530529','10.0.1.75','success','2026-03-16 18:32:04'),(135,7,'xuzhiming','徐志铭','login','用户登录','用户: 徐志铭','10.0.1.75','success','2026-03-16 18:38:02');
/*!40000 ALTER TABLE `operation_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL COMMENT '订单ID',
  `product_id` int DEFAULT NULL COMMENT '产品ID',
  `product_name` varchar(100) DEFAULT NULL COMMENT '产品名称',
  `price` decimal(10,2) DEFAULT '0.00' COMMENT '单价',
  `quantity` int DEFAULT '1' COMMENT '数量',
  `width` decimal(10,2) DEFAULT '0.00' COMMENT '宽度',
  `height` decimal(10,2) DEFAULT '0.00' COMMENT '高度',
  `remark` varchar(255) DEFAULT '' COMMENT '备注',
  `subtotal` decimal(10,2) DEFAULT '0.00' COMMENT '小计',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `original_width` decimal(10,2) DEFAULT '0.00' COMMENT '原始宽度',
  `original_height` decimal(10,2) DEFAULT '0.00' COMMENT '原始高度',
  `free_shipping` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单明细表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,2,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-05 15:54:30',0.00,0.00,0),(2,2,3,'[6090KT板]马年气氛',22.00,1,60.00,70.00,'',22.00,'2026-03-05 15:54:30',0.00,0.00,0),(5,5,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-05 17:37:29',20.00,30.00,0),(12,4,2,'[PVC吧台贴]马年氛围',10.00,2,20.00,30.00,'',20.00,'2026-03-06 14:40:07',20.00,30.00,0),(13,4,3,'[6090KT板]马年气氛',22.00,4,60.00,70.00,'',88.00,'2026-03-06 14:40:07',60.00,70.00,0),(14,6,4,'测试',10.00,1,0.00,0.00,'',10.00,'2026-03-06 16:03:24',0.00,0.00,0),(15,7,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-06 18:07:25',20.00,30.00,0),(16,7,3,'[6090KT板]马年气氛',22.00,1,60.00,70.00,'',22.00,'2026-03-06 18:07:25',60.00,70.00,0),(17,8,4,'测试',10.00,1,0.00,0.00,'',10.00,'2026-03-06 18:07:32',0.00,0.00,0),(24,9,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-10 11:45:17',20.00,30.00,0),(25,9,3,'[6090KT板]马年气氛',22.00,5,33.00,70.00,'',110.00,'2026-03-10 11:45:17',60.00,70.00,0),(26,9,3,'[6090KT板]马年气氛',22.00,2,6022.00,70.00,'',44.00,'2026-03-10 11:45:17',60.00,70.00,0),(27,3,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-10 11:48:27',20.00,30.00,0),(32,12,3,'[6090KT板]马年气氛',22.00,1,22.50,70.00,'',22.00,'2026-03-10 17:24:17',60.00,70.00,0),(33,13,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-12 17:27:17',20.00,30.00,0),(34,13,3,'[6090KT板]马年气氛',22.00,1,60.00,70.00,'',22.00,'2026-03-12 17:27:17',60.00,70.00,0),(35,14,2,'[PVC吧台贴]马年氛围',10.00,2,20.00,30.00,'',20.00,'2026-03-16 17:55:59',20.00,30.00,0),(36,15,2,'[PVC吧台贴]马年氛围',10.00,3,20.00,30.00,'',30.00,'2026-03-16 18:14:13',20.00,30.00,0),(37,16,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-16 18:14:27',20.00,30.00,0),(38,17,3,'[6090KT板]马年气氛',22.00,3,60.00,70.00,'',66.00,'2026-03-16 18:14:32',60.00,70.00,0),(39,18,2,'[PVC吧台贴]马年氛围',10.00,3,20.00,30.00,'',30.00,'2026-03-16 18:14:37',20.00,30.00,0),(40,19,2,'[PVC吧台贴]马年氛围',10.00,1,20.00,30.00,'',10.00,'2026-03-16 18:14:44',20.00,30.00,0),(41,20,2,'[PVC吧台贴]马年氛围',10.00,2,20.00,30.00,'',20.00,'2026-03-16 18:31:57',20.00,30.00,0);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` varchar(50) NOT NULL COMMENT '订单号',
  `shop_id` int NOT NULL COMMENT '店铺ID',
  `total_amount` decimal(10,2) DEFAULT '0.00' COMMENT '订单总金额',
  `status` tinyint DEFAULT '1' COMMENT '订单状态: 1=待支付, 2=已支付, 3=已完成, 4=已取消',
  `remark` text COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `express_shop_address` varchar(255) DEFAULT NULL,
  `express_shop_phone` varchar(50) DEFAULT NULL,
  `express_method` varchar(50) DEFAULT NULL,
  `express_fee_type` varchar(20) DEFAULT NULL,
  `express_fee` decimal(10,2) DEFAULT '0.00',
  `order_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
  `confirm_time` datetime DEFAULT NULL COMMENT '确认时间',
  `pay_time` datetime DEFAULT NULL COMMENT '付款时间',
  `make_time` datetime DEFAULT NULL COMMENT '制作时间',
  `pack_time` datetime DEFAULT NULL COMMENT '打包时间',
  `free_shipping` int DEFAULT '0',
  `is_deleted` int DEFAULT '0',
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_order_no` (`order_no`),
  KEY `idx_shop_id` (`shop_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (2,'ORD20260305155429398429',64,32.00,3,'','2026-03-05 15:54:30','2026-03-05 15:56:01','华北 天津市 天津市 南开区 大悦城3楼','18622238259','顺丰快递','寄付',0.00,'2026-03-05 15:54:30','2026-03-05 15:55:54','2026-03-05 15:56:01',NULL,NULL,0,0,NULL),(3,'ORD20260305160044261238',56,10.00,3,'','2026-03-05 16:00:44','2026-03-10 11:48:31','舟山市  定海区 人民南路80号','18622238259','顺丰快递','到付',0.00,'2026-03-05 16:00:44','2026-03-10 11:48:31','2026-03-10 11:48:31',NULL,NULL,0,0,NULL),(4,'ORD20260305163500784927',64,108.00,3,'','2026-03-05 16:35:01','2026-03-10 11:40:05','华北 天津市 天津市 南开区 大悦城3楼','18622238259','顺丰快递','寄付',0.00,'2026-03-05 16:35:01',NULL,'2026-03-10 11:40:05',NULL,NULL,0,0,NULL),(5,'ORD20260305173728221561',63,10.00,6,'','2026-03-05 17:37:29','2026-03-06 15:09:33','华北 天津市 天津市 南开区 大悦城2楼','','顺丰快递','到付',0.00,'2026-03-05 17:37:29','2026-03-06 15:04:56','2026-03-06 15:05:04','2026-03-06 15:07:55','2026-03-06 15:09:20',0,0,NULL),(6,'ORD20260306160324896855',64,10.00,3,'','2026-03-06 16:03:24','2026-03-10 11:42:19','华北 天津市 天津市 南开区 大悦城3楼','18622238259','顺丰快递','寄付',0.00,'2026-03-06 16:03:24',NULL,'2026-03-10 11:42:19',NULL,NULL,0,0,NULL),(7,'ORD20260306180724708972',64,32.00,1,'','2026-03-06 18:07:25','2026-03-06 18:07:25','华北 天津市 天津市 南开区 大悦城3楼','18622238259','顺丰快递','到付',0.00,'2026-03-06 18:07:25',NULL,NULL,NULL,NULL,0,0,NULL),(8,'ORD20260306180732193710',64,10.00,1,'','2026-03-06 18:07:32','2026-03-12 17:22:03','华北 天津市 天津市 南开区 大悦城3楼','18622238259','顺丰快递','寄付',0.00,'2026-03-06 18:07:32',NULL,NULL,NULL,NULL,0,1,'2026-03-12 17:22:03'),(9,'ORD20260310112032605635',68,164.00,3,'','2026-03-10 11:20:32','2026-03-10 11:45:24','华北 天津市 天津市 南开区 大悦城4楼','18622238259','顺丰快递','寄付',0.00,'2026-03-10 11:20:32',NULL,'2026-03-10 11:45:24',NULL,NULL,0,0,NULL),(12,'ORD20260310172416995633',68,22.00,3,'','2026-03-10 17:24:17','2026-03-10 18:17:17','华北 天津市 天津市 南开区 大悦城4楼','','顺丰快递','到付',0.00,'2026-03-10 17:24:17','2026-03-10 18:17:04','2026-03-10 18:17:17',NULL,NULL,0,0,NULL),(13,'ORD20260312172717910534',64,32.00,3,'','2026-03-12 17:27:17','2026-03-12 17:50:29','华北 天津市 天津市 南开区 大悦城3楼','18622238259','顺丰快递','到付',0.00,'2026-03-12 17:27:17','2026-03-12 17:46:46','2026-03-12 17:50:29',NULL,NULL,0,0,NULL),(14,'ORD20260316175558172024',71,20.00,3,'','2026-03-16 17:55:59','2026-03-16 17:56:13','','18622238259','顺丰快递','到付',0.00,'2026-03-16 17:55:59','2026-03-16 17:56:07','2026-03-16 17:56:13',NULL,NULL,0,0,NULL),(15,'ORD20260316181413527136',62,30.00,1,'','2026-03-16 18:14:13','2026-03-16 18:14:13','','','顺丰快递','到付',0.00,'2026-03-16 18:14:13',NULL,NULL,NULL,NULL,0,0,NULL),(16,'ORD20260316181426874742',56,10.00,1,'','2026-03-16 18:14:27','2026-03-16 18:14:27','','','顺丰快递','到付',0.00,'2026-03-16 18:14:27',NULL,NULL,NULL,NULL,0,0,NULL),(17,'ORD20260316181431500953',54,66.00,1,'','2026-03-16 18:14:32','2026-03-16 18:14:32','','','顺丰快递','到付',0.00,'2026-03-16 18:14:32',NULL,NULL,NULL,NULL,0,0,NULL),(18,'ORD20260316181437222969',72,30.00,1,'','2026-03-16 18:14:37','2026-03-16 18:14:37','','','顺丰快递','到付',0.00,'2026-03-16 18:14:37',NULL,NULL,NULL,NULL,0,0,NULL),(19,'ORD20260316181443971388',61,10.00,1,'','2026-03-16 18:14:44','2026-03-16 18:14:44','','','顺丰快递','到付',0.00,'2026-03-16 18:14:44',NULL,NULL,NULL,NULL,0,0,NULL),(20,'ORD20260316183156530529',73,20.00,1,'','2026-03-16 18:31:57','2026-03-16 18:32:04','','','顺丰快递','到付',0.00,'2026-03-16 18:31:57',NULL,NULL,NULL,NULL,0,1,'2026-03-16 18:32:04');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_categories`
--

DROP TABLE IF EXISTS `product_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_categories` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `category_name` varchar(100) NOT NULL COMMENT '分类名称',
  `group_id` int DEFAULT '0' COMMENT '所属分类组',
  `parent_id` int DEFAULT '0' COMMENT '父分类ID，0为顶级分类',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1=正常, 0=停用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_default` tinyint DEFAULT '0' COMMENT '是否为默认分类: 1=是, 0=否',
  `color` varchar(50) DEFAULT '' COMMENT '颜色',
  PRIMARY KEY (`id`),
  KEY `idx_parent` (`parent_id`),
  KEY `idx_status` (`status`),
  KEY `idx_group` (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产品分类表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_categories`
--

LOCK TABLES `product_categories` WRITE;
/*!40000 ALTER TABLE `product_categories` DISABLE KEYS */;
INSERT INTO `product_categories` VALUES (2,'北京同庆',1,0,0,1,'2026-03-03 13:37:38','2026-03-04 11:04:12',1,''),(3,'常规',2,0,0,1,'2026-03-03 13:38:22','2026-03-10 11:19:13',0,''),(4,'自定义',2,0,0,1,'2026-03-03 13:38:30','2026-03-10 11:19:01',0,'');
/*!40000 ALTER TABLE `product_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_category_values`
--

DROP TABLE IF EXISTS `product_category_values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_category_values` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL COMMENT '产品ID',
  `group_id` int NOT NULL COMMENT '分类组ID',
  `category_id` int DEFAULT NULL COMMENT '分类ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_product` (`product_id`),
  KEY `idx_group` (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category_values`
--

LOCK TABLES `product_category_values` WRITE;
/*!40000 ALTER TABLE `product_category_values` DISABLE KEYS */;
INSERT INTO `product_category_values` VALUES (1,2,1,2,'2026-03-03 13:39:12'),(2,2,2,3,'2026-03-03 13:39:12'),(3,3,1,2,'2026-03-03 13:41:09'),(4,3,2,3,'2026-03-03 13:41:09'),(5,4,1,NULL,'2026-03-06 16:02:50'),(6,4,2,4,'2026-03-06 16:02:50'),(7,5,1,NULL,'2026-03-16 17:57:03'),(8,5,2,NULL,'2026-03-16 17:57:03');
/*!40000 ALTER TABLE `product_category_values` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `product_name` varchar(100) NOT NULL COMMENT '产品名称',
  `product_name_pinyin` varchar(255) DEFAULT NULL COMMENT '产品名称拼音',
  `product_name_initial` varchar(50) DEFAULT NULL COMMENT '产品名称拼音首字母',
  `category_id` int DEFAULT NULL COMMENT '分类ID',
  `width` decimal(10,2) DEFAULT '0.00' COMMENT '宽度',
  `height` decimal(10,2) DEFAULT '0.00' COMMENT '高度',
  `price` decimal(10,2) DEFAULT '0.00' COMMENT '价格',
  `stock` int DEFAULT '0' COMMENT '库存',
  `unit` varchar(20) DEFAULT '' COMMENT '单位',
  `barcode` varchar(50) DEFAULT '' COMMENT '条码',
  `description` text COMMENT '产品描述',
  `sales_status` tinyint DEFAULT '1' COMMENT '销售状态: 1=在售, 0=停售',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1=正常, 0=停用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` text COMMENT '备注',
  `free_shipping` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_barcode` (`barcode`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产品信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (2,'[PVC吧台贴]马年氛围','[PVCbataitie]manianfenwei','[PVCbtt]mnfw',NULL,20.00,30.00,10.00,0,'个','','',1,1,'2026-03-03 13:39:12','2026-03-06 17:19:30','',0),(3,'[6090KT板]马年气氛','[6090KTban]manianqifen','[6090KTb]mnqf',NULL,60.00,70.00,22.00,0,'个','','',1,1,'2026-03-03 13:41:09','2026-03-06 17:26:13','',0),(4,'测试','ceshi','cs',NULL,0.00,0.00,10.00,0,'个','','',1,1,'2026-03-06 16:02:50','2026-03-06 17:26:16','',1),(5,'地方是短发','difangshiduanfa','dfsdf',NULL,0.00,0.00,0.00,0,'','','',0,1,'2026-03-16 17:57:03','2026-03-16 17:57:03','',0);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL COMMENT '角色名称',
  `permissions` text COMMENT '权限JSON',
  `status` int DEFAULT NULL COMMENT '状态: 1=启用, 0=禁用',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `is_super_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'超级管理员','[\"stats_view\"]',1,'2026-03-11 11:00:23',1),(2,'管理员','[\"login\", \"shop_view\", \"order_view\", \"product_view\", \"stats_view\"]',1,'2026-03-11 11:31:35',0);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shops`
--

DROP TABLE IF EXISTS `shops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shops` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '店铺ID',
  `shop_name` varchar(100) NOT NULL COMMENT '店铺名称',
  `shop_name_pinyin` varchar(255) DEFAULT NULL COMMENT '店铺名称拼音',
  `shop_name_initial` varchar(50) DEFAULT NULL COMMENT '店铺名称拼音首字母',
  `business_model` varchar(50) DEFAULT NULL COMMENT '经营模式',
  `phone` varchar(20) DEFAULT NULL COMMENT '电话',
  `address` varchar(255) DEFAULT NULL COMMENT '详细地址',
  `region` varchar(20) DEFAULT NULL COMMENT '大区',
  `province` varchar(50) DEFAULT NULL COMMENT '省份',
  `city` varchar(50) DEFAULT NULL COMMENT '市/县',
  `district` varchar(50) DEFAULT NULL COMMENT '区',
  `address_pinyin` varchar(255) DEFAULT NULL COMMENT '地址拼音',
  `address_initial` varchar(50) DEFAULT NULL COMMENT '地址拼音首字母',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1=正常, 0=停用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` text COMMENT '备注',
  `free_shipping` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='店铺管理表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shops`
--

LOCK TABLES `shops` WRITE;
/*!40000 ALTER TABLE `shops` DISABLE KEYS */;
INSERT INTO `shops` VALUES (1,'测试店铺','ceshidianpu','csdp','直营','13800138000','','','','','','','',0,'2026-03-03 11:26:26','2026-03-10 10:44:35','',0),(2,'南开大悦城店','nankaidayuechengdian','nkdycd','','','',NULL,NULL,NULL,NULL,NULL,NULL,1,'2026-03-03 11:26:34','2026-03-03 11:51:36','',0),(3,'南开大悦城店2','nankaidayuechengdian2','nkdycd2','直营','18622238259','南岸家园','华南','天津市','天津市','南开区','huanantianjinshitianjinshinankaiqunananjiayuan','hntjstjsnkqnajy',1,'2026-03-03 11:32:15','2026-03-03 11:57:19','',0),(4,'事实上','shishishang','sss','直营店','','南开大悦城 2楼','','','华北 天津市',' 天津 市','huabei tianjinshi tianjin shinankaidayuecheng 2lou','hb tjs tj snkdyc 2l',1,'2026-03-03 11:38:42','2026-03-03 11:57:19','',0),(5,'和平大悦城店','hepingdayuechengdian','hpdycd','加盟店','18622238259','和平大悦城6楼','华北','天津市','天津','市 和平区','huabeitianjinshitianjinshi hepingquhepingdayuecheng6lou','hbtjstjs hpqhpdyc6l',1,'2026-03-03 11:54:44','2026-03-03 11:57:19','',0),(6,'海底捞火锅店','haidilaohuoguodian','hdlhgd','直营店','13800001111','天河路100号','','广东省','广州市','天河区','guangdongshengguangzhoushitianhequtianhelu100hao','gdsgzsthqthl100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺1',0),(7,'星巴克咖啡','xingbakekafei','xbkkf','加盟店','13800002222','南京西路200号','华东','上海市','上海','市静安区','huadongshanghaishishanghaishijinganqunanjingxilu200hao','hdshsshsjaqnjxl200h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺2',0),(8,'京东便利店','jingdongbianlidian','jdbld','直营店','13800003333','建国路88号','华北','北京市','北京','市朝阳区','huabeibeijingshibeijingshichaoyangqujianguolu88hao','hbbjsbjscyqjgl88h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺3',0),(9,'小米之家','xiaomizhijia','xmzj','加盟店','13800004444','科技园路50号','','','深圳市','南山区','shenzhenshinanshanqukejiyuanlu50hao','szsnsqkjyl50h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺4',0),(10,'优衣库','youyiku','yyk','直营店','13800005555','延安路150号','','','杭州市','西湖区','hangzhoushixihuquyananlu150hao','hzsxhqyal150h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺5',0),(11,'屈臣氏','quchenshi','qcs','加盟店','13800006666','春熙路300号','','','成都市','锦江区','chengdushijinjiangquchunxilu300hao','cdsjjqcxl300h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺6',0),(12,'周黑鸭','zhouheiya','zhy','直营店','13800007777','江汉路88号','','','武汉市','江汉区','wuhanshijianghanqujianghanlu88hao','whsjhqjhl88h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺7',0),(13,'绝味鸭脖','jueweiyabo','jwyb','加盟店','13800008888','麓山南路120号','','','长沙市','岳麓区','changshashiyueluqulushannanlu120hao','cssylqlsnl120h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺8',0),(14,'正新鸡排','zhengxinjipai','zxjp','直营店','13800009999','夫子庙200号','','','南京市','秦淮区','nanjingshiqinhuaiqufuzimiao200hao','njsqhqfzm200h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺9',0),(15,'蜜雪冰城','mixuebingcheng','mxbc','加盟店','13800001010','解放碑150号','西南','重庆市','重庆','市渝中区','xinanchongqingshichongqingshiyuzhongqujiefangbei150hao','xncqscqsyzqjfb150h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺10',0),(16,'瑞幸咖啡','ruixingkafei','rxkf','直营店','13800001111','北京路250号','','','广州市','越秀区','guangzhoushiyuexiuqubeijinglu250hao','gzsyxqbjl250h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺11',0),(17,'奈雪的茶','naixuedecha','nxdc','加盟店','13800001212','华强北100号','','','深圳市','福田区','shenzhenshifutianquhuaqiangbei100hao','szsftqhqb100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺12',0),(18,'喜茶','xicha','xc','直营店','13800001313','淮海路180号','华东','上海市','上海','市徐汇区','huadongshanghaishishanghaishixuhuiquhuaihailu180hao','hdshsshsxhqhhl180h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺13',0),(19,'茶颜悦色','chayanyuese','cyys','加盟店','13800001414','太平街80号','','','长沙市','天心区','changshashitianxinqutaipingjie80hao','csstxqtpj80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺14',0),(20,'古茗茶饮','gumingchayin','gmcy','直营店','13800001515','江南大道300号','','','杭州市','滨江区','hangzhoushibinjiangqujiangnandadao300hao','hzsbjqjndd300h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺15',0),(21,'书亦烧仙草','shuyishaoxiancao','sysxc','加盟店','13800001616','天府大道200号','','','成都市','高新区','chengdushigaoxinqutianfudadao200hao','cdsgxqtfdd200h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺16',0),(22,'益禾堂','yihetang','yht','直营店','13800001717','光谷步行街150号','','','武汉市','洪山区','wuhanshihongshanquguanggubuxingjie150hao','whshsqggbxj150h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺17',0),(23,'CoCo都可','CoCodouke','CoCodk','加盟店','13800001818','中山路100号','','','南京市','鼓楼区','nanjingshigulouquzhongshanlu100hao','njsglqzsl100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺18',0),(24,'一点点','yidiandian','ydd','直营店','13800001919','小寨路120号','','','西安市','雁塔区','xianshiyantaquxiaozhailu120hao','xasytqxzl120h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺19',0),(25,'乐乐茶','lelecha','llc','加盟店','13800002020','观音桥180号','西南','重庆市','重庆','市江北区','xinanchongqingshichongqingshijiangbeiquguanyinqiao180hao','xncqscqsjbqgyq180h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺20',0),(26,'德克士','dekeshi','dks','直营店','13800002121','琶洲大道80号','','','广州市','海珠区','guangzhoushihaizhuqupazhoudadao80hao','gzshzqpzdd80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺21',0),(27,'华莱士','hualaishi','hls','加盟店','13800002222','五一路60号','','','福州市','鼓楼区','fuzhoushigulouquwuyilu60hao','fzsglqwyl60h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺22',0),(28,'正新鸡排','zhengxinjipai','zxjp','直营店','13800002323','中山路200号','','','厦门市','思明区','xiamenshisimingquzhongshanlu200hao','xmssmqzsl200h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺23',0),(29,'叫了只炸鸡','jiaolezhizhaji','jlzzj','加盟店','13800002424','香港中路100号','','','青岛市','市南区','qingdaoshishinanquxianggangzhonglu100hao','qdssnqxgzl100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺24',0),(30,'叫了个炸鸡','jiaolegezhaji','jlgzj','直营店','13800002525','人民路80号','','','大连市','中山区','dalianshizhongshanqurenminlu80hao','dlszsqrml80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺25',0),(31,'麦当劳','maidanglao','mdl','加盟店','13800002626','南京路150号','华北','天津市','天津','市和平区','huabeitianjinshitianjinshihepingqunanjinglu150hao','hbtjstjshpqnjl150h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺26',0),(32,'肯德基','kendeji','kdj','直营店','13800002727','中央大街120号','','','哈尔滨市','南岗区','haerbinshinangangquzhongyangdajie120hao','hebsngqzydj120h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺27',0),(33,'汉堡王','hanbaowang','hbw','加盟店','13800002828','太原街80号','','','沈阳市','和平区','shenyangshihepingqutaiyuanjie80hao','syshpqtyj80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺28',0),(34,'赛百味','saibaiwei','sbw','直营店','13800002929','重庆路100号','','','长春市','朝阳区','changchunshichaoyangquchongqinglu100hao','ccscyqcql100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺29',0),(35,'必胜客','bishengke','bsk','加盟店','13800003030','观前街60号','','','苏州市','姑苏区','suzhoushigusuquguanqianjie60hao','szsgsqgqj60h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺30',0),(36,'达美乐','dameile','dml','直营店','13800003131','太湖大道120号','','','无锡市','滨湖区','wuxishibinhuqutaihudadao120hao','wxsbhqthdd120h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺31',0),(37,'棒约翰','bangyuehan','byh','加盟店','13800003232','天一广场80号','','','宁波市','海曙区','ningboshihaishuqutianyiguangchang80hao','nbshsqtygc80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺32',0),(38,'尊宝披萨','zunbaopisa','zbps','直营店','13800003333','五马街100号','','','温州市','鹿城区','wenzhoushiluchengquwumajie100hao','wzslcqwmj100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺33',0),(39,'现捞','xianlao','xl','加盟店','13800003434','祖庙路60号','','','佛山市','禅城区','foshanshichanchengquzumiaolu60hao','fssccqzml60h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺34',0),(40,'久久鸭','jiujiuya','jjy','直营店','13800003535','鸿福路80号','','','东莞市','南城区','dongguanshinanchengquhongfulu80hao','dgsncqhfl80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺35',0),(41,'绝味','juewei','jw','加盟店','13800003636','中山路100号','','','中山市','东区','zhongshanshidongquzhongshanlu100hao','zssdqzsl100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺36',0),(42,'周黑鸭','zhouheiya','zhy','直营店','13800003737','吉大路60号','','','珠海市','香洲区','zhuhaishixiangzhouqujidalu60hao','zhsxzqjdl60h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺37',0),(43,'煌上煌','huangshanghuang','hsh','加盟店','13800003838','建设路80号','','','江门市','蓬江区','jiangmenshipengjiangqujianshelu80hao','jmspjqjsl80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺38',0),(44,'紫燕百味鸡','ziyanbaiweiji','zybwj','直营店','13800003939','麦地路100号','','','惠州市','惠城区','huizhoushihuichengqumaidilu100hao','hzshcqmdl100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺39',0),(45,'久久丫','jiujiuya','jjy','加盟店','13800004040','朝阳大街120号','','','保定市','竞秀区','baodingshijingxiuquzhaoyangdajie120hao','bdsjxqzydj120h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺40',0),(46,'留夫鸭','liufuya','lfy','直营店','13800004141','共青团路80号','','','淄博市','张店区','ziboshizhangdianqugongqingtuanlu80hao','zbszdqgqtl80h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺41',0),(47,'鼎香坊','dingxiangfang','dxf','加盟店','13800004242','南大街100号','','','烟台市','芝罘区','yantaishizhifuqunandajie100hao','ytszfqndj100h',1,'2026-03-03 12:30:44','2026-03-03 12:30:44','测试店铺42',0),(48,'老枝花卤','laozhihualu','lzhl','直营店','13800004343','胜利街60号','华东','山东省','潍坊市','奎文区','huadongshandongshengweifangshikuiwenqushenglijie60hao','hdsdswfskwqslj60h',1,'2026-03-03 12:30:44','2026-03-12 16:22:02','测试店铺43',0),(49,'辣友记方法','layoujifangfa','lyjff','加盟店','13800004444','解放路80号','华东','浙江省','绍兴市','越城区','huadongzhejiangshengshaoxingshiyuechengqujiefanglu80hao','hdzjssxsycqjfl80h',1,'2026-03-03 12:30:44','2026-03-12 16:21:55','测试店铺44',0),(50,'卤人甲uu','lurenjiauu','lrjuu','直营店','13800004545','衣裳街100号','华东','浙江省','湖州市','吴兴区','huadongzhejiangshenghuzhoushiwuxingquyishangjie100hao','hdzjshzswxqysj100h',1,'2026-03-03 12:30:44','2026-03-12 16:15:03','测试店铺45',0),(51,'卤萌主j','lumengzhuj','lmzj','加盟店','13800004646','中山西路60号','华东','浙江省','台州市','椒江区','huadongzhejiangshengtaizhoushijiaojiangquzhongshanxilu60hao','hdzjstzsjjqzsxl60h',1,'2026-03-03 12:30:44','2026-03-12 16:14:49','测试店铺46',0),(52,'有间卤铺','youjianlupu','yjlp','直营店','13800004747','八一北街80号','华东','浙江省','金华市','婺城区','huadongzhejiangshengjinhuashiwuchengqubayibeijie80hao','hdzjsjhswcqbybj80h',1,'2026-03-03 12:30:44','2026-03-12 16:14:35','测试店铺47',0),(53,'卤当当p','ludangdangp','lddp','加盟店','13800004848','上街100号','华东','浙江省','衢州市','柯城区','huadongzhejiangshengquzhoushikechengqushangjie100hao','hdzjsqzskcqsj100h',1,'2026-03-03 12:30:44','2026-03-12 16:14:28','测试店铺48',0),(54,'小鲜卤','xiaoxianlu','xxl','加盟店','13800004949','中山街120号','华东','浙江省','','','huadongzhejiangshengzhongshanjie120hao','hdzjszsj120h',1,'2026-03-03 12:30:44','2026-03-04 12:05:42','测试店铺49',0),(55,'卤小二票','luxiaoerpiao','lxep','办公地点','13800005050','人民南路80号','华东','浙江省','舟山市','定海区','huadongzhejiangshengzhoushanshidinghaiqurenminnanlu80hao','hdzjszssdhqrmnl80h',1,'2026-03-03 12:30:44','2026-03-10 11:12:32','测试店铺50',0),(56,'南开大悦城店4','nankaidayuechengdian4','nkdycd4','加盟店','','人民南路80号','','','舟山市',' 定海区','zhoushanshi dinghaiqurenminnanlu80hao','zss dhqrmnl80h',1,'2026-03-03 12:39:46','2026-03-03 12:39:46','',0),(57,'南开大悦城店45','nankaidayuechengdian45','nkdycd45','加盟店','','人民南路80号、','','','舟山市',' 定海区','zhoushanshi dinghaiqurenminnanlu80hao、','zss dhqrmnl80h、',1,'2026-03-03 12:40:18','2026-03-03 12:40:18','',0),(58,'南开大悦城店6','nankaidayuechengdian6','nkdycd6','加盟店','','南开大悦城7楼','华北','天津市','','','huabeitianjinshinankaidayuecheng7lou','hbtjsnkdyc7l',1,'2026-03-03 12:42:32','2026-03-03 12:42:32','',0),(59,'南开大悦城店34','nankaidayuechengdian34','nkdycd34','加盟店','','市 南开大悦城123','华北','天津市','天津','','huabeitianjinshitianjinshi nankaidayuecheng123','hbtjstjs nkdyc123',1,'2026-03-03 12:45:40','2026-03-03 12:45:40','',0),(60,'南开大悦城店啊啊','nankaidayuechengdianaa','nkdycdaa','加盟店','','市 南开大悦城 23楼','华北','天津市','天津','','huabeitianjinshitianjinshi nankaidayuecheng 23lou','hbtjstjs nkdyc 23l',0,'2026-03-03 12:57:31','2026-03-04 13:07:10','',0),(61,'南开大悦城2店','nankaidayuecheng2dian','nkdyc2d','加盟店','','','','','','','','',1,'2026-03-04 17:23:07','2026-03-04 17:23:07','',0),(62,'南开大悦城32店','nankaidayuecheng32dian','nkdyc32d','加盟店','','','','','','','','',1,'2026-03-04 17:33:38','2026-03-04 17:33:38','',0),(63,'南开大悦城21店','nankaidayuecheng21dian','nkdyc21d','加盟店','','大悦城2楼','华北','天津市','天津市','南开区','huabeitianjinshitianjinshinankaiqudayuecheng2lou','hbtjstjsnkqdyc2l',1,'2026-03-04 18:16:17','2026-03-04 18:16:17','',0),(64,'南开大悦城22店','nankaidayuecheng22dian','nkdyc22d','加盟店','18622238259','大悦城3楼','华北','天津市','天津市','南开区','huabeitianjinshitianjinshinankaiqudayuecheng3lou','hbtjstjsnkqdyc3l',1,'2026-03-04 18:16:38','2026-03-05 15:46:36','',0),(65,'南开大悦城店224','nankaidayuechengdian224','nkdycd224','加盟店','333','','','','','','','',0,'2026-03-09 17:58:37','2026-03-09 18:33:44','',0),(67,'事实上2','shishishang2','sss2','加盟店','','','','','','','','',0,'2026-03-09 18:18:04','2026-03-10 18:11:31','',0),(68,'地方发的发','difangfadefa','dffdf','直营店','','大悦城4楼','华北','天津市','天津市','南开区','huabeitianjinshitianjinshinankaiqudayuecheng4lou','hbtjstjsnkqdyc4l',0,'2026-03-09 18:21:30','2026-03-12 13:11:25','',0),(69,'南开大悦城店发的地方','nankaidayuechengdianfadedifang','nkdycdfddf','加盟店','','','','','','','','',0,'2026-03-10 17:03:23','2026-03-11 13:27:18','',0),(70,'dfdsdsdsgsgsd','dfdsdsdsgsgsd','dfdsdsdsgsgsd','加盟店','','','','','','','','',0,'2026-03-12 14:52:07','2026-03-12 14:52:13','',0),(71,'是大扶桑岛国','shidafusangdaoguo','sdfsdg','加盟店','18622238259','','','','','','','',1,'2026-03-16 17:55:30','2026-03-16 17:55:46','',0),(72,'是的发送','shidefasong','sdfs','加盟店','','','','','','','','',1,'2026-03-16 18:03:26','2026-03-16 18:03:26','',0),(73,'sdfsdfsdfdf','sdfsdfsdfdf','sdfsdfsdfdf','加盟店','','',NULL,'','','','','',1,'2026-03-16 18:31:36','2026-03-16 18:31:36','',0);
/*!40000 ALTER TABLE `shops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_config`
--

DROP TABLE IF EXISTS `system_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `config_key` varchar(50) NOT NULL COMMENT '配置键',
  `config_value` text COMMENT '配置值',
  `config_type` varchar(20) DEFAULT NULL COMMENT '类型: text/text/number/image',
  `description` varchar(200) DEFAULT NULL COMMENT '描述',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_key` (`config_key`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_config`
--

LOCK TABLES `system_config` WRITE;
/*!40000 ALTER TABLE `system_config` DISABLE KEYS */;
INSERT INTO `system_config` VALUES (1,'system_name','沪上阿姨产品订购系统','text',NULL,'2026-03-06 16:35:29','2026-03-06 16:35:29'),(2,'logo','/static/uploads/e1aa2880-3114-4e6a-8190-e0e042c32c95.png','image',NULL,'2026-03-06 16:35:29','2026-03-06 16:35:29'),(3,'free_shipping_amount','100','text',NULL,'2026-03-06 17:39:22','2026-03-06 17:39:22');
/*!40000 ALTER TABLE `system_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希',
  `role_id` int DEFAULT NULL COMMENT '角色ID',
  `status` int DEFAULT NULL COMMENT '状态: 1=启用, 0=禁用',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `name` varchar(50) DEFAULT '',
  `role_ids` varchar(255) DEFAULT '',
  `avatar` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (7,'xuzhiming','scrypt:32768:8:1$bDclry74xYnEsjZO$036e8db330d4f9fc0928a4045f3b92ec1973eff567710cf9b742767406c119a51dcb0bf99984098f36b02c3e1829d515bd9956fd53f052a9f6905a52af090ae9',NULL,1,'2026-03-11 17:40:06','徐志铭','1','/static/avatars/3ac53fa0-6f35-4814-ba11-e56deaa533c3.webp'),(8,'zhaoxin','scrypt:32768:8:1$N5o6dVs2zLs7aJ7Z$ac2a3a0fac2f55963367f6adf1e160c779cd570b8e7cc674cb2badc30d07d4731da65bc899be8492ccb9a63d5d2b9be96ce12c1c5c43bf84b77e2db216f6b018',NULL,1,'2026-03-11 17:42:13','赵馨','2',NULL);
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

-- Dump completed on 2026-03-17  1:00:59
