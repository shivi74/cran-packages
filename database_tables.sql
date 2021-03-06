DROP DATABASE IF EXISTS `sFHp69uV0B`;
CREATE DATABASE `sFHp69uV0B` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_unicode_ci;
USE `sFHp69uV0B`;

SET @PREVIOUS_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `Maintainers`;
DROP TABLE IF EXISTS `Authors`;
DROP TABLE IF EXISTS `People`;
DROP TABLE IF EXISTS `Packages`;

CREATE TABLE `Packages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(512) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `Version` varchar(16) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `Publication` datetime NOT NULL,
  `Title` varchar(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `Description` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_Version_Name` (`Version`,`Name`) USING BTREE,
  KEY `idx_Version_Name1` (`Version`,`Name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=208 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `People` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(128) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `Email` varchar(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `Authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `PackageID` int(11) NOT NULL,
  `PeopleID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_PackageID_PeopleID` (`PackageID`,`PeopleID`) USING BTREE,
  KEY `PackageID` (`PackageID`),
  KEY `idx_PeopleID` (`PeopleID`) USING BTREE,
  CONSTRAINT `Authors_ibfk_1` FOREIGN KEY (`PackageID`) REFERENCES `Packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Authors_ibfk_2` FOREIGN KEY (`PeopleID`) REFERENCES `People` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=325 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `Maintainers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `PackageID` int(11) NOT NULL,
  `PeopleID` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_PackageID_PeopleID` (`PackageID`,`PeopleID`) USING BTREE,
  KEY `idx_PeopleID` (`PeopleID`) USING BTREE,
  CONSTRAINT `Maintainers_ibfk_1` FOREIGN KEY (`PackageID`) REFERENCES `Packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Maintainers_ibfk_2` FOREIGN KEY (`PeopleID`) REFERENCES `People` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=197 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

SET FOREIGN_KEY_CHECKS = @PREVIOUS_FOREIGN_KEY_CHECKS;
