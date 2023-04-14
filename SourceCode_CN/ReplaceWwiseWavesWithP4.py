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
        self.setWindowTitle("配置 P4 账号信息")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)

        self.p4_server_label = QLabel("P4服务器地址及端口：")
        layout.addWidget(self.p4_server_label)

        self.p4_server_input = QLineEdit()
        layout.addWidget(self.p4_server_input)

        self.p4_username_label = QLabel("P4账号：")
        layout.addWidget(self.p4_username_label)

        self.p4_username_input = QLineEdit()
        layout.addWidget(self.p4_username_input)

        self.p4_password_label = QLabel("P4密码：")
        layout.addWidget(self.p4_password_label)

        self.p4_password_input = QLineEdit()
        layout.addWidget(self.p4_password_input)

        self.p4_workspace_label = QLabel("P4 WorkSpace：")
        layout.addWidget(self.p4_workspace_label)

        self.p4_workspace_input = QLineEdit()
        layout.addWidget(self.p4_workspace_input)

        self.confirm_button = QPushButton("确认")
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
    p4 = p4Manager()
    wwise = 0
    reaper = 0
    p4 = 0
    wwiseProjectPathRoot = ''
    path = ''
    useP4 = False

    def __init__(self):
        super(GUI, self).__init__()
        self.p4 = p4Manager()
        self.setWindowTitle("ReplaceWwiseWavesWithP4 @SZZ    Version: 2.0  2023.04.14")
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
        self.connectWwise()

    def show_p4_config_dialog(self):
        dialog = P4ConfigDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            p4_server = dialog.p4_server_input.text()
            p4_username = dialog.p4_username_input.text()
            p4_password = dialog.p4_password_input.text()
            p4_workspace = dialog.p4_workspace_input.text()


            # self.PrintLog("--- P4服务器地址及端口：{}".format(p4_server))
            # self.PrintLog("--- P4账号：{}".format(p4_username))
            # self.PrintLog("--- P4密码：{}".format(p4_password))
            # self.PrintLog("--- P4 WorkSpace：{}".format(p4_workspace))

            self.p4.update_p4_config(p4_server, p4_username, p4_password, p4_workspace)
            self.check1.setChecked(1)
            self.updateP4Usage()
    
    def initUI(self):
        
        # Font
        bold_font = QFont()
        bold_font.setBold(True)
        bold_font.setPointSize(13)
        
        button0 = QPushButton("连接到 Wwise", self)
        button0.clicked.connect(self.connectWwise)
        button0.setGeometry(15, 70, 110, 30)

        label = QLabel("Waapi Port :", self)
        label.setGeometry(8, 30, 70, 20)

        self.entry = QLineEdit("8070", self)
        self.entry.setGeometry(90, 30, 35, 20)

        button1 = QPushButton("2.自动导入Wwise", self)
        button1.setFont(bold_font)
        button1.clicked.connect(self.Process)
        button1.setGeometry(500, 40, 190, 50)

        #button99 = QPushButton("显示P4账号信息", self)
        #button99.clicked.connect(self.showP4config)
        #button99.setGeometry(750, 65, 100, 30)

        self.check1 = QCheckBox("同时自动Checkout", self)
        self.check1.stateChanged.connect(self.updateP4Usage)
        self.check1.setGeometry(540, 100, 120, 30)

        self.labelFolder = QLabel("请选择需要导入的文件夹...", self)
        self.labelFolder.setWordWrap(True)  # 允许自动换行
        self.labelFolder.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        self.labelFolder.setGeometry(180, 15, 260, 60)

        buttonFolder = QPushButton("1.选择文件夹", self)
        buttonFolder.setFont(bold_font)
        buttonFolder.clicked.connect(self.UpdatePath)
        buttonFolder.setGeometry(180, 90, 150, 50)

        buttonFolder2 = QPushButton("Open Folder", self)
        buttonFolder2.clicked.connect(self.OpenPath)
        buttonFolder2.setGeometry(340, 90, 100, 50)

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

        self.config_p4_button = QPushButton("配置P4账号信息", self)
        self.config_p4_button.setGeometry(750, 65, 100, 30)
        self.config_p4_button.clicked.connect(self.show_p4_config_dialog)
        
    def PrintLog(self, string):
        self.logtext.append(string + '\n')
        self.logtext.ensureCursorVisible()
        QApplication.processEvents()
        

    def connectWwise(self):
        self.PrintLog("")
        self.PrintLog("... 尝试使用"+self.entry.text()+"端口连接Wwise ...")
        try:
            self.wwise=WwiseManager(self.entry.text())
            self.wwiseProjectPathRoot=self.wwise.WwiseProjectPathRoot
        except:
            self.PrintLog("<<< 连接Wwise失败, 请打开Wwise或者检查Wwise WAMP端口设置 >>>")
            return
        if self.wwise and self.wwiseProjectPathRoot:
            self.PrintLog("    Wwise工程："+self.wwiseProjectPathRoot)
            self.PrintLog("=== 连接Wwise成功! ===")
        else:
            self.PrintLog("<<< 连接Wwise失败, 请打开Wwise或者检查Wwise WAMP端口设置 >>>")
      
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
        self.path = QFileDialog.getExistingDirectory(self, "请选择一个文件夹", os.path.expanduser("~"))
        if self.path:
            self.labelFolder.setText(self.path)
            
            self.PrintLog("")
            self.PrintLog("选中文件夹: " + self.path)
            
            #self.PrintLog ("Get Directory: "+ self.path)
            _count=0
            for file,root in self.findallfiles(self.path):
                fname,ext=os.path.splitext(file)
                if ext!=".wav":
                    continue
                _count+=1
            self.PrintLog("    总共有 "+str(_count)+" 个待导入wave文件")
            
        
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
            self.PrintLog("")
            self.PrintLog("... 尝试使用以下配置连接P4 ...")
            self.showP4config()
            try:
                self.p4.forceConnect()
                self.PrintLog("=== P4登录成功!自动Checkout已开启 ===")
            except:
                self.PrintLog("<<< 连接P4失败, 请检查P4设置 >>>")
                self.check1.setChecked(False)
                self.PrintLog("=== P4功能已禁用 ===")
                return
            #self.PrintLog("P4功能已成功开启")

      
    def Process(self): 
        if (not self.wwise) or (not self.wwiseProjectPathRoot):
            self.PrintLog("<<< 请先确保Wwise连接成功 >>>")
            return
        if not self.path:
            self.PrintLog("<<< 请先选择导入文件夹 >>>")
            return
           
        self.PrintLog("")
        self.PrintLog("... 开始批处理 ...")
        _originFolder=self.wwiseProjectPathRoot+"\Originals\SFX\\"

        self.PrintLog("    origin路径为："+_originFolder)
        self.PrintLog("    下面开始依次处理wave文件...")
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
                self.PrintLog("    *准备替换 "+str("\Originals\\"+_oldFile.split("\Originals\\")[-1])+" ...")
                if self.replaceFile(_fullname,_oldFile):
                    _count1+=1
                #print("new="+_fullname)
                #print("old="+_oldFile)
            else:
                self.PrintLog("    *跳过"+str(file)+": 在Origin内找不到同名文件!")
                newpath = self.path+"/SkippedFiles/"
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                shutil.move(_fullname,newpath+fullname)
                _count2+=1
                

        self.PrintLog("")
        self.PrintLog("批处理完成! "+str(_count)+"个文件中，完美替换了 "+str(_count1)+" 个文件，跳过了"+str(_count2)+"个文件。")
        if _count2>0:
            self.PrintLog("跳过的文件已整理到/SkippedFiles/文件夹中")

    
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
                self.PrintLog("        --Checkout成功")
                    
                try:
                    shutil.copy(in_newf,in_oldf)  # 替换相同的文件会抛出error
                except:
                    self.PrintLog("        ----警告!该文件替换前后无差别")
                return True
            except:
                try:
                    self.PrintLog("        --！Checkout失败，自动进行强行覆盖...")
                    os.chmod(in_oldf,stat.S_IWRITE)
                except:
                    self.PrintLog("        ----！文件替换失败，请检查文件是否被锁： "+str(in_oldf))
                    return False
                else:
                    shutil.copy(in_newf,in_oldf)
                    self.PrintLog("        ----！文件替换成功, 请稍后手动checkout")
                    return False
        
        else:
            try:
                self.PrintLog("        --！未登录P4，强行覆盖文件...")
                os.chmod(in_oldf,stat.S_IWRITE)
            except:
                self.PrintLog("        ----！文件替换失败，请检查文件是否被锁： "+str(in_oldf))
                return False
            else:
                try:
                    shutil.copy(in_newf,in_oldf)  # 替换相同的文件会抛出error
                except:
                    self.PrintLog("        ----警告!该文件替换前后无差别")
                self.PrintLog("        ----！强制替换成功, 请稍后手动进行版本控制")
                return False
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())

