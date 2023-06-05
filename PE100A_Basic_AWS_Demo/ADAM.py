from ModbusDevice import ModbusDevice

class ADAM:
    
    CHANNELS=0
    debug=True
    module_hex = 0x0000
    module_string = "ADAM-xxx"
    typecodes = {"0x0000":"Invalid"}
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
        self.dev = ModbusDevice(1)
        
    # Helper functions for module info
    def module_name(self): return self.module_string
    
    def convert_uint(self,value,vmin,vmax):
        value = int(value)
        if(value>65536): value=65536
        if(value<0): value=0
        
        # Value is now 0-65536
        
        # Turn this in to a float from 0.0-1.0
        f = (float(value)/65535.0)
        if(f>1.0): f=1.0;
        if(f<0.0): f=0.0;
        
        vrange = abs(vmin)+vmax;
        
        f = (vrange*f)+vmin
        #print(f)
        return f
    

    # Device connect and close functions
    def connect(self):
        try:
            return self.dev.connectIP(self.ip,self.port);
        except: pass
        return False
    def close(self):
        if(self.dev.connected()):
            self.dev.close()

    # Read the module info register and confirm it matches
    def confirm_device(self):
        if(self.dev.connected()==False):
            self.debug("Device not connected")
            return False
        v = self.dev.read_register_04(210);
        if(v==self.module_hex): return True
        return False
        
    # Read the live channel data as float
    def read_channel_float(self,ch):
        if(self.dev.connected()==False):
            self.debug("Device not connected")
            return 0.0
        if(ch>=self.CHANNELS):
            self.debug("Invalid channel %d > %d" % (ch,self.CHANNELS-1))
            return 0.0
        f = self.dev.read_float(ch)
        return f
        
    # Read the live channel data as an unsigned integer
    # This is the default format for modbus
    def read_channel(self,ch):
        if(self.dev.connected()==False):
            self.debug("Device not connected")
            return 0.0
        if(ch>=self.CHANNELS):
            self.debug("Invalid channel %d > %d" % (ch,self.CHANNELS-1))
            return 0.0
        i = self.dev.read_uint16(ch)
        return i

    def read_channel_typecode_string(self, ch):
        if(self.dev.connected()==False):
            self.debug("Device not connected")
            return "NotConnected"
        if(ch>=self.CHANNELS):
            self.debug("Invalid channel %d > %d" % (ch,self.CHANNELS-1))
            return "InvalidChannel"
            
        code = self.dev.read_register_04(200+ch)
        st = ("0x%04X" % code)
        #print(st)
        return self.typecode_str(st)

    def write_channel_typecode(self, ch, code):
        if(self.dev.connected()==False):
            self.debug("Device not connected")
            return "NotConnected"
        if(ch>=self.CHANNELS):
            self.debug("Invalid channel %d > %d" % (ch,self.CHANNELS-1))
            return "InvalidChannel"

        try:
            code = self.dev.write_register_06(200+ch,int(code))
            return True;
        except: pass
        return False
        
    # Private functions
    def debug(self,msg):
        if(self.debug): print(msg)
    def typecode_str(self,key):
        if key in self.typecodes:
            return self.typecodes[key]
        return "Not Found"
        
        
class ADAM6017(ADAM):
    
    CHANNELS=8
    debug=True
    module_hex = 0x6017
    module_string = "ADAM-6017"
    typecodes = {"0x0103":"+-150 mV",
    "0x0104":"+-500 mV",
    "0x0105":"0~150 mV",
    "0x0106":"0~500 mV",
    "0x0140":"+-1 V",
    "0x0142":"+-5 V",
    "0x0143":"+-10 V",
    "0x0145":"0~1 V",
    "0x0147":"0~5 V",
    "0x0148":"0~10 V",
    "0x0181":"+-20 mA",
    "0x0180":"4~20 mA",
    "0x0182":"0~20 mA"}
    
class ADAM6015(ADAM):
    
    CHANNELS=7
    debug=True
    module_hex = 0x6015
    module_string = "ADAM-6015"
    typecodes = {"0x03A4":"PT100(385) -50~150ºC",
    "0x03A5":"PT100(385) 0~100ºC",
    "0x03A6":"PT100(385) 0~200ºC",
    "0x03A7":"PT100(385) 0~400ºC",
    "0x03A2":"PT100(385) -200~200ºC",
    "0x03C4":"PT100(392) -50~150ºC",
    "0x03C5":"PT100(392) 0~100ºC",
    "0x03C6":"PT100(392) 0~200ºC",
    "0x03C7":"PT100(392) 0~400ºC",
    "0x03C2":"PT100(392) -200~200ºC",
    "0x03E2":"PT1000 -40~160ºC",
    "0x0300":"Balco500 -30~120ºC",
    "0x0320":"NI604(518) -80~100ºC",
    "0x0321":"NI604(518) 0~100ºC"}
    
