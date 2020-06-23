/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - 063autoqa
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`063autoqa` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `063autoqa`;

/*Table structure for table `userdetails` */

DROP TABLE IF EXISTS `userdetails`;

CREATE TABLE `userdetails` (
  `id` int(11) NOT NULL auto_increment,
  `fullname` varchar(100) default NULL,
  `gender` varchar(10) default NULL,
  `mobile` varchar(15) default NULL,
  `email` varchar(100) default NULL,
  `dob` varchar(15) default NULL,
  `address` varchar(100) default NULL,
  `username` varchar(100) default NULL,
  `password` varchar(100) default NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `userdetails` */

insert  into `userdetails`(`id`,`fullname`,`gender`,`mobile`,`email`,`dob`,`address`,`username`,`password`) values (1,'abc','on','7894561230','abc@gmail.com','2019-11-02',NULL,'a','a');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
