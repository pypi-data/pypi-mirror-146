#-*- coding:utf-8 -*-
import configparser as c
class InvalidBool(ValueError):
    pass
class readini():
    def __init__(self,inifile):
        self.ini = c.ConfigParser()
        self.ini.read(inifile)
    def read(self,sect,vl):
        self.myvl = self.ini.get('a','b')
        return self.myvl
    def getbool(self,sectb,bname):
        self.tb = self.read(sectb,bname)
        if (str(self.tb) == 'True'):
            self.rtb = True
        elif (str(self.tb) == 'False'):
            self.rtb = False
        else:
            try:
                self.rtb = self.ini[sectb].getboolean(str(bname))
            except:
                raise InvalidBool(str(tb))
        return self.rtb