CREATE DATABASE filetra;

USE filetra;
GO

CREATE TABLE users (
	usr_id varchar(36) NOT NULL PRIMARY KEY,
	usr_email varchar(255) NOT NULL,
	usr_password varchar(255) NOT NULL,
	usr_name varchar(128),
);

CREATE TABLE salts (
	slt_id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	usr_id varchar(36) NOT NULL FOREIGN KEY REFERENCES users(usr_id),
	slt_salt varchar(64) NOT NULL
);

CREATE TABLE groups (
	grp_id varchar(36) NOT NULL PRIMARY KEY,
	grp_name varchar(255) NOT NULL,
	usr_owner_id varchar(36) NOT NULL FOREIGN KEY REFERENCES users(usr_id),
);

CREATE TABLE directories (
	dir_id varchar(36) NOT NULL PRIMARY KEY,
	dir_name varchar(255) NOT NULL,
	grp_owner_id varchar(36) NOT NULL FOREIGN KEY REFERENCES groups(grp_id),
);

CREATE TABLE user_permissions (
	pms_id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	usr_id varchar(36) NOT NULL FOREIGN KEY REFERENCES users(usr_id),
	grp_id varchar(36) NOT NULL FOREIGN KEY REFERENCES groups(grp_id),
	pms_allow_add bit,
	pms_allow_edit bit,
	pms_allow_delete bit
);