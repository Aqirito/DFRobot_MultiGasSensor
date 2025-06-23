# -*- coding: utf-8 -*
"""
@file  read_gas_concentration.py
@brief Obtain gas concentration corresponding to the current environment, output as concentration value
@n Experimental mode: connect sensor communication pin to the main controller and burn
@n Experimental phenomenon: view the gas concentration corresponding to the current environment through serial port printing
@n Communication mode select, DIP switch SEL: 0: I2C, 1: UART
@n Group serial number         Address in the set
A0 A1 DIP level    00    01    10    11
@n 1            0x60  0x61  0x62  0x63
@n 2            0x64  0x65  0x66  0x67
@n 3            0x68  0x69  0x6A  0x6B
@n 4            0x6C  0x6D  0x6E  0x6F
@n 5            0x70  0x71  0x72  0x73
@n 6 (Default address group) 0x74  0x75  0x76  0x77 (Default address)
@n 7            0x78  0x79  0x7A  0x7B
@n 8            0x7C  0x7D  0x7E  0x7F
@n I2C address select, default to 0x77, A1 and A0 are grouped into 4 I2C addresses.
@n             | A0 | A1 |
@n             | 0  | 0  |    0x74
@n             | 0  | 1  |    0x75
@n             | 1  | 0  |    0x76
@n             | 1  | 1  |    0x77   default i2c address
@copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
@license     The MIT License (MIT)
@author      PengKaixing(kaixing.peng@dfrobot.com)
@version     V2.0
@date        2021-03-28
@url         https://github.com/DFRobot/DFRobot_MultiGasSensor
"""
import time

from uDFRobot_MultiGasSensor import *

"""
  ctype=1:UART
  ctype=0:IIC
"""
ctype = 0

if ctype == 0:

    # I2C Device address, which can be changed by changing A1 and A0, You can change the address using change_sensor_iic_addr.py
    # Add more address if more sensors
    # Replace with your actual sensor addresses:
    ADDR_NO2 = 0x74
    ADDR_CO = 0x76

    # Add more if more than one I2C ports
    I2C_CO_NO2 = SoftI2C(scl=Pin(19), sda=Pin(18))
    print(
        "I2C_CO_NO2 Addresses: {}".format([hex(addr) for addr in I2C_CO_NO2.scan()])
    )  # Scan detected addresses in hex

    SENSOR_NO2 = DFRobot_MultiGasSensor_I2C(ADDR_NO2, I2C_CO_NO2)
    SENSOR_CO = DFRobot_MultiGasSensor_I2C(ADDR_CO, I2C_CO_NO2)

else:
    gas = DFRobot_MultiGasSensor_UART(9600)


def setup():
    # Mode of obtaining data: the main controller needs to request the sensor for data
    while False == SENSOR_NO2.change_acquire_mode(SENSOR_NO2.PASSIVITY):
        print("wait acquire mode change for NO2")
        time.sleep(1)
    print("change acquire mode success for NO2")
    SENSOR_NO2.set_temp_compensation(SENSOR_NO2.ON)
    time.sleep(1)

    while False == SENSOR_CO.change_acquire_mode(SENSOR_CO.PASSIVITY):
        print("wait acquire mode change for CO")
        time.sleep(1)
    print("change acquire mode success for CO")
    SENSOR_CO.set_temp_compensation(SENSOR_CO.ON)
    time.sleep(1)


def loop():
    # Gastype is set while reading the gas level. Must first perform a read before
    # attempting to use it.
    SENSOR_NO2_CONN = SENSOR_NO2.read_gas_concentration()
    print("Gas type " + SENSOR_NO2.gastype + " concentration: %.2f " % SENSOR_NO2_CONN)

    SENSOR_CO_CONN = SENSOR_CO.read_gas_concentration()
    print("Gas type " + SENSOR_CO.gastype + " concentration: %.2f " % SENSOR_CO_CONN)
    time.sleep(1)


if __name__ == "__main__":
    setup()
    while True:
        loop()
