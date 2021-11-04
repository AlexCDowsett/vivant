import pymysql

# Configuration
endpoint = 'vivant-db.c04gl03xq7f6.eu-west-2.rds.amazonaws.com'
username = 'admin'
password = '8Am5v9Ni'
db_name = 'Vivant_DB'

conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name)



class Door:
    def __init__(self, door_name):
        conn.begin()
        c = conn.cursor()
        
        c.execute('INSERT INTO Doors (nickname) VALUES (%s);', (door_name))
        conn.commit()

        c.execute('SELECT MAX(door_id) FROM Doors')
        self.id = int(c.fetchone()[0])
        self.name = door_name

        c.close()
        conn.close()
        

    def __del__(self):
        conn.begin()
        c = conn.cursor()

        c.execute("DELETE FROM Doors WHERE door_id='%s';", (self.id))
        c.commit()
        
        c.close()
        conn.close()
        
    def ring():
        ''


front_door = Door('Front Door')
back_door = Door('Back Door')

conn.begin()
c = conn.cursor()
c.execute('SELECT * FROM LockLog')

rows = c.fetchall()
for row in rows:
    print("{0} {1} {2}".format(row[0], row[1], row[2]))

c.close()
conn.close()

del front_door, back_door

conn.begin()
c = conn.cursor()
c.execute('SELECT * FROM LockLog')

rows = c.fetchall()
for row in rows:
    print("{0} {1}".format(row[0], row[1]))

c.close()
conn.close()

handler()
