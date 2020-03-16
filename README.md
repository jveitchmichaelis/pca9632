# PCA9632 Driver

![coverage](coverage.svg)

## Introduction

This Python package provides a platform agnostic driver for the [NXP PCA9632](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/4-bit-fm-plus-ic-bus-low-power-led-driver:PCA9632) led controller.

The PCA9632 is a 4-bit led controller with 8-bit PWM support, as well as blink modes. It can source quite a lot of current (400mA) and is simple to set up. It's specifically designed for RGBA (red/green/blue/amber) LEDs, but works well for providing easy dimmable control over 4 leds for indication purposes.

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

## Test suite

This package has a reasonably comprehensive test suite which you can use to check that commands are being recieved and interpreted properly. You need `pytest`. Run with:

```
python -m pytest test
```

you should see connected LEDs illuminate, as well as a check of all brightness levels for each LED. Functionality is verified by checking register settings.
