import time
import busio
import board
import adafruit_lidarlite

i2c = busio.I2C(board.SCL, board.SDA)

sensor = adafruit_lidarlite.LIDARLite(i2c, sensor_type=adafruit_lidarlite.TYPE_V3HP)

#while True:
#    try:
#        print(f"Sensor ID#: {sensor.unit_id}")
#        print(f"Distance = {sensor.distance}")
#        print(f"  Strength: {sensor.signal_strength}")
#    except RuntimeError as e:
#        print(e)
#    try:
#        print(f"Status: 0b{sensor.status:b}")
#        print(f"  Busy: {bool(sensor.status & adafruit_lidarlite.STATUS_BUSY_V3HP)}")
#        print(f"  Overflow: {bool(sensor.status & adafruit_lidarlite.STATUS_SIGNAL_OVERFLOW_V3HP)}")
#        print(f"  Health: 0b{sensor.health_status:b}")
#        print(f"  Power Control: 0b{sensor.power_control:b}")
#        print(f"  I2C Config: 0b{sensor.i2c_config:b}")
#        print(f"  Test Command: 0b{sensor.test_command:b}")
#        print(f"  Correlation: 0b{sensor.correlation_data}")
#    except RuntimeError as e:
#        print(e)

#    print()
#    time.sleep(1)

while True:
    try:
        print(f"{sensor.distance} {sensor.signal_strength}")
        time.sleep(.1)
    except RuntimeError as e:
        print(e)
