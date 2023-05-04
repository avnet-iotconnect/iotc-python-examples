import struct

from pymodbus.exceptions import ModbusIOException
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient

class ModbusDevice():

    client = None
    device_address=1

    def __init__(self, addr):
        self.device_address = addr

    def addr(self,addr):
        self.device_address=addr

    def connectSerial(self, dev, baud, newparity='E'):
        self.dev = dev
        self.client = ModbusSerialClient(method='rtu', port=self.dev, timeout=1,baudrate=baud, parity=newparity)
        #self.client.stopbits = stopbits
        self.client.connect()
        return True

    def connectIP(self, ip, port):
        #print("Connecting to %s port %d" % (ip,port))
        self.client = ModbusTcpClient(host=ip, port=port, debug=True)
        if(self.client.connect()==False):
            self.client=None
        return True
        #print("Connection established")

    def connected(self):
        if(self.client==None): return False
        #return self.client.is_open
        return True

    def close(self): self.disconnect()

    def disconnect(self):
        if(self.client==None): return
        self.client.close()
        self.client=None

    # 16-bit reads
    # functions read_register_XX() do the heavy lifting and the other
    # functions are data formatters
    
    ''' Modbus function 04 '''
    def read_register_04(self, address):
        try:
            #print("Reading (dev %d)(code 04): %d"%(self.device_address,address))
            rr = self.client.read_input_registers(address, 1, unit=self.device_address)
            #print(rr)
            if(type(rr)==type(ModbusIOException())):
                print(rr)
                return -101
            if(rr.function_code!=4):
                print("function_code: %d" % rr.function_code)
                return -100
            return int(rr.registers[0])
        except Exception as e:
            print(e)
            return -1;
            
    ''' Modbus function 03 '''
    def read_register_03(self, address):
        try:
            #print("Reading (code 04): %d"%address)
            rr = self.client.read_holding_registers(address, 1, unit=self.device_address)
            #print(rr)
            if(type(rr)==type(ModbusIOException())):
                print(rr)
                return -101
            if(rr.function_code!=3):
                print("function_code: %d" % rr.function_code)
                return -100
            return int(rr.registers[0])
        except Exception as e:
            print(e)
            return -1;


            
    def read_uint16(self, address):
        return self.read_register_04(address)

    def read_int16(self, address):
        r = self.read_register_04(address)
        if(r>0x7FFF): r=r-0x10000;
        return r
        
    def read_int(self, address):
        r = self.read_int16(address)
        return r
        
    # 32-bit reads
    # function read_uint32() does the heavy lifting and the other
    # functions are data formatters
    def read_uint32(self, address):
        try:
            # Function code 4
            rr = self.client.read_input_registers(address, 2, unit=self.device_address)
            if(type(rr)==type(ModbusIOException())):
                print(rr)
                return -101
            if(rr.function_code!=4):
                print("function_code: %d" % rr.function_code)
                return -100
                
            val = int(rr.registers[0]);
            val <<= 16;
            val |= int(rr.registers[1])&0xFFFF;
            return val
        except Exception as e:
            print(e)
            return -1;

    def read_int32(self, address):
        r = self.read_register_04(address)
        if(r>0x7FFFFFFF): r=r-0x100000000;
        return r
        
    def read_float(self,address):
        # https://stackoverflow.com/questions/1592158/convert-hex-to-float
        # Get the unsigned int
        i = self.read_uint32(address)
        # Get the HEX string of the uint32
        st = ("%08X" % i)
        #print(st)
        # Parse the hex string as a floating point
        f = struct.unpack('!f', bytes.fromhex(st))[0]
        #print("%3.3f" % f)
        return f
    

    def read_registers_04(self, address, count):
        try:
            rr = self.client.read_holding_registers(address, count, unit=self.device_address)
            if(type(rr)==type(ModbusIOException())):
                print("Exception!")
                return -101
            if(rr.function_code!=4 and rr.function_code!=3):
                print("Func code is %d" % rr.function_code)
                return -100
            return rr.registers
        except Exception as e:
            print(e)
            return -1;
    def read_registers_03(self, address, count):
        try:
            rr = self.client.read_input_registers(address, count, unit=self.device_address)
            if(type(rr)==type(ModbusIOException())):
                print("Exception!")
                return -101
            if(rr.function_code!=4 and rr.function_code!=3):
                print("Func code is %d" % rr.function_code)
                return -100
            return rr.registers
        except Exception as e:
            print(e)
            return -1;
            
    # Block reads and writes
    ''' Modbus function 16 '''
    def write_registers_16(self, address, data):
        rr = self.client.write_registers(address, data, unit=self.device_address)
        if(type(rr)==type(ModbusIOException())): return -101
        #print(rr)
        if(rr.function_code!=16): return -100
        return 0
        
    ''' Modbus function 06 '''
    def write_register_06(self, address, data):
        rr = self.client.write_register(address, data, unit=self.device_address)
        if(type(rr)==type(ModbusIOException())): return -101
        #print(rr)
        if(rr.function_code!=6): return -100
        return 0
