from smbus2 import SMBus

PCA_AUTOINCREMENT_OFF = 0x00
PCA_AUTOINCREMENT_ALL = 0x80
PCA_AUTOINCREMENT_INDIVIDUAL = 0xA0
PCA_AUTOINCREMENT_CONTROL = 0xC0
PCA_AUTOINCREMENT_CONTROL_GLOBAL = 0xE0

REG_MODE1 = 0x00
REG_MODE2 = 0x01
REG_PWM0 = 0x02
REG_PWM1 = 0x03
REG_PWM2 = 0x04
REG_PWM3 = 0x05
REG_GRPPWM = 0x06
REG_GRPFREQ = 0x07
REG_LEDOUT = 0x08
REG_SUBADR1 = 0x09
REG_SUBADR2 = 0x0A
REG_SUBADR3 = 0x0B
REG_ALLCALL = 0x0C

AI2 = 7
AI1 = 6
AI0 = 5
SLEEP = 4
SUB1 = 3
SUB2 = 2
SUB3 = 1
ALLCALL = 0
DMBLNK = 5
INVRT = 4
OCH = 3
OUTDRV = 2

LDR3 = 6
LDR2 = 4
LDR1 = 2
LDR0 = 0

LED_MODE_OFF = 0x0
LED_MODE_ON = 0x1
LED_MODE_DIM = 0x2
LED_MODE_GROUP_DIM = 0x4

class Controller:
   
    def __init__(self, address=0x70, channel=1):
        self.i2c_channel = channel
        self.bus = SMBus(self.i2c_channel)
        self.address = address
        
        self.power_on()

        for i in range(4):
            self.led_enable(i)

    def reset(self):
        self.bus.write_byte_data(0x03, 0xA5, 0x5A) 

    def print_registers(self): 
        print("-- Registers -- ")
        self.print_byte_reg(REG_MODE1)
        self.print_byte_reg(REG_MODE2)
        self.print_byte_reg(REG_PWM0)
        self.print_byte_reg(REG_PWM1)
        self.print_byte_reg(REG_PWM2)
        self.print_byte_reg(REG_PWM3)
        self.print_byte_reg(REG_LEDOUT)
        self.print_byte_reg(REG_ALLCALL)
        
    def _read(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def led_enable(self, i):
        config = self._read(REG_LEDOUT)
        config |= (1 << 2*i)
        config |= (1 << 2*i+ 1)
        self.bus.write_byte_data(self.address, REG_LEDOUT, config)
    
    def led_disable(self, i):
        config = self._read(REG_LEDOUT)
        mode = LED_MODE_OFF
        config &= ~(1 << 2*i)
        config &= ~(1 << 2*i+1)
            
        self.bus.write_byte_data(self.address, REG_LEDOUT, config)

    def led_enabled(self, i):
        config = self._read(REG_LEDOUT)

        if (config >> 2*i) & 1 == 1 and (config >> (2*i+1)) & 1 == 1:
            return True

        return False

    def power_on(self):
        config = self._read(REG_MODE1)
        config &= ~(1 << SLEEP)
        self.bus.write_byte_data(self.address, REG_MODE1, config)

    def power_off(self):
        config = self._read(REG_MODE1)
        config |= (1 << SLEEP)
        self.bus.write_byte_data(self.address, REG_MODE1, config)

    def all_on(self):
        reg = PCA_AUTOINCREMENT_ALL | REG_PWM0
        val = [255,255,255,255]
        res = self.bus.write_i2c_block_data(self.address, reg, val)

    def all_off(self):
        reg = PCA_AUTOINCREMENT_ALL | REG_PWM0
        val = [0,0,0,0]
        res = self.bus.write_i2c_block_data(self.address, reg, val)

    def print_byte_reg(self, reg):
        print("{:08b}".format(self.bus.read_byte_data(self.address, reg)))

    def set_led(self, i=0, val=0):
        assert val <= 255 and val >= 0
        reg = PCA_AUTOINCREMENT_ALL | REG_PWM0 + i
        self.bus.write_byte_data(self.address, reg, val)

    def __del__(self):
        self.bus.close()
