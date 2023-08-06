lickport_array_interface_python
===============================

This Python package creates a class named LickportArrayInterface.

Authors::

    Peter Polidoro <peter@polidoro.io>

License::

    BSD

Example Usage::

    from lickport_array_interface import LickportArrayInterface
    dev = LickportArrayInterface() # Try to automatically detect port
    dev = LickportArrayInterface(port='/dev/ttyACM0') # Linux specific port
    dev = LickportArrayInterface(port='/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = LickportArrayInterface(port='COM3') # Windows specific port
    dev.start_acquiring_data()
    dev.start_saving_data()
    dev.stop_saving_data()
    dev.stop_acquiring_data()
