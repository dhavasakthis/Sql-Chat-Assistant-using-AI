
-- CREATE DATABASE Emp;

use Emp;

create TABLE Employee(
EmpId char(5) PRIMARY KEY,
name Varchar(10),
Dept varchar(10),
Salary varchar(10)
);

insert into Employee (EmpId,name,Dept,Salary)
values
(1,'John','Production',1000),
(2,'Jose','Mech',2000),
(3,'Ram','Production',3000),
(4,'peter','Sales',4000),
(5,'Mark','Marketing',5000),
(6,'Leo','Production',2000),
(7,'Ashif','Mech',1000),
(8,'akash','Production',3000),
(9,'issac','Sales',5000),
(10,'David','Marketing',4000),
(11,'John','Production',1000),
(12,'Jose','Mech',2000),
(13,'Ram','Production',3000),
(14,'peter','Sales',4000),
(15,'Mark','Marketing',5000),
(16,'Leo','Production',2000),
(17,'Ashif','Mech',1000),
(18,'akash','Production',3000),
(19,'issac','Sales',5000),
(20,'David','Marketing',4000),
(21,'John','Production',1000),
(22,'Jose','Mech',2000),
(23,'Ram','Production',3000),
(24,'peter','Sales',4000),
(25,'Mark','Marketing',5000),
(26,'Leo','Production',2000),
(27,'Ashif','Mech',1000),
(28,'akash','Production',3000),
(29,'issac','Sales',5000),
(30,'David','Marketing',4000),
(31,'John','Production',1000),
(32,'Jose','Mech',2000),
(33,'Ram','Production',3000),
(34,'peter','Sales',4000),
(35,'Mark','Marketing',5000),
(36,'Leo','Production',2000),
(37,'Ashif','Mech',1000),
(38,'akash','Production',3000),
(39,'issac','Sales',5000),
(40,'David','Marketing',4000),
(41,'John','Production',1000),
(42,'Jose','Mech',2000),
(43,'Ram','Production',3000),
(44,'peter','Sales',4000),
(45,'Mark','Marketing',5000),
(46,'Leo','Production',2000),
(47,'Ashif','Mech',1000),
(48,'akash','Production',3000),
(49,'issac','Sales',5000),
(50,'David','Marketing',4000);

SELECT * FROM Employee;

SELECT COUNT(*) FROM Employee

SELECT COUNT(*) FROM Employee WHERE Dept='Sales';

SELECT COUNT(*) FROM Employee WHERE Dept = 'Marketing';