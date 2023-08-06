
# Hardware Tester v.0.3-beta

## Prerequisites

If on RPi, `pip install teramesh-hardware-tester[rpi]`, otherwise `pip install teramesh-hardware-tester`.

If NOT on RPi, skip `-x test_relays`.

## List tests

    teramesh-hardware-test --no-tests-execute

## Run all tests on USB1

    teramesh-hardware-test -p /dev/ttyUSB1

## Run ONLY test_comms on USB1

    teramesh-hardware-test -p /dev/ttyUSB1 -i test_comms

## Run everything EXCEPT test_buzz on USB1

    teramesh-hardware-test -p /dev/ttyUSB1 -x test_buzz

# Hardware Configurer

Used to set mesh config via CLI:

    $ teramesh-configure --help
    Usage: teramesh-configure [OPTIONS]

    Options:
      -p, --port TEXT                 USB port to open serial to.  [required]
      -b, --baudrate INTEGER          Port baudrate.
      --router-ssid TEXT              [required]
      --router-password TEXT          [required]
      --router-bssid TEXT
      --mesh-id TEXT                  [required]
      --mesh-password TEXT            [required]
      --mesh-type TEXT                One of: idle, root, node, leaf, sta.
      --channel INTEGER               0 for auto or 1-13 for set channel.
      --channel-switch-disable / --no-channel-switch-disable
      --router-switch-disable / --no-router-switch-disable
      --mqtt-uri TEXT                 [required]
      --help                          Show this message and exit.
