import configparser
import os

# Custom dictionary class so we can add helper functions
# such as keyexists(key)
class CustomDictOne(dict):
    def __init__(self,*arg,**kw):
        super(CustomDictOne, self).__init__(*arg, **kw)

    def keyexists(self, key):
        return (key in self)
        #return True

class Config:

    def __init__(self):
        self.clear()

    # Load and clear functions
    def clear(self):
        self.dict = {}
        #self.dict = CustomDictOne()

    def load(self,infile):
        try:
            config = configparser.ConfigParser()
            if(os.path.exists(infile) == False):
                print("Error, file '%s' does not exist"%infile)
                return False
            config.read(infile)
            newD = {s:dict(config.items(s)) for s in config.sections()}
            #newD = {s:CustomDictOne(config.items(s)) for s in config.sections()}
            self.dict.update(newD)
            #print(newD)
            return True
        except:
            print("Error parsing config file '%s'"%infile)
            return False
            
    # GET functions
    def get(self,section,key):
        return self.get_str(section,key)

    def get_str(self,section,key):
        """
        # Custom dict implementation
        if(self.dict.keyexists(section)):
            if(self.dict[section].keyexists(key)):
                return str(self.dict[section][key])
        """

        # Normal dict implementation
        if(section in self.dict):
            if(key in self.dict[section]):
                return str(self.dict[section][key])

        return ""

    def get_int(self,section,key):
        if(section in self.dict):
            if(key in self.dict[section]):
                return int(self.dict[section][key]);
        return 0

    def get_num(self,section,key):
        if(section in self.dict):
            if(key in self.dict[section]):
                return float(self.dict[section][key]);
        return 0.0

    # Checking functions
    def isset(self,section,key=None):
        if(section in self.dict):
            if(key!=None):
                if(key in self.dict[section]):
                    return True
            else:
                return True
        return False

    def strempty(self,st):
        if(st==None): return True
        if(st==False): return True
        if(len(st)<=0): return True
        return False
