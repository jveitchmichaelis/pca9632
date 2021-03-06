# PCA9632 Driver

![coverage](coverage.svg)

## Introduction

This Python package provides a platform agnostic driver for the [NXP PCA9632](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/4-bit-fm-plus-ic-bus-low-power-led-driver:PCA9632) led controller.

The PCA9632 is a 4-bit led controller with 8-bit PWM support, as well as blink modes. It can source quite a lot of current (25mA per pin) and is simple to set up. It's specifically designed for RGBA (red/green/blue/amber) LEDs, but works well for providing easy dimmable control over 4 leds for indication purposes.

The only dependency for this library is `smbus2` so provided your I2C device is addressable by that, this library should work (for example on a Raspberry Pi or other dev board).

## Examples

Per the chip documentation, you need to do the following to light up connected LEDs:

* Power on the oscillator (wake the chip)
* Enable the LEDs you want to control

Currently when you create a `Controller` object, the library will automatically power on the chip and enable all four LEDs. You can then set individual brightness like:

```
from pca9632.controller import Controller

c = Controller()

i = 0 # 0-3
brightness = 50 # 0:255

c.set_led(i, brightness)
```

the constructor support setting the I2C slave address (default is the all-call address `0x70`) and I2C channel (default 1). There are also modes to set all LEDs to full brightness (`c.all_on()` and `c.all_off()`), as well as a power-down mode `c.power_off()` to conserve power.

More sophisticated modes will be added shortly (for examples setting multiple LED values simultaneously, e.g. for RGB LEDs).

If you don't have permission to access I2C devices, you can use this guide to set up a [group](https://lexruee.ch/setting-i2c-permissions-for-non-root-users.html) to do so.

## Hardware notes

The chip itself is very easy to hook up (although it comes in a VSSOP package which can be challenging to solder if you've not had much experience with SMD soldering).

Note that the datasheet configuration is open-drain: connect the LEDs cathode (negative) to the chip and the anode (positive) to a maximum of 5V.

## Test suite

This package has a reasonably comprehensive test suite which you can use to check that commands are being recieved and interpreted properly. You need `pytest`. Run with:

```
python -m pytest test
```

you should see connected LEDs illuminate, as well as a check of all brightness levels for each LED. Functionality is verified by checking register settings.
