-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: i360
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB

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
-- Table structure for table `i360_commands`
--

DROP TABLE IF EXISTS `i360_commands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_commands` (
  `i360_command_id` int(4) NOT NULL AUTO_INCREMENT,
  `i360_command_name` varchar(30) NOT NULL,
  `i360_command_letter` varchar(3) NOT NULL,
  `i360_command_description` text NOT NULL,
  `i360_command_params` varchar(10) NOT NULL,
  `i360_command_priority` int(3) NOT NULL,
  `i360_command_break` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`i360_command_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='команды отдаваемые на управление системы';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_commands`
--

LOCK TABLES `i360_commands` WRITE;
/*!40000 ALTER TABLE `i360_commands` DISABLE KEYS */;
INSERT INTO `i360_commands` VALUES (1,'makePhoto','MPN','Make Photo\nуказывает с какого фотоаппарата нужно произвести съемку\n\nСтруктура хранения\n\nsource \nid_sequence\nid_camera\nid_photo_EAN13.jpg\n\nВ параметрах передается номер камеры для съемки (1-4)','',0,0),(2,'motor','MN','Управление первым сервомотором\r\n\r\nF - скорость вращения\r\nA - угол поворота\r\n$x - передаточное число для определения числа оборотов из угла поворота\r\n\r\n$y - старт, торможение плавные для фото\r\n\r\n$z - съемка без остановки','',0,0),(3,'speed','FN','Указание скорости исполнительного элемента для передачи в микроконтроллер','',0,0),(4,'angle','AN','указание угла поворота исполнительного элемента\r\n\r\nдалее расчитывается число шагов исходя из передаточного отношения и числа шагов на угол поворота шагового двигателя','',0,0),(5,'settingsRatio','SXN','Передаточное отношение первого привода\r\nопределяет число шагов в зависимости от угла поворота','',0,0),(6,'stop','G0','Останов системы','',0,0),(7,'init','STR','Start system - подключение по компортам, инициализация системы\r\n\r\nУточнить по GCode','',0,0),(8,'defaultCamera','DC','Default Camera Settings\r\nif make photo without params\r\n','',0,0),(9,'defaultMotor','DM','if angle or speed command without motor number\r\n','',0,0),(10,'onHoldTime','HLD','Сколько времени без команд система поддерживает соединение с объектами (фотоаппараты и плата управления моторами)','',0,0),(11,'makeHDR','HDR','Съемка с камеры в трех состояниях для получения HDR картинки (jpg after)','',0,0),(12,'pause','PSE','При появлении в очереди - тормозит следующий ход до команды STR','',0,0),(13,'reset','RST','Сбрасывает к нулевым значениям входные данные по задаче.','',0,0);
/*!40000 ALTER TABLE `i360_commands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_description`
--

DROP TABLE IF EXISTS `i360_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_description` (
  `i360_description_id` int(11) NOT NULL AUTO_INCREMENT,
  `i360_table` varchar(40) NOT NULL,
  `i360_field` varchar(40) NOT NULL,
  `i360_value` varchar(100) NOT NULL,
  `i360_description` text NOT NULL,
  PRIMARY KEY (`i360_description_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='Описание поля определенной таблицы';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_description`
--

LOCK TABLES `i360_description` WRITE;
/*!40000 ALTER TABLE `i360_description` DISABLE KEYS */;
INSERT INTO `i360_description` VALUES (1,'i360_objects_features','i360_object_key','Светосила','Соотношение между входным световым потоком в объектив камеры и выходным потоком на матрицу камеры'),(2,'i360_object','i360_object_type','camera','Камера, которой проводится съемка\r\nВ состав камеры входит и установленный объектив, если объектив меняется - это другая камера.\r\n\r\nВ одной съемке может участвовать несколько камер.\r\n\r\nЕсли число используемых камер меняется - это другая сцена. '),(3,'i360_objects','i360_object_type','scene','Сцена - совокупность установленных камер и стола, возможно что несколько камер на сцену, тогда есть камера по умолчанию и настройки второй камеры');
/*!40000 ALTER TABLE `i360_description` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_filters`
--

DROP TABLE IF EXISTS `i360_filters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_filters` (
  `i360_filter_id` int(5) NOT NULL AUTO_INCREMENT,
  `i360_filter_description` text NOT NULL,
  `i360_filter_title` varchar(50) NOT NULL COMMENT 'заголовок',
  `i360_filter_settings` text NOT NULL COMMENT 'настройки, тип, макс, мин',
  `i360_filter_bin` varchar(150) NOT NULL,
  PRIMARY KEY (`i360_filter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='фильтры в системе';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_filters`
--

LOCK TABLES `i360_filters` WRITE;
/*!40000 ALTER TABLE `i360_filters` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_filters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_filters_presets`
--

DROP TABLE IF EXISTS `i360_filters_presets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_filters_presets` (
  `i360_filter_preset_id` int(11) NOT NULL AUTO_INCREMENT,
  `i360_filter_id` int(11) NOT NULL,
  `i360_filter_preset_name` varchar(100) NOT NULL,
  `i360_filter_preset_settings` text NOT NULL,
  PRIMARY KEY (`i360_filter_preset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Пресеты по настройкам филтров';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_filters_presets`
--

LOCK TABLES `i360_filters_presets` WRITE;
/*!40000 ALTER TABLE `i360_filters_presets` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_filters_presets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_filters_roadmap`
--

DROP TABLE IF EXISTS `i360_filters_roadmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_filters_roadmap` (
  `i360_filter_roadmap_id` int(11) NOT NULL AUTO_INCREMENT,
  `i360_filter_roadmap_name` varchar(100) NOT NULL,
  `i360_filter_roadmap_create_on` datetime NOT NULL,
  `i360_filter_roadmap_active` tinyint(1) NOT NULL DEFAULT '1',
  `i360_filter_roadmap_modified_at` datetime NOT NULL,
  PRIMARY KEY (`i360_filter_roadmap_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Порядок обработки изображения';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_filters_roadmap`
--

LOCK TABLES `i360_filters_roadmap` WRITE;
/*!40000 ALTER TABLE `i360_filters_roadmap` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_filters_roadmap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_filters_roadmaps_lists`
--

DROP TABLE IF EXISTS `i360_filters_roadmaps_lists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_filters_roadmaps_lists` (
  `i360_filter_roadmap_list_id` int(11) NOT NULL AUTO_INCREMENT,
  `i360_filter_roadmap_id` int(11) NOT NULL,
  `i360_filter_id` int(11) NOT NULL,
  `i360_filter_settings` text NOT NULL COMMENT 'настройки фильтра выбранные в программном интерфейсе',
  `i360_filter_line` int(11) NOT NULL COMMENT 'порядковый номер выполнения фильтра (от предыдущего источник, следующему результат',
  PRIMARY KEY (`i360_filter_roadmap_list_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Последовательность применения фильтров к результату';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_filters_roadmaps_lists`
--

LOCK TABLES `i360_filters_roadmaps_lists` WRITE;
/*!40000 ALTER TABLE `i360_filters_roadmaps_lists` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_filters_roadmaps_lists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_image_sizes`
--

DROP TABLE IF EXISTS `i360_image_sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_image_sizes` (
  `i360_image_size_id` int(3) NOT NULL AUTO_INCREMENT,
  `i360_image_width` int(5) NOT NULL,
  `i360_image_height` int(5) NOT NULL,
  `i360_image_active` tinyint(1) NOT NULL DEFAULT '1',
  `i360_image_description` varchar(155) NOT NULL,
  `i360_image_preview` int(1) NOT NULL,
  `i360_image_filename` varchar(100) NOT NULL COMMENT 'структура формирования имени',
  `i360_result_uploadpath` varchar(100) NOT NULL COMMENT 'путь до загрузки',
  `i360_image_path` varchar(100) NOT NULL COMMENT 'куда сохранять',
  `i360_image_library_path` varchar(100) NOT NULL,
  `i360_result_path` varchar(100) NOT NULL,
  `i360_filter_path` varchar(100) NOT NULL,
  `i360_result_filename` varchar(100) NOT NULL,
  `i360_image_source` int(1) NOT NULL DEFAULT '0' COMMENT 'является ли источником',
  PRIMARY KEY (`i360_image_size_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='размеры изображений на которые готовить превью и результат';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_image_sizes`
--

LOCK TABLES `i360_image_sizes` WRITE;
/*!40000 ALTER TABLE `i360_image_sizes` DISABLE KEYS */;
INSERT INTO `i360_image_sizes` VALUES (1,438,584,1,'NoteBook product card',0,'notebook_[photo_id].jpg','','[APP]/img/[Date]/[issue_id]','0','[APP]/result/[Date]','','[EAN13].notebook.360.jpg',0),(2,150,300,1,'small preview in action',2,'tb_[photo_id].jpg','','[APP]/img/[Date]/[issue_id]','0','','','',0),(3,400,600,1,'main preview in action',1,'preview_[photo_id].jpg','','[APP]/img/[Date]/[issue_id]','0','','','',0),(4,2400,3200,1,'Исходное изображение (максимальный и минимальный размер)',0,'source_[photo_id].jpg','','[APP]/img/[Date]/[issue_id]','[LIB]/img/[Date]/[issue_id]','','','',1);
/*!40000 ALTER TABLE `i360_image_sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_issues`
--

DROP TABLE IF EXISTS `i360_issues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_issues` (
  `i360_issue_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'номер действия в истории',
  `i360_location_name` varchar(40) NOT NULL COMMENT 'относительно чего работа (снимаем фон, продукт, тест)',
  `i360_issue_action` enum('PHOTO','MOVE') NOT NULL DEFAULT 'PHOTO' COMMENT 'photo, move',
  `i360_issue_created_on` datetime NOT NULL,
  `i360_issue_started_at` datetime NOT NULL COMMENT 'Когда начал работать сервис',
  `i360_issue_started` int(1) NOT NULL,
  `i360_issue_finished_at` datetime NOT NULL,
  `i360_issue_finished` int(1) NOT NULL,
  `i360_issue_options` text NOT NULL COMMENT 'настройки съемки',
  PRIMARY KEY (`i360_issue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='съемка последовательности кадров по товару';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_issues`
--

LOCK TABLES `i360_issues` WRITE;
/*!40000 ALTER TABLE `i360_issues` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_issues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_objects`
--

DROP TABLE IF EXISTS `i360_objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_objects` (
  `i360_object_id` int(11) NOT NULL AUTO_INCREMENT,
  `i360_object_name` varchar(40) NOT NULL,
  `i360_object_type` varchar(25) NOT NULL,
  `i360_object_descripton` text NOT NULL,
  PRIMARY KEY (`i360_object_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='Таблица предустановок';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_objects`
--

LOCK TABLES `i360_objects` WRITE;
/*!40000 ALTER TABLE `i360_objects` DISABLE KEYS */;
INSERT INTO `i360_objects` VALUES (1,'Canon D30 (50mm 1.2)','camera','Первая камера 50х1.2'),(2,'Белый фон, сумка средняя на 50мм','scene','Постановка сцены - белый фон съемка сумки на 50мм'),(3,'Белый столик из икеи','table','Версия столика от ноября 2019 года, с поворотным столиком из Икеи.');
/*!40000 ALTER TABLE `i360_objects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_objects_features`
--

DROP TABLE IF EXISTS `i360_objects_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_objects_features` (
  `i360_object_features_id` int(11) NOT NULL AUTO_INCREMENT,
  `i360_object_id` int(11) NOT NULL,
  `i360_object_key` varchar(25) NOT NULL,
  `i360_object_value` varchar(100) NOT NULL,
  PRIMARY KEY (`i360_object_features_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_objects_features`
--

LOCK TABLES `i360_objects_features` WRITE;
/*!40000 ALTER TABLE `i360_objects_features` DISABLE KEYS */;
INSERT INTO `i360_objects_features` VALUES (1,1,'Светосила','1.2'),(2,2,'Фокусное расстояние','50'),(3,2,'Расстояние до объекта (м)','3'),(4,3,'Передаточное число','1600'),(5,2,'Рекомендованная диафрагма','8'),(6,3,'Диаметр стола (мм)','400'),(7,3,'Высота стола (см)','75'),(8,2,'Тип замера экспозиции','По центральной точке'),(9,1,'created_on','2019-11-16 10:00:00'),(10,3,'created_on','2019-11-16 10:00:00'),(11,1,'usb_port','/dev/USB001'),(12,3,'usb_port','/deb/USB2');
/*!40000 ALTER TABLE `i360_objects_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_photos`
--

DROP TABLE IF EXISTS `i360_photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_photos` (
  `i360_photo_id` int(11) NOT NULL AUTO_INCREMENT,
  `i360_photo_created_at` int(11) NOT NULL,
  `i360_camera_id` int(11) NOT NULL,
  `i360_id` int(11) NOT NULL,
  `i360_hdr_group` int(11) NOT NULL COMMENT 'Если съемка для hdr',
  PRIMARY KEY (`i360_photo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='фотографии по последовательности';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_photos`
--

LOCK TABLES `i360_photos` WRITE;
/*!40000 ALTER TABLE `i360_photos` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_photos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_products`
--

DROP TABLE IF EXISTS `i360_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_products` (
  `i360_product_id` int(11) NOT NULL,
  `i360_product_EAN13` varchar(13) NOT NULL,
  `i360_product_reference` varchar(155) NOT NULL,
  `i360_product_description` text NOT NULL,
  `i360_product_options` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='библиотека продукта для съемки';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_products`
--

LOCK TABLES `i360_products` WRITE;
/*!40000 ALTER TABLE `i360_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_results`
--

DROP TABLE IF EXISTS `i360_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_results` (
  `i360_result` int(11) NOT NULL AUTO_INCREMENT COMMENT 'номер результата обработки',
  `i360_filters` text NOT NULL COMMENT 'примененные фильтры',
  `i360_camera_id` int(3) NOT NULL COMMENT 'номер камеры',
  `i360_id` int(11) NOT NULL COMMENT 'номер последовательности',
  `i360_image_size_id` int(3) NOT NULL COMMENT 'размер превью',
  `i360_result_created_on` datetime NOT NULL COMMENT 'начало обработки',
  `i360_result_finished_on` datetime NOT NULL COMMENT 'конец обработки',
  `i360_filename` text NOT NULL COMMENT 'конструктор имени файла',
  `i360_result_upload_path` varchar(100) NOT NULL COMMENT 'путь загрузки',
  PRIMARY KEY (`i360_result`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='результат с примененными фильтрами';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_results`
--

LOCK TABLES `i360_results` WRITE;
/*!40000 ALTER TABLE `i360_results` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_roadmap`
--

DROP TABLE IF EXISTS `i360_roadmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_roadmap` (
  `i360_roadmap_id` int(6) NOT NULL AUTO_INCREMENT,
  `i360_roadmap_command` varchar(15) NOT NULL COMMENT 'комманда к исполнению',
  `i360_roadmap_created_at` datetime NULL,
  `i360_roadmap_started_at` datetime NOT NULL COMMENT 'время запуска',
  `i360_roadmap_started` int(1) NOT NULL DEFAULT '0',
  `i360_roadmap_finished_at` datetime DEFAULT NULL COMMENT 'время окончания',
  `i360_roadmap_finished` int(1) NOT NULL DEFAULT '0',
  `i360_roadmap_options` varchar(155) NOT NULL COMMENT 'то что отправлено в параметрах команды',
  `i360_roadmap_updated_at` datetime NOT NULL COMMENT 'время обновления при многошаговом исполнении',
  `i360_roadmap_last_message` varchar(100) DEFAULT NULL,
  `i360_roadmap_progress` int(3) NOT NULL DEFAULT '0' COMMENT 'текущий прогресс выполнения',
  `i360_roadmap_workplace` varchar(20) NOT NULL COMMENT 'наименование рабочего места для старта задания',
  PRIMARY KEY (`i360_roadmap_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='оперативный план';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_roadmap`
--

LOCK TABLES `i360_roadmap` WRITE;
/*!40000 ALTER TABLE `i360_roadmap` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_roadmap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_tags`
--

DROP TABLE IF EXISTS `i360_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_tags` (
  `i360_tag_id` int(4) NOT NULL AUTO_INCREMENT,
  `i360_tag_name` varchar(11) NOT NULL,
  `i360_tag_color` varchar(155) NOT NULL,
  PRIMARY KEY (`i360_tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_tags`
--

LOCK TABLES `i360_tags` WRITE;
/*!40000 ALTER TABLE `i360_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `i360_tags_links`
--

DROP TABLE IF EXISTS `i360_tags_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `i360_tags_links` (
  `i360_tag_link_id` int(6) NOT NULL,
  `i360_tag_direction` varchar(10) NOT NULL,
  `i360_tag_direction_id` int(6) NOT NULL,
  `i360_tag_id` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Связка тегов и различных объектов';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `i360_tags_links`
--

LOCK TABLES `i360_tags_links` WRITE;
/*!40000 ALTER TABLE `i360_tags_links` DISABLE KEYS */;
/*!40000 ALTER TABLE `i360_tags_links` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-24  0:02:15
