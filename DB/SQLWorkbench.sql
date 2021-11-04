DROP DATABASE Vivant_DB;
CREATE DATABASE Vivant_DB;
USE Vivant_DB;

################################################

CREATE TABLE Doors (
	door_uuid CHAR(36) NOT NULL PRIMARY KEY,
    nickname VARCHAR(255) NOT NULL
);
CREATE TABLE Devices (
	device_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    door_uuid CHAR(36) NOT NULL,
	nickname VARCHAR(255) NOT NULL,
    FOREIGN KEY (door_uuid) REFERENCES Doors(door_uuid)
);
CREATE TABLE RingLog (
	ring_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	door_uuid CHAR(36) NOT NULL,
	dt datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (door_uuid) REFERENCES Doors(door_uuid)
);
CREATE TABLE TTSLog (
	tts_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	door_uuid CHAR(36) NOT NULL,
	request VARCHAR(255) NOT NULL,
	dt datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (door_uuid) REFERENCES Doors(door_uuid)
);
CREATE TABLE LockLog (
	lock_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	door_uuid CHAR(36) NOT NULL,
    device_id INT NOT NULL,
	door_status ENUM('UNLOCK', 'LOCK') NOT NULL,
	dt datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (door_uuid) REFERENCES Doors(door_uuid),
    FOREIGN KEY (device_id) REFERENCES Devices(device_id)
);
CREATE TABLE Updates (
	door_uuid CHAR(36) NOT NULL,
	ring_id INT,
	tts_id INT,
	lock_id INT,
	FOREIGN KEY (door_uuid) REFERENCES Doors(door_uuid),
    FOREIGN KEY (ring_id) REFERENCES RingLog(ring_id),
    FOREIGN KEY (tts_id) REFERENCES TTSLog(tts_id),
    FOREIGN KEY (lock_id) REFERENCES LockLog(lock_id)
);

################################################

INSERT INTO Doors (door_uuid, nickname) VALUES ('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 'Other Door');
INSERT INTO Devices (door_uuid, nickname) VALUES
('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 'iPhone 8'),
('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 'iPhone X');
INSERT INTO LockLog (door_uuid, device_id, door_status) VALUES
('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 1, 'LOCK'),
('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 2, 'UNLOCK');
INSERT INTO RingLog (door_uuid) VALUES ('d5e1bbbc-2120-470b-ace2-4b14ef3415b9');
INSERT INTO Updates (door_uuid, lock_id) VALUES ('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 1);


SELECT * FROM Doors;
SELECT * FROM Devices;
SELECT * FROM LockLog;
SELECT * FROM RingLog;
SELECT * FROM TTSLog;
SELECT * FROM Updates;

-- TEST DATA --
INSERT INTO LockLog (door_uuid, device_id, door_status) VALUES
('134f2cd6-7548-41b7-bea8-2b4d840fe3ef', 3, 'LOCK')
INSERT INTO Updates (door_uuid, lock_id) VALUES
('134f2cd6-7548-41b7-bea8-2b4d840fe3ef', 53)