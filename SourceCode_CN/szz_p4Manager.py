from P4 import P4,P4Exception
from pprint import pprint

class p4Manager:
    workSpaceName=''
    
    def __init__(self) -> None:
        self.p4client = P4()
        self.workSpaceName=self.p4client.client
        #_password=self.p4client.user.lower()
        #print(self.p4client.password)#=_password
        
    def test(self):
        
        try:
            self.p4client.connect()
            self.p4client.run_login()
            info=self.p4client.run("info")
            pprint(info)

        except P4Exception:
            for e in self.p4client.errors:
                print(e)
            self.p4client.disconnect()
            return False
        
        self.p4client.disconnect()
        return True

    
    def forceConnect(self):
        self.p4client.connect()
        self.p4client.run_login()
        
        self.p4client.disconnect()
        
    
    #def disconnect(self):
    #    self.p4client.disconnect()
        
    def add(self,in_filePath):
        try:
            self.p4client.connect()
            self.p4client.run_login()
            self.p4client.run("add",in_filePath)
        except P4Exception:
            for e in self.p4client.errors:
                print(e)
            return False
        finally:
            self.p4client.disconnect()
            return True
        
        
    def checkout(self,in_filePath):
        self.p4client.connect()
        self.p4client.run_login()
        self.p4client.run("edit",in_filePath)

        self.p4client.disconnect()


#new=p4Manager()
#new.test()