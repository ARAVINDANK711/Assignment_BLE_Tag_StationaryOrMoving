#Importing bluepy library to detect BLE tag signals

from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import time, struct

#Calculating the detected accelerometer value to find if the Beacon is moving or stationary

class CalculateAccelerometerValue(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def FindMovingOrStationary(self, cHandle, data):
        x, y, z = struct.unpack('3h', data)
        magnitude = (x ** 2 + y ** 2 + z ** 2) ** 0.5
        if magnitude > 1.0:
            print("The tag is moving")
        else:
            print("The tag is stationary")

#Adding 5 seconds for the bluetooth module to detect if any movement for BLE devices

scanner = Scanner()
devices = scanner.scan(5.0)

#connecting to the BLE tag to calculate the movement

for device in devices:
    
    if device.addr == 'AA:BB:CC:DD:EE:FF':
        tag = Peripheral(device)
        accelerometer_service = tag.getServiceByUUID('00000000-0000-0000-0000-000000000001')
        accelerometer_char = accelerometer_service.getCharacteristics('00000000-0000-0000-0000-000000000002')[0]
        tag.writeCharacteristic(accelerometer_char.getHandle() + 1, b'\x01\x00')
        tag.setDelegate(CalculateAccelerometerValue())

while True:
    if tag.waitForNotifications(1.0):
        continue

    print("Waiting...")
