from bluepy import btle
import struct

class MyDelegate(btle.DefaultDelegate):
    def __init__(self,params):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self,cHandle,data):
        print("handling notification...")
##        print(self)
##        print(cHandle)
        print(struct.unpack("b", data))

p = btle.Peripheral("10:21:3E:59:F0:C1")
p.setDelegate(MyDelegate(0))

while True:
    if p.waitForNotifications(10.0):
        print("ASS")
    print("waiting...")
