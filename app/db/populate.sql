-- Insert statements for users table
INSERT INTO users (username, first_name, last_name, email, hashed_password, role, is_active) VALUES
    ('jdoe', 'John', 'Doe', 'jdoe@example.com', '$2a$12$1n4YVOWG/pP6nBaQ3q/lg.Wy/fwMbaXncmJ.zAIvs0oYBnxKn5fYW', 'admin', TRUE),
    ('asmith', 'Alice', 'Smith', 'asmith@example.com', '$2a$12$1n4YVOWG/pP6nBaQ3q/lg.Wy/fwMbaXncmJ.zAIvs0oYBnxKn5fYW', 'admin', TRUE),
    ('bwayne', 'Bruce', 'Wayne', 'bwayne@example.com', '$2a$12$1n4YVOWG/pP6nBaQ3q/lg.Wy/fwMbaXncmJ.zAIvs0oYBnxKn5fYW', 'viewer', FALSE),
    ('ckent', 'Clark', 'Kent', 'ckent@example.com', '$2a$12$1n4YVOWG/pP6nBaQ3q/lg.Wy/fwMbaXncmJ.zAIvs0oYBnxKn5fYW', 'admin', TRUE),
    ('dprince', 'Diana', 'Prince', 'dprince@example.com', '$2a$12$1n4YVOWG/pP6nBaQ3q/lg.Wy/fwMbaXncmJ.zAIvs0oYBnxKn5fYW', 'admin', TRUE)
;

-- Insert statements for satellite table
INSERT INTO satellite (satellite_name, tle_line1, tle_line2, storage_capacity, power_capacity, fov_max, fov_min, is_illuminated, under_outage) VALUES
    ('Hubble', '1 20580U 90037B   22345.91473380  .00000210  00000-0  10000-3 0  9990', '2 20580  28.4710  32.5128 0002550  87.5643 272.6629 14.34320633134567', 500.0, 1000.0, 45.0, 10.0, TRUE, FALSE),
    ('ISS', '1 25544U 98067A   22345.57659722  .00001532  00000-0  32904-4 0  9992', '2 25544  51.6451 140.1420 0007106  45.2510  90.7513 15.49507138336609', 2000.0, 5000.0, 60.0, 15.0, TRUE, FALSE),
    ('Landsat-8', '1 39084U 13008A   22345.50159722  .00000067  00000-0  12345-4 0  9997', '2 39084  98.2071  50.2498 0001430  98.3528 261.7564 14.57117234123456', 1000.0, 1500.0, 50.0, 12.0, FALSE, FALSE),
    ('Terra', '1 25994U 99068A   22345.89201289  .00000123  00000-0  45678-5 0  9998', '2 25994  98.2098  70.3512 0001756  102.3567  257.6489 14.57198333123456', 800.0, 1200.0, 55.0, 14.0, FALSE, TRUE),
    ('Aqua', '1 27424U 02022A   22345.78034567  .00000178  00000-0  56789-6 0  9993', '2 27424  98.2097  80.5412 0001612  110.7892  249.4561 14.57189234123456', 900.0, 1300.0, 52.0, 13.0, TRUE, FALSE)
;

-- Insert statements for ground_station table
INSERT INTO ground_station (ground_station_name, latitude, longitude, elevation, send_mask, receive_mask, uplink_rate, downlink_rate, under_outage) VALUES
    ('Houston Station', 29.5623, -95.0830, 10.0, 5.0, 5.0, 100.0, 200.0, FALSE),
    ('Canberra Station', -35.4011, 148.9819, 700.0, 10.0, 10.0, 150.0, 250.0, FALSE),
    ('Madrid Station', 40.4310, -4.2485, 700.0, 8.0, 8.0, 120.0, 220.0, FALSE),
    ('Goldstone Station', 35.4259, -116.8897, 1000.0, 12.0, 12.0, 180.0, 280.0, TRUE),
    ('Santiago Station', -33.4521, -70.6769, 500.0, 7.0, 7.0, 130.0, 230.0, FALSE)
;

-- Insert statements for mission table
INSERT INTO mission (mission_name, mission_start, mission_end) VALUES
    ('Apollo 11', '1969-07-16 13:32:00', '1969-07-24 16:50:35'),
    ('Mars Rover Curiosity', '2011-11-26 15:02:00', '2011-11-27 15:02:00'),
    ('Hubble Servicing Mission 4', '2009-05-11 18:01:00', '2009-05-24 15:57:00'),
    ('Voyager 1 Launch', '1977-09-05 12:56:00', '1979-09-05 12:56:00'),
    ('James Webb Space Telescope Deployment', '2021-12-25 12:20:00', '2024-12-25 12:20:00')
;

-- Insert statements for image request table
INSERT INTO image_request (image_name, mission_id, latitude, longitude, priority, image_type, image_start_time, image_end_time, delivery_time) VALUES
    ('request_001', 1, 37.7749, -122.4194, 2, 'high', '2025-04-16 10:00:00', '2025-04-16 10:15:00', '2025-04-16 11:00:00'),
    ('request_002', 2, 34.0522, -118.2437, 1, 'medium', '2025-04-16 09:30:00', '2025-04-16 09:45:00', '2025-04-16 10:30:00'),
    ('request_003', 3, 40.7128, -74.0060, 3, 'low', '2025-04-16 08:00:00', '2025-04-16 08:20:00', '2025-04-16 09:00:00'),
    ('request_004', 1, 48.8566, 2.3522, 1, 'medium', '2025-04-16 07:15:00', '2025-04-16 07:30:00', '2025-04-16 08:00:00'),
    ('request_005', 2, 51.5074, -0.1278, 2, 'high', '2025-04-16 11:00:00', '2025-04-16 11:20:00', '2025-04-16 12:00:00')
;
