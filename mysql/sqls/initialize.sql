-- database app 作成 --
CREATE DATABASE IF NOT EXISTS app;
USE app;


-- table Profile 作成 --
CREATE TABLE IF NOT EXISTS Profiles(
  id int PRIMARY KEY AUTO_INCREMENT,
  email varchar(50) NOT NULL,
  password varchar(20) NOT NULL,
  tel varchar(20) NOT NULL,
  name varchar(20) NOT NULL,
  times int DEFAULT 0
);


-- テストデータ挿入 --
INSERT INTO Profiles (email, password, tel, name) VALUES("syuu@email.com", "Password1", "09012345678", "syuu");
INSERT INTO Profiles (email, password, tel, name) VALUES("yana@email.com", "Password2", "08012345678", "yana");