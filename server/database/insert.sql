-- Subject Table
INSERT INTO subject VALUES("CO3066", "CC01", 201, "Công nghệ phần mềm nâng cao", 2, "7:00 - 9:50", "B9-303", "BK-CS1", "--|--|41|42|43|44|--|46|47|48|49|50|51|");
INSERT INTO subject VALUES("CO3067", "CC01", 201, "Tính toán song song", 2, "15:00 - 17:50", "B1-201", "BK-CS1", "--|--|41|42|43|44|--|46|47|48|49|--|--|--|--|01|");
INSERT INTO subject VALUES("SP1009", "CC03", 201, "Đường lối cách mạng của Đảng Cộng sản Việt Nam", 3, "8:00 - 10:50", "B8-303", "BK-CS1", "39|40|41|42|43|44|--|46|47|48|49|50|51|");
INSERT INTO subject VALUES("CO3068", "CC01", 201, "Tính toán song song", 5, "12:00 - 14:50", "A5-106.1", "BK-CS1", "--|--|--|--|--|44|--|46|47|48|49|50|51|52|");
INSERT INTO subject VALUES("CO3065", "CC01", 201, "Công nghệ phần mềm nâng cao", 5, "15:00 - 17:50", "B2-202", "BK-CS1", "39|40|41|42|43|44|--|46|47|48|49|");
INSERT INTO subject VALUES("CO3021", "CC01", 201, "Hệ quản trị cơ sở dữ liệu", 7, "12:00 - 14:50", "B2-201", "BK-CS1", "--|40|41|42|43|44|--|46|47|48|49|50|51|");
INSERT INTO subject VALUES("CO4027", "CC01", 201, "Học máy", 4, "12:00 - 14:50", "B2-201", "BK-CS1", "39|40|41|42|43|44|--|46|47|48|49|50|51|");

-- User Table
INSERT INTO user VALUES(1752259, "Nguyễn Phúc Hưng", 1, "CC17KHM", "");
INSERT INTO user VALUES(1752015, "Nguyễn Sỹ Đức", 1, "CC17KHM", "");
INSERT INTO user VALUES(1752041, "Nguyễn Anh Hoàng Phúc", 1, "CC17KHM", "");
INSERT INTO user VALUES(1752025, "Trần Lê Minh Khoa", 1, "CC17KHM", "");

-- Hung's Enrollment
INSERT INTO enrollment VALUES(1752259, "CO3066", "CC01", 201);
INSERT INTO enrollment VALUES(1752259, "CO3067", "CC01", 201);
INSERT INTO enrollment VALUES(1752259, "SP1009", "CC03", 201);
INSERT INTO enrollment VALUES(1752259, "CO3068", "CC01", 201);
INSERT INTO enrollment VALUES(1752259, "CO3065", "CC01", 201);
INSERT INTO enrollment VALUES(1752259, "CO3021", "CC01", 201);

-- Duc's Enrollment
INSERT INTO enrollment VALUES(1752015, "CO3066", "CC01", 201);
INSERT INTO enrollment VALUES(1752015, "CO3067", "CC01", 201);
INSERT INTO enrollment VALUES(1752015, "SP1009", "CC03", 201);
INSERT INTO enrollment VALUES(1752015, "CO3068", "CC01", 201);
INSERT INTO enrollment VALUES(1752015, "CO3065", "CC01", 201);
INSERT INTO enrollment VALUES(1752015, "CO3021", "CC01", 201);
INSERT INTO enrollment VALUES(1752015, "CO4027", "CC01", 201);

-- Phuc's Enrollment
INSERT INTO enrollment VALUES(1752041, "CO3066", "CC01", 201);
INSERT INTO enrollment VALUES(1752041, "CO3067", "CC01", 201);
INSERT INTO enrollment VALUES(1752041, "SP1009", "CC03", 201);
INSERT INTO enrollment VALUES(1752041, "CO3068", "CC01", 201);
INSERT INTO enrollment VALUES(1752041, "CO3065", "CC01", 201);
INSERT INTO enrollment VALUES(1752041, "CO3021", "CC01", 201);
INSERT INTO enrollment VALUES(1752041, "CO4027", "CC01", 201);

USE capstone;

/* Test - Check-in success */
INSERT INTO subject VALUES("CO0001", "CC01", 201, "Test Subject", 3, "00:01 - 23:59", "B2-201", "BK-CS1", "39|40|41|42|43|44|--|46|47|48|49|50|51|52");
INSERT INTO enrollment VALUES(1752259, "CO0000", "CC01", 201);