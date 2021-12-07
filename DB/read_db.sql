USE Vivant_DB;
SELECT * FROM Doors;
SELECT * FROM Users;
SELECT * FROM LockLog;
SELECT * FROM RingLog;
SELECT * FROM TTSLog;

INSERT INTO Users(Username, Password, DoorUUID, FirstName, LastName) VALUES
('alexd22', 'password', '134f2cd6-7548-41b7-bea8-2b4d840fe3ef', 'Alex', 'Dowsett'),
('sam22', 'password123', '134f2cd6-7548-41b7-bea8-2b4d840fe3ef', 'Sam', 'Thompson'),
('jacob123', 'password', 'd5e1bbbc-2120-470b-ace2-4b14ef3415b9', 'Jacob', 'Prosser');


DELETE FROM Users WHERE Username = 'alexd22';