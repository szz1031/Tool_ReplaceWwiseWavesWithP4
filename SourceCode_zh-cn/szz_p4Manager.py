from P4 import P4,P4Exception
from pprint import pprint

class p4Manager:
    workSpaceName=''
    psw=''

    def __init__(self) -> None:
        self.p4client = P4()
        self.workSpaceName=self.p4client.client
        self.psw=self.p4client.password
        print("P4Manager init")

    # 添加此方法以更新P4配置
    def update_p4_config(self, p4_server, p4_username, p4_password, p4_workspace):
        if self.p4client.connected():
            self.p4client.disconnect()
        self.p4client.port = p4_server
        self.p4client.user = p4_username
        self.p4client.password = p4_password
        self.psw=p4_password
        self.p4client.client = p4_workspace
        print("Update P4 Setting")

    def test(self):
        
        try:
            self.p4client.password = self.psw
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
        if self.p4client.connected():
            self.p4client.disconnect()
        if not self.p4client.connected():  # 检查客户端是否已经连接
            self.p4client.password = self.psw
            self.p4client.connect()
            self.p4client.run_login()
        
    
    #def disconnect(self):
    #    self.p4client.disconnect()
        
    def add(self,in_filePath):
        try:
            if not self.p4client.connected():
                self.p4client.password = self.psw
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
        if not self.p4client.connected():
            self.p4client.password = self.psw
            self.p4client.connect()
            self.p4client.run_login()
        self.p4client.run("edit",in_filePath)

        #self.p4client.disconnect()


new=p4Manager()
#new.test()