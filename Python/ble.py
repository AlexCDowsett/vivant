from bluepy import btle
import struct

def main():
    #p = btle.Peripheral("10:21:3E:59:F0:C1")
    p = chimeBLE("10:21:3E:59:F0:C1", "jdy-23")
    #delegate = bleDelegate(0)
    #p.withDelegate(delegate)
    p.read_wait(10.0)
#        print("ASS")
    print("data = ", p.delegate.data)
    
    p.delegate.data = 'i'
    print("data = ", p.delegate.data)
    
    p.read_wait(10.0)
#        print("ASS")
    print("data = ", p.delegate.data)
    
    

class bleDelegate(object):
    def __init__(self, *args):
        #btle.DefaultDelegate.__init__(self)
        self.data = 's'

    def handleNotification(self,cHandle,data):
        print("Notfication recieved")
        #print(struct.unpack("c",data))
        self.data = struct.unpack("c",data)
        #p.writeCharacteristic(cHandle, struct.pack('i',1), False)

#p = btle.Peripheral("10:21:3e:59:f0:c1")
#p.setDelegate(bleDelegate(0))

class chimeBLE:
    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.chime = btle.Peripheral(self.mac)
        #get the handle characteristic from underlying GATT protocol
        self.handle = 0x01
        #self.handle = self.chime.getHandle()
        #self.chime = btle.Peripheral("10:21:3e:59:f0:c1")
        self.delegate = bleDelegate(0)
        self.chime.withDelegate(self.delegate)
        self.response = False
        self.status = True
    #def connect(self):

    def send_data(self, data):
        self.chime.writeCharacteristic(self.handle, struct.pack("i", data))
        #return response

    def read_wait(self, wait_s):
        self.chime.waitForNotifications(wait_s)
        #return self.delegate.data
    #def read(self):
    #    temp = self.chime.readCharacteristic(self.handle)
    #    self.delegate.data = struct.unpack("c", temp)
        


if __name__ == '__main__':
    main()

