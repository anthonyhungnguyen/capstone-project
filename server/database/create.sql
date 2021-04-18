DROP TABLE subject;

CREATE DATABASE capstone;

USE capstone;

CREATE TABLE subject(
	id VARCHAR(15) NOT NULL,
	group_code VARCHAR(10) NOT NULL,
    	semester INT NOT NULL,
	name VARCHAR(255) NOT NULL
);

DROP TABLE user;


USE capstone;
CREATE TABLE role(
  id INT AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL,
  PRIMARY KEY(id)
)

USE capstone;
CREATE TABLE user(
    id INT NOT NULL,
    password VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    
);

USE capstone;
CREATE TABLE user_role(
	id INT AUTO_INCREMENT,
	userid INT NOT NULL,
	roleid INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (userid) REFERENCES user(id),
	FOREIGN KEY (roleid) REFERENCES role(id)
)

DROP TABLE enrollment;


USE capstone;
CREATE TABLE enrollment(
    user_id INT NOT NULL,
    subject_id VARCHAR(15) NOT NULL,
    group_code VARCHAR(10) NOT NULL,
    semester INT NOT NULL,
    PRIMARY KEY(user_id, subject_id, group_code, semester),
    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE,
    FOREIGN KEY(subject_id, group_code, semester) REFERENCES subject(id, group_code, semester) ON UPDATE CASCADE
);


USE capstone;
CREATE TABLE schedule(
    id INT AUTO_INCREMENT,
    teacher_id VARCHAR(10) NOT NULL,
    device_id VARCHAR(10) NOT NULL,
    subject_id VARCHAR(15) NOT NULL,
    group_code VARCHAR(10) NOT NULL,
    semester INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    PRIMARY KEY(id)
);


USE capstone;

CREATE TABLE attendance_log(
    id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    group_code INT NOT NULL,
    semester INT NOT NULL,
    teacher_id INT NOT NULL,
    device_id INT NOT NULL,
    attendance_time TIMESTAMP,
    image_id VARCHAR(50),
    PRIMARY KEY(id)
);

USE capstone;

CREATE TABLE register(
    id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    image_link VARCHAR(255),
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE
);