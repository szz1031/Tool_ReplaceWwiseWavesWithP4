import sys
import os
import stat
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QLabel, QLineEdit, QCheckBox, QFrame, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QFont
from szz_wwiseManager import WwiseManager
from szz_p4Manager import p4Manager

class P4ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(P4ConfigDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("P4V Settings")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)

        self.p4_server_label = QLabel("Server & Port ：")
        layout.addWidget(self.p4_server_label)

        self.p4_server_input = QLineEdit()
        layout.addWidget(self.p4_server_input)

        self.p4_username_label = QLabel("User ：")
        layout.addWidget(self.p4_username_label)

        self.p4_username_input = QLineEdit()
        layout.addWidget(self.p4_username_input)

        self.p4_password_label = QLabel("Password ：")
        layout.addWidget(self.p4_password_label)

        self.p4_password_input = QLineEdit()
        layout.addWidget(self.p4_password_input)

        self.p4_workspace_label = QLabel("WorkSpace：")
        layout.addWidget(self.p4_workspace_label)

        self.p4_workspace_input = QLineEdit()
        layout.addWidget(self.p4_workspace_input)

        self.confirm_button = QPushButton("Confirm")
        layout.addWidget(self.confirm_button)

        self.confirm_button.clicked.connect(self.accept)
        # 从文件中读取配置信息
        config = self.read_config_from_file()

        # 将配置信息设置为 QLineEdit 部件的文本
        self.p4_server_input.setText(config.get("p4_server", ""))
        self.p4_username_input.setText(config.get("p4_username", ""))
        self.p4_password_input.setText(config.get("p4_password", ""))
        self.p4_workspace_input.setText(config.get("p4_workspace", ""))

        if parent:
            self.move(parent.geometry().center() - self.rect().center())

    def read_config_from_file(self):
        config = {}
        try:
            with open("p4_config.txt", "r") as f:
                for line in f.readlines():
                    key, value = line.strip().split("=")
                    config[key] = value
        except FileNotFoundError:
            pass  # 文件不存在时，不执行任何操作
        return config


    def accept(self):
        p4_server = self.p4_server_input.text()
        p4_username = self.p4_username_input.text()
        p4_password = self.p4_password_input.text()
        p4_workspace = self.p4_workspace_input.text()

        # 将配置信息保存到文件
        self.save_config_to_file(p4_server, p4_username, p4_password, p4_workspace)

        super(P4ConfigDialog, self).accept()
    
    def save_config_to_file(self, p4_server, p4_username, p4_password, p4_workspace):
        with open("p4_config.txt", "w") as f:
            f.write(f"p4_server={p4_server}\n")
            f.write(f"p4_username={p4_username}\n")
            f.write(f"p4_password={p4_password}\n")
            f.write(f"p4_workspace={p4_workspace}\n")

class GUI(QMainWindow):
    wwise = 0
    reaper = 0
    p4 = 0
    wwiseProjectPathRoot = ''
    path = ''
    useP4 = False

    def __init__(self):
        super(GUI, self).__init__()
        self.p4 = p4Manager()
        self.setWindowTitle("ReplaceWwiseWavesWithP4 @SZZ    Version: 2.2  2023.04.21")
        self.setGeometry(100, 100, 880, 600)
        self.setStyleSheet("""
        QWidget {
            background-color: #2B2B2B;
        }
        QLabel {
            color: #F0F0F0;
        }
        QLineEdit {
            color: #FFFFFF;  
            background-color: transparent;
            border: 1px solid #5A5A5A;
        }
        QPushButton {
            font-family: "微软雅黑";
            background-color: #464646;
            color: #F0F0F0;
            border: 1px solid #5A5A5A;
            padding: 4px;
        }
        QPushButton:hover {
            background-color: #5A5A5A;
        }
        QPushButton:pressed {
            background-color: #787878;
        }
        QTextEdit {
            background-color: #3A3A3A;
            color: #F0F0F0;
            border: 1px solid #5A5A5A;
        }
        QCheckBox {
            color: #F0F0F0;
        }
        """)
        self.initUI()
        #self.connectWwise()
        self.load_p4_config()

    def load_p4_config(self):
        config_file = "p4_config.txt"
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                lines = f.readlines()
                p4_server = lines[0].strip().split("=")[-1]
                p4_username = lines[1].strip().split("=")[-1]
                p4_password = lines[2].strip().split("=")[-1]
                p4_workspace = lines[3].strip().split("=")[-1]

                # Update p4Manager instance with loaded configuration
                self.p4 = p4Manager()
                self.p4.p4client.port = p4_server
                self.p4.p4client.user = p4_username
                self.p4.psw = p4_password
                self.p4.p4client.client = p4_workspace

    def show_p4_config_dialog(self):
        dialog = P4ConfigDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            p4_server = dialog.p4_server_input.text()
            p4_username = dialog.p4_username_input.text()
            p4_password = dialog.p4_password_input.text()
            p4_workspace = dialog.p4_workspace_input.text()

            self.p4.update_p4_config(p4_server, p4_username, p4_password, p4_workspace)
            self.check1.setChecked(1)
            self.updateP4Usage()
    


    def initUI(self):
        
        # Font
        bold_font = QFont()
        bold_font.setBold(True)
        bold_font.setPointSize(13)

        font2 = QFont()
        font2.setPointSize(8)
        
        button0 = QPushButton("Connect Wwise", self)
        button0.clicked.connect(self.connectWwise)
        button0.setGeometry(15, 75, 110, 30)

        self.wwise_status_label = QLabel("Status: Not connected", self)
        self.wwise_status_label.setFont(font2)
        self.wwise_status_label.setGeometry(0, 115, 140, 25)
        self.wwise_status_label.setAlignment(Qt.AlignCenter)

        label = QLabel("Waapi Port :", self)
        label.setGeometry(8, 35, 70, 20)

        self.entry = QLineEdit("8070", self)
        self.entry.setGeometry(90, 35, 35, 20)

        button1 = QPushButton("2. Import To Wwise", self)
        button1.setFont(bold_font)
        button1.clicked.connect(self.Process)
        button1.setGeometry(500, 65, 190, 50)

        self.check1 = QCheckBox("Auto Checkout", self)
        self.check1.stateChanged.connect(self.updateP4Usage)
        self.check1.setGeometry(540, 118, 120, 30)

        self.labelFolder = QLabel("Please select a folder...", self)
        self.labelFolder.setWordWrap(True)  # 允许自动换行
        self.labelFolder.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        self.labelFolder.setGeometry(180, 10, 260, 60)

        buttonFolder = QPushButton("1. Select Folder", self)
        buttonFolder.setFont(bold_font)
        buttonFolder.clicked.connect(self.UpdatePath)
        buttonFolder.setGeometry(180, 65, 150, 50)

        buttonFolder2 = QPushButton("Open Folder", self)
        buttonFolder2.clicked.connect(self.OpenPath)
        buttonFolder2.setGeometry(340, 65, 100, 50)

        self.logtext = QTextEdit(self)
        self.logtext.setReadOnly(True)
        self.logtext.setGeometry(10, 150, 860, 430)
        
        # 添加分割线
        self.line1 = QFrame(self)
        self.line1.setStyleSheet("background-color: #787878")
        self.line1.setGeometry(QRect(135, 15, 2, 130))
        self.line1.setFrameShape(QFrame.VLine)
        self.line1.setFrameShadow(QFrame.Sunken)

        self.line2 = QFrame(self)
        self.line2.setStyleSheet("background-color: #787878")
        self.line2.setGeometry(QRect(470, 15, 2, 130))
        self.line2.setFrameShape(QFrame.VLine)
        self.line2.setFrameShadow(QFrame.Sunken)

        self.line3 = QFrame(self)
        self.line3.setStyleSheet("background-color: #787878")
        self.line3.setGeometry(QRect(720, 15, 2, 130))
        self.line3.setFrameShape(QFrame.VLine)
        self.line3.setFrameShadow(QFrame.Sunken)

        self.config_p4_button = QPushButton("Configure P4 account", self)
        self.config_p4_button.setGeometry(730, 75, 140, 30)
        self.config_p4_button.clicked.connect(self.show_p4_config_dialog)
        
    def PrintLog(self, string):
        self.logtext.append(string + '\n')
        self.logtext.ensureCursorVisible()
        QApplication.processEvents()
        

    def connectWwise(self):
        self.PrintLog("")
        self.PrintLog("... Connect Wwise with WAMP Port: "+self.entry.text()+" ...")
        try:
            self.wwise=WwiseManager(self.entry.text())
            self.wwiseProjectPathRoot=self.wwise.WwiseProjectPathRoot
        except:
            self.PrintLog("<<< Failed to connect to Wwise, please open Wwise or check Wwise WAMP port settings >>>")
            self.wwise_status_label.setText("Status: Failed")
            self.wwise_status_label.setStyleSheet("color: red;")
            return
        if self.wwise and self.wwiseProjectPathRoot:
            self.wwise_status_label.setText("Status: Connected")
            self.PrintLog("    Connect To Wwise Project："+self.wwiseProjectPathRoot)
            self.PrintLog("=== 连接Wwise成功! ===")
            self.wwise_status_label.setStyleSheet("color: green;")
        else:
            self.PrintLog("<<< Failed to connect to Wwise, please open Wwise or check Wwise WAMP port settings >>>")
            self.wwise_status_label.setText("Status: Failed")
            self.wwise_status_label.setStyleSheet("color: red;")
      
    def showP4config(self):
        '''
        显示P4环境信息
        '''
        p4=self.p4
        self.PrintLog(" --- P4 Server："+p4.p4client.port)
        self.PrintLog(" --- P4 User："+p4.p4client.user)
        self.PrintLog(" --- P4 Password："+p4.psw)
        self.PrintLog(" --- P4 WorkSpace："+p4.p4client.client)
        
    
    def UpdatePath(self):
        _path=QFileDialog.getExistingDirectory(self, "Please select a folder", os.path.expanduser("~"))
        if _path:
            self.path = _path
            self.labelFolder.setText(self.path)
            
            self.PrintLog("")
            self.PrintLog("Select Folder: " + self.path)
            
            #self.PrintLog ("Get Directory: "+ self.path)
            _count=0
            for file,root in self.findallfiles(self.path):
                fname,ext=os.path.splitext(file)
                if ext!=".wav":
                    continue
                _count+=1
            self.PrintLog("    There are a total of "+str(_count)+" wave files to be imported")
            
        
    def OpenPath(self):
        if self.path!='':
            os.startfile(self.path)
        
    def findallfiles(self,path):                     # 遍历文件夹的generator，包括子文件夹，返回（文件名，文件地址）
        for root,dirs,files in os.walk(path):
            for file in files:            
                yield file,root                 
    
    def test(self):
        if not self.wwise:
            self.connectWwise()
        self.wwise.getSelectedWwiseObjects()
        self.PrintLog(self.wwise._lastSelectedObject['id'])
        self.PrintLog(self.wwise._lastSelectedObject['path'])
        return
    
    def updateP4Usage(self):
        self.useP4 = self.check1.isChecked()
        if self.useP4:
            #FIXME
            self.PrintLog("")
            self.PrintLog("... Try to connect with P4 using the following configuration ...")
            self.showP4config()
            try:
                self.p4.forceConnect()
                self.PrintLog("=== P4 login successful! Automatic Checkout is enabled ===")
            except:
                self.PrintLog("<<< Failed to login P4 >>>")
                self.check1.setChecked(False)
                self.PrintLog("=== CheckOut is disabled, please click 'Configure P4 account' to modify the configuration ===")
                return
            #self.PrintLog("P4功能已成功开启")

      
    def Process(self): 
        if (not self.wwise) or (not self.wwiseProjectPathRoot):
            self.PrintLog("<<< Please connect to Wwise first >>>")
            return
        if not self.path:
            self.PrintLog("<<< Please select the import folder first >>>")
            return
           
        self.PrintLog("")
        self.PrintLog("... Start batch processing ...")
        _originFolder=self.wwiseProjectPathRoot+"\Originals\SFX\\"

        self.PrintLog("    Target Path："+_originFolder)
        self.PrintLog("    Start processing wave files in turn...")
        _count=0
        _count1=0
        _count2=0
        for file,root in self.findallfiles(self.path):
            _fullname = os.path.join(root,file)
            _fullname = os.path.normpath(_fullname)  #去掉反斜杠
            filepath,fullname=os.path.split(_fullname)
            fname,ext=os.path.splitext(fullname)
            if ext!='.wav':
                continue
            
            _count+=1
            _oldFile=self.findFileInRoot(fname,_originFolder)
            if _oldFile:
                self.PrintLog("    *Replaced "+str("\Originals\\"+_oldFile.split("\Originals\\")[-1])+" ...")
                if self.replaceFile(_fullname,_oldFile):
                    _count1+=1
                #print("new="+_fullname)
                #print("old="+_oldFile)
            else:
                self.PrintLog("    *Skipped "+str(file)+"  reason: file not found in Wwise origin//")
                newpath = self.path+"/SkippedFiles/"
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                shutil.move(_fullname,newpath+fullname)
                _count2+=1
                

        self.PrintLog("")
        self.PrintLog("Batch processing completed! Among "+str(_count)+" files, "+str(_count1)+" files were perfectly replaced, and "+str(_count2)+" files were skipped.")
        if _count2>0:
            self.PrintLog("Skipped files are moved into the /SkippedFiles/ folder")

    
    def findFileInRoot(self,in_fname,in_root,in_ext=".wav"):
        '''
        返回找到的完整文件路径
        '''
        for file,root in self.findallfiles(in_root):
            _fullname = os.path.join(root,file)
            _fullname = os.path.normpath(_fullname)  #去掉反斜杠
            filepath,fullname=os.path.split(_fullname)
            fname,ext=os.path.splitext(fullname)
            if fname==in_fname and ext==in_ext:
                return _fullname
        return
    
    def replaceFile(self,in_newf,in_oldf):
        if self.useP4:
            try:
                p4=self.p4
                p4.checkout(in_oldf)
                self.PrintLog("        -- checkout succeeded")
                    
                try:
                    shutil.copy(in_newf,in_oldf)  # 替换相同的文件会抛出error
                except:
                    self.PrintLog("        ---- WARNING! There is no difference before and after this file is replaced")
                return True
            except:
                try:
                    self.PrintLog("        --！Checkout fails, automatically overwrite forcibly...")
                    os.chmod(in_oldf,stat.S_IWRITE)
                except:
                    self.PrintLog("        ----！File replacement failed, please check if the file is checkout by others： "+str(in_oldf))
                    return False
                else:
                    shutil.copy(in_newf,in_oldf)
                    self.PrintLog("        ----！The file was replaced successfully but not been checkout, please manually checkout later")
                    return False
        
        else:
            try:
                self.PrintLog("        --！Forcibly overwrite files without logging in to P4...")
                os.chmod(in_oldf,stat.S_IWRITE)
            except:
                self.PrintLog("        ----！File replacement failed, please check if the file is checkout by others： "+str(in_oldf))
                return False
            else:
                try:
                    shutil.copy(in_newf,in_oldf)  # 替换相同的文件会抛出error
                except:
                    self.PrintLog("        ---- WARNING! There is no difference before and after this file is replaced")
                self.PrintLog("        ----！The file was replaced successfully but not been checkout, please manually checkout later")
                return False
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())

