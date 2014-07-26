# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.29)
# Database: battlehack
# Generation Time: 2014-07-26 08:58:45 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table listings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `listings`;

CREATE TABLE `listings` (
  `listing_id` int(10) NOT NULL AUTO_INCREMENT,
  `listing_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `user_id` int(10) DEFAULT NULL,
  `title` varchar(140) DEFAULT NULL,
  `image_url` text,
  `thumbnail_url` text,
  `description` text,
  `price` float DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`listing_id`),
  KEY `user_id` (`user_id`),
  KEY `lat` (`lat`),
  KEY `lon` (`lon`),
  KEY `status` (`lon`),
  KEY `listing_time` (`listing_time`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `listings` WRITE;
/*!40000 ALTER TABLE `listings` DISABLE KEYS */;

INSERT INTO `listings` (`listing_id`, `listing_time`, `lat`, `lon`, `user_id`, `title`, `image_url`, `thumbnail_url`, `description`, `price`, `status`)
VALUES
	(4,'2014-07-26 18:56:43',-33.8776,151.216,1,'Test Listing','https://fbcdn-sphotos-f-a.akamaihd.net/hphotos-ak-xpa1/t31.0-8/10496057_10152517550304916_9169413106805908160_o.jpg','http://127.0.0.1:5000/img/lol_thumb.png','A cool product i dont need anymore',1099,'OPEN');

/*!40000 ALTER TABLE `listings` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table transactions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `transactions`;

CREATE TABLE `transactions` (
  `transaction_id` int(10) NOT NULL AUTO_INCREMENT,
  `transaction_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `listing_id` int(10) DEFAULT NULL,
  `user_id` int(10) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int(10) NOT NULL,
  `registration_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
