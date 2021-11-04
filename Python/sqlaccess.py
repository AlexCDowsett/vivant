import pymysql
import uuid
import pickle
import time

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
            c.execute("SELECT * FROM Doors WHERE door_uuid=%s;", (self.uuid))

            if c.fetchone() == None:
                c.execute('INSERT INTO Doors (door_uuid, nickname) VALUES (%s, %s);', (self.uuid, self.name))
                conn.commit()
                log(self.name + ' was missing from the database and has now been added.')

            else:
                log(self.name + ' loaded.')
            
        except FileNotFoundError:
            log('New door detected.')
            fw = open('uuid.data', 'wb')
            self.uuid = uuid.uuid4()
            pickle.dump(self.uuid, fw)
            fw.close()

            c.execute('INSERT INTO Doors (door_uuid, nickname) VALUES (%s, %s);', (self.uuid, self.name))
            conn.commit()

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

        c.execute('INSERT INTO TempUpdate (ring_id) VALUES (%s);', (temp))
        conn.commit()

        c.close()

        log(self.name + "'s doorbell was rang.")

        # --> INSERT HERE CODE WHEN DOORBELL IS RUNG

    def unlock():
        ''

    def lock():
        ''
        

if __name__ == '__main__': # Only runs the following code if the program is the main program and is not imported into another.
    main() # Calls the main function

door = Door(door_name)

door.ring()

c = conn.cursor()
c.execute('SELECT * FROM Doors')
rows = c.fetchall()
for row in rows:
    print("{0} {1}".format(row[0], row[1]))
c.close()
conn.close()
