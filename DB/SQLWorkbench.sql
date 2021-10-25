DROP DATABASE Vivant_DB;
CREATE DATABASE Vivant_DB;
USE Vivant_DB;

################################################

CREATE TABLE Doors (
	door_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nickname VARCHAR(255) NOT NULL
);

################################################

CREATE TABLE Devices (
	device_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    door_id INT NOT NULL,
	nickname VARCHAR(255) NOT NULL,
    FOREIGN KEY (door_id) REFERENCES Doors(door_id)
);

################################################

CREATE TABLE RingLog (
	ring_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	door_id INT NOT NULL,
	dt datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (door_id) REFERENCES Doors(door_id)
);

################################################

CREATE TABLE TTSLog (
	tts_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	door_id INT NOT NULL,
	request VARCHAR(255) NOT NULL,
	dt datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (door_id) REFERENCES Doors(door_id)
);

################################################

CREATE TABLE LockLog (
	lock_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	door_id INT NOT NULL,
    device_id INT NOT NULL,
	door_status ENUM('UNLOCK', 'LOCK') NOT NULL,
	dt datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (door_id) REFERENCES Doors(door_id),
    FOREIGN KEY (device_id) REFERENCES Devices(device_id)
);

################################################

CREATE TABLE TempUpdate (
	door_id INT NOT NULL,
	ring_id INT,
	tts_id INT,
	lock_id INT,
    FOREIGN KEY (door_id) REFERENCES Doors(door_id),
    FOREIGN KEY (ring_id) REFERENCES RingLog(ring_id),
    FOREIGN KEY (tts_id) REFERENCES TTSLog(tts_id),
    FOREIGN KEY (lock_id) REFERENCES LockLog(lock_id)
);

################################################

INSERT INTO Doors (nickname) VALUES
('Door 1'),
('Door 2');

SELECT * FROM Doors;

INSERT INTO Devices (door_id, nickname) VALUES
(1, 'local'),
(1, 'iPhone 8'),
(2, 'iPhone X');

SELECT * FROM Devices;

INSERT INTO LockLog (door_id, device_id, door_status) VALUES
(1, 1, 'LOCK'),
(2, 2, 'UNLOCK');

SELECT * FROM LockLog;

INSERT INTO TempUpdate (door_id, lock_id) VALUES
(1, 1);

SELECT * FROM TempUpdate;