import pymysql
import uuid
import pickle
import time
import datetime
import sched

# Configuration

endpoint = 'vivant-db.c04gl03xq7f6.eu-west-2.rds.amazonaws.com'
username = 'admin'
password = '8Am5v9Ni'
db_name = 'Vivant_DB'

door_name = 'Test Door'
check_threshold = 5

conn = pymysql.connect(host=endpoint, user=username, password=password, database=db_name)

def log(statement):
    '''This function simply prints a string with the date and time as a prefix.'''
    print('[{}] {}'.format(time.strftime('%d/%m/%y|%H:%M:%S'), statement)) # Prints message to the console.


def main():
    door = Door()

    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, door.check, (s,))
    s.run()
    conn.close()


class Door:
    def __init__(self):
        
        try: 
            fd = open('uuid.data', 'rb')
            self.uuid = pickle.load(fd)

            c = conn.cursor()
            
            c.execute('SELECT * FROM Doors WHERE DoorUUID=%s;', (self.uuid))
            result = c.fetchone()
            if result == None:
                
                self.name = door_name
                c.execute('INSERT INTO Doors (DoorUUID, Nickname) VALUES (%s, %s);', (self.uuid, self.name))
                conn.commit()
                c.close()
                
            else:
                self.name = result[1]
            
            log(self.name + ' (' + str(self.uuid) + ') online.')
            
        except FileNotFoundError:
            log('New door detected.')
            self.__new()


        
    def __del__(self):
        conn.close()
        log(self.name + ' ('+ str(self.uuid) + ') offline.')


    def __new(self):
        c = conn.cursor()
        
        fw = open('uuid.data', 'wb')
        self.uuid = uuid.uuid4()
        pickle.dump(self.uuid, fw)
        fw.close()

        self.name = door_name
        c.execute('INSERT INTO Doors (DoorUUID, Nickname) VALUES (%s, %s);', (self.uuid, self.name))
        conn.commit()
        c.close()

        log(self.name + ' (' + str(self.uuid) + ') online.')

        # --> INSERT HERE CODE WHEN DOOR IS SET UP FOR FIRST TIME
        
    def ring(self, hidden=False):
        if hidden == False:
            c = conn.cursor()      
            c.execute('INSERT INTO RingLog (DoorUUID, Executed) VALUES (%s, 1);', (self.uuid))
            conn.commit()
            c.close()

        log(self.name + "'s doorbell was rang.")

        # --> INSERT HERE CODE WHEN DOORBELL IS RANG

    def unlock(self, hidden=False):
        if hidden == False:
            c = conn.cursor()
            c.execute('INSERT INTO LockLog (DoorUUID, DoorStatus, Executed) VALUES (%s, %s, 1);', (self.uuid, 'UNLOCK'))
            conn.commit()
            c.close()

        log(self.name + " was unlocked.")

        # --> INSERT HERE CODE WHEN DOOR IS UNLOCKED
        
    def lock(self, hidden=False):
        if hidden == False:
            c = conn.cursor()
            c.execute('INSERT INTO LockLog (DoorUUID, DoorStatus, Executed) VALUES (%s, %s, 1);', (self.uuid, 'LOCK'))
            conn.commit()
            c.close()

        log(self.name + " was locked.")

        # --> INSERT HERE CODE WHEN DOOR IS LOCKED

    def tts(self, request, hidden=False):
        if hidden == False:
            c = conn.cursor()
            c.execute('INSERT INTO TTSLog (DoorUUID, Request, Executed) VALUES (%s, %s, 1);', (self.uuid, request))
            conn.commit()
            c.close()

        log(self.name + "'s Text-To-Speech message recieved: " + request)

        # --> INSERT HERE CODE FOR TTS
        
    def check(self, s=None):

        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt_threshold = (datetime.datetime.now() - datetime.timedelta(seconds=check_threshold)).strftime("%Y-%m-%d %H:%M:%S")
        c = conn.cursor()
        updates = False

        # Updates last active time for door.
        c.execute('UPDATE Doors SET LastActive = %s WHERE DoorUUID = %s;', (dt, self.uuid,))

        # Check if any the door has been remotely rang since last check.
        c.execute('SELECT * FROM RingLog WHERE Executed = 0 AND DoorUUID=%s AND DateTime > %s;', (self.uuid, dt_threshold))
        ans = c.fetchone()
        if ans is not None:
            self.ring(hidden=True)
            c.execute('UPDATE RingLog SET Executed = 1 WHERE RingID = %s;', (ans[0],))
            updates = True

        # Check if the door has been remotely locked or unlocked since last check.
        c.execute('SELECT * FROM LockLog WHERE Executed = 0 AND DoorUUID=%s AND DateTime > %s;', (self.uuid, dt_threshold))
        ans = c.fetchone()
        if ans is not None:
            if ans[3] == 'UNLOCK':
                self.unlock(hidden=True)
            elif ans[3] == 'LOCK':
                self.lock(hidden=False)
            c.execute('UPDATE LockLog SET Executed = 1 WHERE LockID = %s;', (ans[0],))
            updates = True

        # Check ifa Text-To-Speech request has been sent since last check.
        c.execute('SELECT * FROM TTSLog WHERE Executed = 0 AND DoorUUID=%s AND DateTime > %s;', (self.uuid, dt_threshold))
        ans = c.fetchone()
        if ans is not None:
            self.tts(ans[2], hidden=True)
            c.execute('UPDATE TTSLog SET Executed = 1 WHERE TTSID = %s;', (ans[0],))
            updates = True

        conn.commit() 
        c.close()

        if s is not None:
            s.enter(1, 1, self.check, (s,))

        return updates
            
                

if __name__ == '__main__': # Only runs the following code if the program is the main program and is not imported into another.
    main() # Calls the main function

#door.ring()
#door.lock()
#door.unlock()
#door.tts("Hello")


