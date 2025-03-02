DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL,
    username varchar(45) DEFAULT NULL,
    first_name varchar(45) DEFAULT NULL,
    last_name varchar(45) DEFAULT NULL,
    email varchar(200) DEFAULT NULL,
    hashed_password varchar(200) DEFAULT NULL,
    role ENUM('admin', 'operator', 'viewer') DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);