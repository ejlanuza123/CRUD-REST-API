/*
SQLyog Community v13.2.1 (64 bit)
MySQL - 5.7.44-log : Database - company
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`company` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `company`;

/*Table structure for table `accounts` */

DROP TABLE IF EXISTS `accounts`;

CREATE TABLE `accounts` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `accounts` */

insert  into `accounts`(`username`,`password`) values 
('ejlanuza0123','lanuza123');

/*Table structure for table `department` */

DROP TABLE IF EXISTS `department`;

CREATE TABLE `department` (
  `Dnumber` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Dname` varchar(45) NOT NULL,
  `Mgr_ssn` int(10) unsigned NOT NULL,
  `Mgr_start_date` date NOT NULL,
  PRIMARY KEY (`Dnumber`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `department` */

insert  into `department`(`Dnumber`,`Dname`,`Mgr_ssn`,`Mgr_start_date`) values 
(1,'Headquarters',888665555,'1981-06-19'),
(4,'Administration',987654321,'1995-01-01'),
(5,'Research',333445555,'1988-05-02');

/*Table structure for table `dependent` */

DROP TABLE IF EXISTS `dependent`;

CREATE TABLE `dependent` (
  `Dep_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Essn` int(10) unsigned NOT NULL,
  `Dependent_name` varchar(45) NOT NULL,
  `Sex` char(1) NOT NULL,
  `Bdate` date NOT NULL,
  `Relationship` varchar(45) NOT NULL,
  PRIMARY KEY (`Dep_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `dependent` */

insert  into `dependent`(`Dep_id`,`Essn`,`Dependent_name`,`Sex`,`Bdate`,`Relationship`) values 
(1,333445555,'Alice','F','1986-04-05','Daughter'),
(2,333445555,'Theodore','M','1983-10-25','Son'),
(3,333445555,'Joy','F','1958-05-03','Spouse'),
(4,987654321,'Abner','M','1942-02-28','Spouse'),
(5,123456789,'Michael','M','1988-01-04','Son'),
(6,123456789,'Alice','F','1988-12-30','Daughter'),
(7,123456789,'Elizabeth','F','1967-05-05','Spouse');

/*Table structure for table `dept_locations` */

DROP TABLE IF EXISTS `dept_locations`;

CREATE TABLE `dept_locations` (
  `DL_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Dnumber` int(10) unsigned NOT NULL,
  `Dlocation` varchar(45) NOT NULL,
  PRIMARY KEY (`DL_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `dept_locations` */

insert  into `dept_locations`(`DL_id`,`Dnumber`,`Dlocation`) values 
(1,1,'Houston'),
(2,4,'Stafford'),
(3,5,'Bellaire'),
(4,5,'Sugarland'),
(5,5,'Houston');

/*Table structure for table `employee` */

DROP TABLE IF EXISTS `employee`;

CREATE TABLE `employee` (
  `ssn` int(10) unsigned NOT NULL,
  `Fname` varchar(45) NOT NULL,
  `Minit` char(1) DEFAULT NULL,
  `Lname` varchar(45) NOT NULL,
  `Bdate` date NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Sex` char(1) NOT NULL,
  `Salary` double NOT NULL,
  `Super_ssn` int(10) unsigned DEFAULT NULL,
  `DL_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ssn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `employee` */

insert  into `employee`(`ssn`,`Fname`,`Minit`,`Lname`,`Bdate`,`Address`,`Sex`,`Salary`,`Super_ssn`,`DL_id`) values 
(2022,'Rodrigo','M','Lanuza','1999-04-15','San miguel','M',2000,293929,1),
(2023,'vincent','M','santos','2000-12-22','timiguiban','M',2000,293929,1),
(4444,'Tj','M','Dimagiba','2000-05-02','Tiniguiban','M',22222,293929,1),
(12223,'giana','M','santos','2002-02-05','timiguiban','F',2000,293929,1),
(20211,'Xyril','Y','Zancisco','2015-12-22','Tiniguiban','M',4000,2222,4),
(20233,'Nani','E','Kudasai','2010-05-23','Sta monica','M',300,232323,2),
(32323,'Kris','D','Toffer','1999-03-02','San Jose','M',49999,2323,3),
(55454,'Francis','J','Zancisco','2000-06-22','Tiniguiban','M',4000,2323,4),
(344234,'Trevor','M','Nalica','1995-04-03','Bancao bancao','M',49999,2022,1),
(565656,'Michael','J','RElova','2000-05-05','San miguel','M',49999,23232,3),
(4323423,'Frabz','M','Chang','1999-04-03','Tiniguiban','M',55555,23232,4),
(6253671,'John','M','Victor','1992-03-22','Bancao bancao','M',323232,222323,3),
(123456789,'John','B','Smith','1965-01-09','731 Fondren, Houston,\nTX','M',30000,333445555,5),
(333445555,'Franklin','T','Wong','1955-12-08','638 Voss, Houston,\nTX','M',40000,888665555,5),
(453453453,'Joyce','A','English','1972-07-31','5631 Rice, Houston,\nTX','F',25000,333445555,5),
(666884444,'Ramesh','K','Narayan','1962-09-15','975 Fire Oak, Humble,\nTX','M',38000,333445555,5),
(888665555,'James','E','Borg','1937-11-10','450 Stone, Houston,\nTX','M',55000,NULL,1),
(987654321,'Jennifer','S','Wallace','1941-06-20','291 Berry, Bellaire,\nTX','F',43000,888665555,4),
(987987987,'Ahmad','V','Jabbar','1969-03-29','980 Dallas, Houston,\nTX','M',25000,987654321,4),
(999887777,'Alicia','J','Zelaya','1968-01-19','3321 Castle, Spring,\nTX','F',25000,987654321,4);

/*Table structure for table `project` */

DROP TABLE IF EXISTS `project`;

CREATE TABLE `project` (
  `Pnumber` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Pname` varchar(45) NOT NULL,
  `DL_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`Pnumber`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;

/*Data for the table `project` */

insert  into `project`(`Pnumber`,`Pname`,`DL_id`) values 
(1,'ProductX',3),
(2,'ProductY',4),
(3,'ProductZ',5),
(10,'Computerization',2),
(20,'Reorganization',1),
(30,'Newbenefits',2);

/*Table structure for table `works_on` */

DROP TABLE IF EXISTS `works_on`;

CREATE TABLE `works_on` (
  `work_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Essn` int(10) unsigned NOT NULL,
  `Pno` int(10) unsigned NOT NULL,
  `Hours` double DEFAULT NULL,
  PRIMARY KEY (`work_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `works_on` */

insert  into `works_on`(`work_id`,`Essn`,`Pno`,`Hours`) values 
(1,123456789,1,32.5),
(2,123456789,2,7.5),
(3,666884444,3,40),
(4,453453453,1,20),
(5,453453453,2,20),
(6,333445555,2,10),
(7,333445555,3,10),
(8,333445555,10,10),
(9,333445555,20,10),
(10,999887777,30,30),
(11,999887777,10,10),
(12,987987987,10,35),
(13,987987987,30,5),
(14,987654321,30,20),
(15,987654321,20,15),
(16,888665555,20,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
