DROP TABLE subject;

CREATE TABLE subject(
	id VARCHAR(15) NOT NULL,
	group_code VARCHAR(10) NOT NULL,
    semester INT NOT NULL,
	name VARCHAR(255) NOT NULL,
    week_day INT NOT NULL,
	time_range VARCHAR(20) NOT NULL,
	room VARCHAR(20),
	base VARCHAR(10),
    week_learn VARCHAR(255),
	CONSTRAINT PK_Subject PRIMARY KEY (id, group_code, semester)
);

DROP TABLE user;

CREATE TABLE user(
    id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    gender INT NOT NULL,
    major_code VARCHAR(50),
    image_url BLOB,
    CONSTRAINT PK_User PRIMARY KEY(id)
);

DROP TABLE enrollment;

CREATE TABLE enrollment(
    user_id INT NOT NULL,
    subject_id VARCHAR(15) NOT NULL,
    group_code VARCHAR(10) NOT NULL,
    semester INT NOT NULL,
    CONSTRAINT PK_enrollment PRIMARY KEY(user_id, subject_id, group_code, semester),
    CONSTRAINT FK_user_reference FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE ,
    CONSTRAINT FK_subject_reference FOREIGN KEY(subject_id, group_code, semester) REFERENCES subject(id, group_code, semester) ON UPDATE CASCADE ON DELETE CASCADE
);