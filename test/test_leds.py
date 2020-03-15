from pca9632.controller import Controller, REG_MODE1, REG_PWM0, REG_PWM1, REG_PWM2, REG_PWM3
import pytest

@pytest.fixture
def led_controller():
    dev = Controller()

    yield dev

    dev.reset()
    dev.all_off()
    dev.power_off()

def test_reset(led_controller):
    dev = led_controller
    dev.reset()

def test_power_on(led_controller):
    dev = led_controller
    dev.power_on()
    assert dev._read(REG_MODE1) >> 4 & 1 == 0

def test_power_off(led_controller):
    dev = led_controller
    dev.power_off()
    assert dev._read(REG_MODE1) >> 4 & 1 == 1

def test_enable(led_controller):
    dev = led_controller
    for i in range(4):
        dev.led_enable(i)
        assert dev.led_enabled(i) == True

def test_disable(led_controller):
    dev = led_controller
    for i in range(4):
        dev.led_disable(i)
        assert dev.led_enabled(i) == False

def test_all_on(led_controller):
    dev = led_controller
    dev.all_on()
    
    assert dev._read(REG_PWM0) == 255
    assert dev._read(REG_PWM1) == 255
    assert dev._read(REG_PWM2) == 255
    assert dev._read(REG_PWM3) == 255

def test_all_off():
    dev = Controller() 
    dev.all_off()
    dev.power_off()

def test_full_range(led_controller):
    dev = led_controller

    for i in range(4):
        for v in range(256):
            dev.set_led(i, v)
            assert v == dev._read(REG_PWM0+i)
 
