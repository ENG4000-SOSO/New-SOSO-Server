CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TYPE user_role AS ENUM ('admin', 'operator', 'viewer');

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS satellite;
DROP TABLE IF EXISTS ground_station;
DROP TABLE IF EXISTS image_request;
DROP TABLE IF EXISTS activity_request;
DROP TABLE IF EXISTS outage_request;
DROP TABLE IF EXISTS mission CASCADE;
DROP TABLE IF EXISTS schedule_request;

CREATE TABLE users (
    id SERIAL,
    username varchar(45) DEFAULT NULL,
    first_name varchar(45) DEFAULT NULL,
    last_name varchar(45) DEFAULT NULL,
    email varchar(200) DEFAULT NULL,
    hashed_password varchar(200) DEFAULT NULL,
    role user_role DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

CREATE TABLE satellite (
    id SERIAL PRIMARY KEY,
    satellite_name VARCHAR(255) UNIQUE NOT NULL,
    tle_line1 VARCHAR(255) NOT NULL,
    tle_line2 VARCHAR(255) NOT NULL,
    storage_capacity DOUBLE PRECISION,
    power_capacity DOUBLE PRECISION,
    fov_max DOUBLE PRECISION,
    fov_min DOUBLE PRECISION,
    is_illuminated BOOLEAN DEFAULT FALSE,
    under_outage BOOLEAN DEFAULT FALSE
);

CREATE TABLE ground_station (
    id SERIAL PRIMARY KEY,
    ground_station_name VARCHAR(255) UNIQUE NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    elevation DOUBLE PRECISION NOT NULL,
    send_mask DOUBLE PRECISION,
    receive_mask DOUBLE PRECISION,
    uplink_rate DOUBLE PRECISION NOT NULL,
    downlink_rate DOUBLE PRECISION NOT NULL,
    under_outage BOOLEAN DEFAULT FALSE
);

CREATE TABLE mission (
    id SERIAL PRIMARY KEY,
    mission_name VARCHAR NOT NULL,
    mission_start TIMESTAMP NOT NULL,
    mission_end TIMESTAMP NOT NULL
);

CREATE TABLE image_request (
    id SERIAL PRIMARY KEY,
    image_name VARCHAR NOT NULL,
    mission_id INTEGER NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    priority INTEGER NOT NULL,
    image_type VARCHAR,
    image_start_time TIMESTAMP NOT NULL,
    image_end_time TIMESTAMP NOT NULL,
    delivery_time TIMESTAMP NOT NULL,
    recurrence_revisit VARCHAR,
    recurrence_number_of_revisits INTEGER,
    recurrence_revisit_frequency INTEGER,
    recurrence_revisit_frequency_units VARCHAR,
    FOREIGN KEY (mission_id) REFERENCES mission(id) ON DELETE CASCADE
);

CREATE TABLE activity_request (
    id SERIAL PRIMARY KEY,
    target VARCHAR NOT NULL,
    activity VARCHAR NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    duration VARCHAR NOT NULL,
    repeat_cycle_repetition VARCHAR,
    repeat_cycle_frequency_minimum_gap VARCHAR,
    repeat_cycle_frequency_maximum_gap VARCHAR,
    payload_outage VARCHAR NOT NULL
);

CREATE TABLE outage_request (
    id SERIAL PRIMARY KEY,
    target VARCHAR NOT NULL,
    activity VARCHAR NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL
);

CREATE TABLE schedule_request (
    id UUID PRIMARY KEY,
    mission_id INTEGER NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    input_object_key VARCHAR,
    output_object_key VARCHAR,
    status VARCHAR,
    FOREIGN KEY (mission_id) REFERENCES mission(id) ON DELETE CASCADE
);
