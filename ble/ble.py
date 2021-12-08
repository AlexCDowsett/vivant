import bluepy import btle
import struct

class bleDelegate(object):
    def __init__(self) -> None:
        #btle.DefaultDelegate.__init__(self)
        self.data

    def handleNotification(self,cHandle,data):
        print("Notfication recieved")
        print(struct.unpack("c",data))
        self.data = struct.unpack("c",data)

#p = btle.Peripheral("10:21:3e:59:f0:c1")
#p.setDelegate(bleDelegate(0))

class chimeBLE:
    def __init__(self, mac, name):
        self.mac = mac
        self.macarray = mac.split(':')
        self.name = name
        self.chime = btle.Peripheral(self.mac)
        #get the handle characteristic from underlying GATT protocol
        self.handle = btle.getHandle()
        self.chime = btle.Peripheral(mac)
        self.delegate = bleDelegate()
        self.chime.withDelegate(self.delegate)
    
    #def connect(self):

    def send_data(self, data):
        response = self.device.writeCharacteristic(self.handle, struct('c', data), withResponse=True )
        return response

    def read_(self):
        self.chime.waitForNotifications(5.0)
        return self.delegate.data
