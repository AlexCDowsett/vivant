import pymysql
import uuid
import pickle
import time
import sched

# Configuration

endpoint = 'vivant-db.c04gl03xq7f6.eu-west-2.rds.amazonaws.com'
username = 'admin'
password = '8Am5v9Ni'
db_name = 'Vivant_DB'

door_name = 'Test Door'

conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name)

def log(statement):
    '''This function simply prints a string with the date and time as a prefix.'''
    print('[{}] {}'.format(time.strftime('%d/%m/%y|%H:%M:%S'), statement)) # Prints message to the console.


def main():
    ''


class Door:
    def __init__(self, door_name):
        self.name = door_name
        c = conn.cursor()
        
        try: 
            fd = open('uuid.data', 'rb')
            self.uuid = pickle.load(fd)
            
            c.execute('SELECT * FROM Doors WHERE door_uuid=%s;', (self.uuid))
            if c.fetchone() == None:
                c.execute('INSERT INTO Doors (door_uuid, nickname) VALUES (%s, %s);', (self.uuid, self.name))
                conn.commit()

            c.execute("SELECT device_id FROM Devices WHERE door_uuid=%s AND nickname='local';", (self.uuid))
            if c.fetchone() == None:
                c.execute('INSERT INTO Devices (door_uuid, nickname) VALUES (%s, %s);', (self.uuid, 'local'))
                conn.commit()
                
            c.execute("SELECT device_id FROM Devices WHERE door_uuid=%s AND nickname='local';", (self.uuid))
            self.device = c.fetchone()[0]

            log(self.name + ' loaded.')
            
        except FileNotFoundError:
            log('New door detected.')
            fw = open('uuid.data', 'wb')
            self.uuid = uuid.uuid4()
            pickle.dump(self.uuid, fw)
            fw.close()

            c.execute('INSERT INTO Doors (door_uuid, nickname) VALUES (%s, %s);', (self.uuid, self.name))
            conn.commit()
            c.execute('INSERT INTO Devices (door_uuid, nickname) VALUES (%s, %s);', (self.uuid, 'local'))
            conn.commit()
            c.execute("SELECT device_id FROM Devices WHERE door_uuid=%s AND nickname='local';", (self.uuid))
            self.device = c.fetchone()[0]

        c.close()
        

    def __del__(self):
        c = conn.cursor()

        c.execute("DELETE FROM Doors WHERE door_uuid=%s;", (self.uuid))
        conn.commit()
        
        c.close()

        log(self.name + ' was removed.')

        
    def ring(self):
        c = conn.cursor()
        
        c.execute('INSERT INTO RingLog (door_uuid) VALUES (%s);', (self.uuid))
        conn.commit()
        
        c.execute('SELECT MAX(ring_id) FROM RingLog WHERE door_uuid=%s;', (self.uuid))
        temp = c.fetchone()[0]
        
        c.execute('INSERT INTO Updates (door_uuid, ring_id) VALUES (%s, %s);', (self.uuid, temp))
        conn.commit()

        c.close()

        log(self.name + "'s doorbell was rang.")

        # --> INSERT HERE CODE WHEN DOORBELL IS RUNG

    def unlock(self):
        c = conn.cursor()

        c.execute('INSERT INTO LockLog (door_uuid, device_id, door_status) VALUES (%s, %s, %s);', (self.uuid, self.device, 'UNLOCK'))
        conn.commit()

        c.execute('SELECT MAX(lock_id) FROM LockLog WHERE door_uuid=%s AND device_id=%s;', (self.uuid, self.device))
        temp = c.fetchone()[0]

        c.execute('INSERT INTO Updates (door_uuid, lock_id) VALUES (%s, %s);', (self.uuid, temp))
        conn.commit()

        c.close()

        log(self.name + " was unlocked.")

        # --> INSERT HERE CODE WHEN DOOR IS UNLOCKED
        
    def lock(self):
        c = conn.cursor()

        c.execute('INSERT INTO LockLog (door_uuid, device_id, door_status) VALUES (%s, %s, %s);', (self.uuid, self.device, 'LOCK'))
        conn.commit()

        c.execute('SELECT MAX(lock_id) FROM LockLog WHERE door_uuid=%s AND device_id=%s;', (self.uuid, self.device))
        temp = c.fetchone()[0]

        c.execute('INSERT INTO Updates (door_uuid, lock_id) VALUES (%s, %s);', (self.uuid, temp))
        conn.commit()

        c.close()

        log(self.name + " was locked.")

        # --> INSERT HERE CODE WHEN DOOR IS LOCKED
        
    def update(self, *args):
        print('Checking for updates...')
        c = conn.cursor()

        c.execute('SELECT lock_id, tts_id FROM Updates WHERE door_uuid=%s AND ring_id IS NULL;', (self.uuid))
        rows = c.fetchall()
        c.execute('DELETE FROM Updates WHERE door_uuid=%s AND ring_id IS NULL;', (self.uuid))
        conn.commit()
        for row in rows:
            
            if row[0] != None: # Unlock/lock request
                c.execute('SELECT door_uuid, door_status FROM LockLog WHERE lock_id=%s;', (row[0]))
                temp = c.fetchone()
                if temp[0] == str(self.uuid):
                    print('Door has been ' + temp[1] + 'ED.')
                    
            elif row[1] != None: # TTS request
                print("TTS request inbound.")
        
        c.close()
        s.enter(1, 1, door.update, (s,))
            
                

if __name__ == '__main__': # Only runs the following code if the program is the main program and is not imported into another.
    main() # Calls the main function


door = Door(door_name)

door.ring()
door.lock()
door.unlock()

print(door.uuid)

s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, door.update, (s,))
s.run()

#c = conn.cursor()
#c.execute('SELECT * FROM Doors')
#rows = c.fetchall()
#for row in rows:
#    print("[{0}, {1}]".format(row[0], row[1]))
#c.close()

conn.close()
