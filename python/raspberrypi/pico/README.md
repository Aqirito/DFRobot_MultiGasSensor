# DFRobot Multi-Gas Sensor Integration with Raspberry Pi Pico
This document provides a guide for integrating the DFRobot Multi-Gas Sensor with the Raspberry Pi Pico, leveraging the MicroPython examples and library provided in the python/raspberrypi/pico directory.

## 1. Introduction
The DFRobot Multi-Gas Sensor (SKU: DFR0784) is a versatile sensor capable of detecting various gases such as O2, CO, H2S, NO2, O3, CL2, NH3, H2, HCL, SO2, HF, and PH3, by simply switching the corresponding gas probes. It also supports high/low threshold alarms. <br>

The Raspberry Pi Pico is a low-cost, high-performance microcontroller board with flexible digital interfaces. This guide focuses on using the Multi-Gas Sensor with the Pico via the I2C communication protocol using MicroPython.

## 2. Compatibility and Communication
The `python/raspberrypi/pico` folder contains MicroPython-compatible code for interfacing the DFRobot Multi-Gas Sensor with the Raspberry Pi Pico.
- **Supported Board**: Raspberry Pi Pico W (and likely other Pico variants with I2C support).
- **Supported Python Version**: MicroPython v1.25.0 or later.
- **Communication Protocol**: I2C (UART is not supported in the provided MicroPython examples).

## 3. Hardware Setup and Installation
### 3.1 Wiring
Connect the DFRobot Multi-Gas Sensor to your Raspberry Pi Pico as follows (typical I2C connections):
- **VCC** to Pico's 3.3V (or 5V, depending on sensor's power input, typically 3.3V)
- **GND** to Pico's GND
- **SDA** to any available GPIO pin on the Pico (e.g., GP18)
- **SCL** to any available GPIO pin on the Pico (e.g., GP19)

(Note: The examples provided typically use GP18 for SDA and GP19 for SCL. Thanks to the use of `machine.SoftI2C`, you have the flexibility to choose virtually any available GPIO pins for SDA and SCL, allowing for custom wiring based on your project's needs. Ensure your wiring matches the pins specified in your `SoftI2C` initialization.)

### 3.2 MicroPython Firmware
Ensure your Raspberry Pi Pico is flashed with MicroPython firmware. If not, follow the official Raspberry Pi Pico MicroPython setup guide to install it.

### 3.3 Library Installation
Transfer the uDFRobot_MultigasSensor.py file from the python/raspberrypi/pico directory to your Raspberry Pi Pico's filesystem. This can typically be done using tools like Thonny IDE by saving the file to the Pico

`tree` Visualization: <br>
. <br>
└── boot.py <br>
└── main.py <br>
└── uDFRobot_MultiGasSensor.py

### 3.4 I2C Address Selection
The DFRobot Multi-Gas Sensor uses DIP switches (A0, A1) to select its I2C address. The default I2C address is 0x77. You can find the address mapping in the example headers:

|   A0   |  A1  | Address | Note |
| ------ | :--: | :-----: | ---- |
|   0    |  0   |   0x74  |      | 
|   0    |  1   |   0x75  |      | 
|   1    |  0   |   0x76  |      | 
|   1    |  1   |   0x77  |      | 

You can verify detected I2C addresses using the `I2C_BUS.scan()` method in the examples.

## 4. Usage Examples
The `python/raspberrypi/pico/examples` folder contains several scripts demonstrating various functionalities of the DFRobot Multi-Gas Sensor. You can transfer these example files to your Pico and run them to test the sensor.

### 4.1 Reading Gas Concentration (read_gas_concentration.py)
This example reads and prints the concentration of the gas detected by the sensor. It also enables temperature compensation for more accurate readings.

### 4.2 Reading Board Temperature (read_temp.py)
This example demonstrates how to read the onboard temperature of the multi-gas sensor.

### 4.3 Reading Voltage Data (read_volatage_data.py)
This script reads the raw voltage output from the sensor probe, which can be used for verification or custom calculations.

### 4.4 Proactive Report Mode (initiativereport.py)
This example configures the sensor to proactively report data without needing explicit requests from the Pico.

### 4.5 Setting Threshold Alarm (set_threshold_alarm.py)
This example demonstrates how to set a concentration threshold for the sensor. <br>
When the detected gas concentration exceeds this threshold, the sensor's ALA (Alarm) pin will output a high logic level.<br>
Connect the ALA pin on the sensor to a GPIO pin on your Pico (e.g., GP18 as suggested in the original Raspberry Pi example, but you'll need to adapt it for Pico's Pin object and how you read its state).

### 4.6 Changing I2C Address (change_sensor_iic_addr.py)
This utility script allows you to change the I2C address group of the sensor "programmatically" sort of tehehe. <br>
(Note) Don't forget to **reconnect** the sensor after changing the address otherwise the address still not changed.

## 5. Key Library Functions (uDFRobot_MultigasSensor.py)
The `uDFRobot_MultiGasSensor.py` library provides the following key methods for interacting with the sensor:
- `change_acquire_mode(mode)`: Changes the data acquisition mode (e.g., `gas.INITIATIVE` for proactive reporting or `gas.PASSIVITY` for request-based reporting).
- `read_gas_concentration()`: Reads the current gas concentration. Updates `gas.gastype`, `gas.gasconcentration`, and `gas.temp` properties.
- `read_temp()`: Reads the onboard temperature of the sensor.
- `read_volatage_data()`: Reads the raw analog voltage output from the gas. 
- `probe.set_threshold_alarm(switchof, threshold, gasType)`: Configures the alarm threshold for a specific gas type. switchof can be `gas.ON` or gas.OFF.set_temp_compensation(tempswitch): Enables or disables temperature compensation for gas concentration readings. tempswitch can be `gas.ON` or `gas.OFF`.
- `data_is_available()`: In proactive reporting mode, checks if new data is available from the sensor.
- `change_i2c_addr_group(group)`: Changes the I2C address group of the sensor.

## 6. Using Multiple Sensors on Shared I2C Pins
The I2C protocol allows multiple slave devices to share the same SDA and SCL lines, provided each device has a unique I2C address. The DFRobot Multi-Gas Sensor supports this by allowing you to set different I2C addresses using its **DIP switches (A0, A1)** and burn it via `change_i2c_addr_group()`. <br>

#### To use multiple DFRobot Multi-Gas Sensors with different I2C addresses on the same I2C bus (i.e., sharing the same SDA and SCL Pico pins):
1. **Assign Unique Addresses**: Physically set different I2C addresses for each sensor using the A0/A1 DIP switches and burn it using the `change_sensor_iic_addr.py` example to assign them.
2. **Initialize a Single `SoftI2C` Bus**: Create one `SoftI2C` object in your MicroPython code, specifying the common SDA and SCL pins.
3. **Create Separate Sensor Objects**: For each physical sensor, create a new `DFRobot_MultiGasSensor_I2C` instance, passing its unique I2C address and the same `SoftI2C` bus object.

## Example for Two Sensors (NO2 and CO) on shared I2C pins:
```python
import time
from uDFRobot_MultiGasSensor import *
from machine import SoftI2C, Pin

# Define the shared I2C pins
SDA_PIN = Pin(18)
SCL_PIN = Pin(19)

# Initialize a single SoftI2C bus instance
# All sensors will communicate over this same physical bus.
COMMON_I2C_BUS = SoftI2C(scl=SCL_PIN, sda=SDA_PIN)

print(f"Scanning I2C bus ({SCL_PIN.id},{SDA_PIN.id}): {[hex(addr) for addr in COMMON_I2C_BUS.scan()]}")

# Define unique I2C addresses for each sensor
# Ensure these addresses match your physical sensor's DIP switch settings.
ADDR_NO2_SENSOR = 0x74 # Example: Sensor 1 for NO2, with A0=0, A1=0
ADDR_CO_SENSOR = 0x76  # Example: Sensor 2 for CO, with A0=1, A1=0

# Create separate DFRobot_MultiGasSensor_I2C objects for each sensor
# Each object uses its unique address but shares the COMMON_I2C_BUS.
SENSOR_NO2 = DFRobot_MultiGasSensor_I2C(ADDR_NO2_SENSOR, COMMON_I2C_BUS)
SENSOR_CO = DFRobot_MultiGasSensor_I2C(ADDR_CO_SENSOR, COMMON_I2C_BUS)


def setup_sensors():
    # Configure NO2 sensor
    while False == SENSOR_NO2.change_acquire_mode(SENSOR_NO2.PASSIVITY):
        print("Waiting for NO2 sensor acquire mode change!")
        time.sleep(1)
    print("NO2 sensor acquire mode changed successfully!")
    SENSOR_NO2.set_temp_compensation(SENSOR_NO2.ON)
    time.sleep(0.5)

    # Configure CO sensor
    while False == SENSOR_CO.change_acquire_mode(SENSOR_CO.PASSIVITY):
        print("Waiting for CO sensor acquire mode change!")
        time.sleep(1)
    print("CO sensor acquire mode changed successfully!")
    SENSOR_CO.set_temp_compensation(SENSOR_CO.ON)
    time.sleep(0.5)

def main_loop():
    while True:
        # Read from NO2 sensor
        no2_concentration = SENSOR_NO2.read_gas_concentration()
        print(f"NO2 Sensor ({hex(ADDR_NO2_SENSOR)}): {SENSOR_NO2.gastype} concentration: {no2_concentration:.2f} {SENSOR_NO2.gasunits} | Temp: {SENSOR_NO2.temp:.1f}°C")

        # Read from CO sensor
        co_concentration = SENSOR_CO.read_gas_concentration()
        print(f"CO Sensor ({hex(ADDR_CO_SENSOR)}): {SENSOR_CO.gastype} concentration: {co_concentration:.2f} {SENSOR_CO.gasunits} | Temp: {SENSOR_CO.temp:.1f}°C")

        time.sleep(2) # Read every 2 seconds

if __name__ == "__main__":
    setup_sensors()
    main_loop()
```
This setup allows you to efficiently manage multiple DFRobot Multi-Gas Sensors on your Raspberry Pi Pico by sharing the I2C bus, provided each sensor has a distinct I2C address.

## 7. Troubleshooting and Notes

- **I2C Bus Scan**: Always use `I2C_BUS.scan()` to verify that your Pico can detect the sensor at its expected I2C address.
- **Root Permissions (Raspberry Pi OS)**: For full Raspberry Pi OS (not Pico), if you encounter permissions issues, you might need to run Python scripts with sudo. This is generally not required for MicroPython on Pico as you interact directly with the board's filesystem and interpreter.
- **Temperature Compensation**: The temperature compensation logic in the MicroPython library `(uDFRobot_MultiGasSensor.py)` has been noted to be a close replication of the C++ library. Ensure you enable it with `set_temp_compensation(gas.ON)` for more accurate readings.
- **Gas Type for Alarm**: When setting an alarm, ensure that the `gas.gastype` property has been populated by a prior call to `read_gas_concentration()` or is explicitly set if you know the probe type.
**Physical Connections**: Double-check all wiring, especially for I2C (SDA, SCL), power (VCC, GND), and the alarm pin if you're using that feature.

By following this guide, you should be able to successfully integrate your DFRobot Multi-Gas Sensor with a Raspberry Pi Pico for various gas detection applications.