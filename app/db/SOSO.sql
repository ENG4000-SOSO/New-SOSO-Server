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

DROP TABLE IF EXISTS satellite;

CREATE TABLE satellite (
    id SERIAL PRIMARY KEY,
    satellite_name VARCHAR(255) UNIQUE NOT NULL,
    storage_capacity DOUBLE PRECISION NOT NULL,
    power_capacity DOUBLE PRECISION NOT NULL,
    fov_max DOUBLE PRECISION NOT NULL,
    fov_min DOUBLE PRECISION NOT NULL,
    is_illuminated BOOLEAN DEFAULT FALSE,
    under_outage BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS ground_station;

CREATE TABLE ground_station (
    id SERIAL PRIMARY KEY,
    ground_station_name VARCHAR(255) UNIQUE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    elevation DOUBLE PRECISION NOT NULL,
    station_mask DOUBLE PRECISION NOT NULL,
    uplink_rate DOUBLE PRECISION NOT NULL,
    downlink_rate DOUBLE PRECISION NOT NULL,
    under_outage BOOLEAN DEFAULT FALSE
);