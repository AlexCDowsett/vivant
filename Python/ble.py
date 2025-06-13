from bluepy import btle
import struct
import time

def main():
    pass
    

class bleDelegate(object):
    def __init__(self, *args):
        #btle.DefaultDelegate.__init__(self)
        self.handle = 1
        
    def handleNotification(self, cHandle, raw_data):
        self.handle = cHandle
        data = raw_data.decode("utf-8")
        data = data.replace('\r','')
        print(data)
        if str(data) == "open":
            print("OPEN!")
            return True
        elif str(data) == "closed":
            print("CLOSED!")
            return False
        #self.data = struct.unpack("!b",data)
        #p.writeCharacteristic(cHandle, struct.pack('i',1), False)

#p = btle.Peripheral("10:21:3e:59:f0:c1")
#p.setDelegate(bleDelegate(0))

class Bluetooth:
    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.chime = btle.Peripheral(self.mac)
        self.handle = 0x01
        #self.handle = self.chime.getHandle()
        self.delegate = bleDelegate()
        self.chime.withDelegate(self.delegate)
        self.response = False
        self.status = True

    def send_data(self, data):
        self.chime.writeCharacteristic(self.delegate.handle, struct.pack("!s", data.encode('ascii')), False)
        #return response

    def read_wait(self, wait_s):
        self.chime.waitForNotifications(wait_s)
        #return self.delegate.data
    #def read(self):
    #    temp = self.chime.readCharacteristic(self.handle)
    #    self.delegate.data = struct.unpack("c", temp)
        


if __name__ == '__main__':
    main()

