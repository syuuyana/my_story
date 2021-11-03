CREATE DATABASE IF NOT EXISTS app;
USE app;


CREATE TABLE IF NOT EXISTS Profiles(
  id int PRIMARY KEY AUTO_INCREMENT,
  email varchar(50) NOT NULL,
  password varchar(20) NOT NULL,
  tel varchar(20) NOT NULL,
  name varchar(20) NOT NULL,
  times int DEFAULT 0
--  comment varchar(500) DEFAULT "Hello World!",
--  icon varchar(100) DEFAULT "static/default_user_icon.png"
);


INSERT INTO Profiles (email, password, tel, name) VALUES("syuu@email.com", "Password1", "09012345678", "syuu");
INSERT INTO Profiles (email, password, tel, name) VALUES("yana@email.com", "Password2", "08012345678", "yana");