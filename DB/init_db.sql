DROP DATABASE Vivant_DB;
CREATE DATABASE Vivant_DB;
USE Vivant_DB;

################################################

CREATE TABLE Doors (
	DoorUUID CHAR(36) NOT NULL PRIMARY KEY,
    Nickname VARCHAR(255) NOT NULL,
    LastActive datetime DEFAULT CURRENT_TIMESTAMP,
    AuthenticationCode INT
);
CREATE TABLE Users (
	Username VARCHAR(255) NOT NULL PRIMARY KEY,
    Password VARCHAR(255) NOT NULL,
    DoorUUID CHAR(36) NOT NULL,
	FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    FOREIGN KEY (DoorUUID) REFERENCES Doors(DoorUUID)
);
CREATE TABLE RingLog (
	RingID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	DoorUUID CHAR(36) NOT NULL,
    Executed BOOL DEFAULT 0,
	DateTime datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (DoorUUID) REFERENCES Doors(DoorUUID)
);
CREATE TABLE TTSLog (
	TTSID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	DoorUUID CHAR(36) NOT NULL,
	Request VARCHAR(255) NOT NULL,
    Executed BOOL DEFAULT 0,
	DateTime datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (DoorUUID) REFERENCES Doors(DoorUUID)
);
CREATE TABLE LockLog (
	LockID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	DoorUUID CHAR(36) NOT NULL,
    Username VARCHAR(255),
	DoorStatus ENUM('UNLOCK', 'LOCK') NOT NULL,
    Executed BOOL DEFAULT 0,
	DateTime datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (DoorUUID) REFERENCES Doors(DoorUUID),
    FOREIGN KEY (Username) REFERENCES Users(Username)
);

################################################

INSERT INTO Doors (DoorUUID, Nickname) VALUES ('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 'Other Door');
INSERT INTO LockLog (DoorUUID, DoorStatus) VALUES
('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 'LOCK'),
('d5e1bbbc-2120-470b-ace2-4b14ef3415b9', 'UNLOCK');
INSERT INTO RingLog (DoorUUID) VALUES ('d5e1bbbc-2120-470b-ace2-4b14ef3415b9');
