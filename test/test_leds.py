from pca9632.controller import Controller, REG_MODE1, REG_PWM0, REG_PWM1, REG_PWM2, REG_PWM3
import time

def test_reset():
    dev = Controller()
    dev.reset()

def test_power_on():
    dev = Controller()
    dev.power_on()
    assert dev._read(REG_MODE1) >> 4 & 1 == 0

def test_power_off():
    dev = Controller()
    dev.power_off()
    assert dev._read(REG_MODE1) >> 4 & 1 == 1

def test_enable():
    dev = Controller()
    for i in range(4):
        dev.led_enable(i)
        assert dev.led_enabled(i) == True

def test_disable():
    dev = Controller()
    for i in range(4):
        dev.led_disable(i)
        assert dev.led_enabled(i) == False

def test_all_on():
    dev = Controller()
    dev.power_on()
    dev.all_on()
    
    assert dev._read(REG_PWM0) == 255
    assert dev._read(REG_PWM1) == 255
    assert dev._read(REG_PWM2) == 255
    assert dev._read(REG_PWM3) == 255

    dev.all_off()
    dev.power_off()

def test_all_off():
    dev = Controller()
    dev.power_on()
    
    dev.all_off()
    dev.power_off()

def test_full_range():
    dev = Controller()
    dev.power_on()

    for i in range(4):
        for v in range(256):
            dev.set_led(i, v)
            assert v == dev._read(REG_PWM0+i)
 
    dev.all_off()
    dev.power_off()
