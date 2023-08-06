# YNCA

Automation Library for Yamaha receivers that support the YNCA protocol.

Supported receivers according to protocol documentation (not all tested) or logs found on the internet.
There might be more receivers that support this protocol. If you find some let met know so the list can be updated.

> RX-A700, RX-A710, RX-A800, RX-A810, RX-A840, RX-A850, RX-A1000, RX-A1010, RX-A1040, RX-A2000, RX-A2010, RX-A3000, RX-A3010, RX-V671, RX-V867, RX-V871, RX-V1067, RX-V2067, RX-V2600, RX-V3067


## Installation

```bash
python3 -m pip install ynca
```

## Usage

This package contains:

### Receiver

The Receiver class is the main interaction point for controlling the receiver.
It is exposing the YNCA API as defined in the specification.

### YNCA Console

The YNCA console provides an interactive console for YNCA commands intended for debugging. Examples on how to start below.

```
python3 -m ynca.connection /dev/ttyUSB0
python3 -m ynca.connection socket://192.168.178.21:50000
```

### YNCA Server

A very basic YNCA server intended for debugging and testing without connecting to a real device. Check the commandline help of `ynca_server.py` for more details.


## Example usage

```python
# Create a receiver class by specifying the port.
# Port could also be e.g. COM3 on Windows or any `serial_url` as supported by PySerial
# Like for example `socket://192.168.1.12:50000` for IP connection
receiver = Receiver("/dev/tty1")

# Initializing takes a while (multiple seconds) since it communicates
# quite a lot with the actual device to determine its capabilities.
# Later calls to the receiver and subunits are fast.
# Note that attributes that are still None after initialization are not supported by the subunits
receiver.initialize()

# Every subunit has a dedicated attribute on the `Receiver` class.
# The name is the subunit id as used in YNCA.
# The returned subunit class can be used to communicate with the subunit
sys = receiver.SYS
main = receiver.MAIN

print(sys.modelname) # Print the modelname of the system
print(main.name) # Print the name of the main zone

# `receiver.inputs` is a dictionary of available inputs with the key being
# the unique ID and the value the friendly name if available.
# Note that not all inputs might be available to all zones, but
# it is not possible to derive this from the API
for id, name in receiver.inputs.items():
    print(f"input {id}: {name}")

# To get notifications when something changes register callback with the subunit
# Note that callbacks are called from a different thread
# Also note that the callback should not block for too long.
def update_callback():
    print("Something was updated on the MAIN subunit")

main.register_update_callback(update_callback)

# Examples to control a zone
main.pwr = True
main.mute = Mute.off
main.input = "HDMI3"
main.volume = -50.5
main.volume_up()

# When done close the receiver for proper shutdown
receiver.close()
```
