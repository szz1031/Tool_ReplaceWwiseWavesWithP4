import sys
import os
import stat
import shutil
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QLabel, QLineEdit, QCheckBox, QFrame, QVBoxLayout, QDialog, QAction
from PyQt5.QtCore import Qt,QRect,QUrl,QCoreApplication
from PyQt5.QtGui import QFont, QDesktopServices
from szz_wwiseManager import WwiseManager
from szz_p4Manager import p4Manager
from szz_reaperManager import reaperManager
import qdarkstyle

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

class LanguageImportDialog(QDialog):
    def __init__(self, parent=None):
        super(LanguageImportDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("多语言导入设置")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        self.checkboxes = []
        self.line_edits = []

        # 第一行，SFX 路径
        self.sfx_checkbox = QCheckBox("SFX")
        layout.addWidget(self.sfx_checkbox)
        self.checkboxes.append(self.sfx_checkbox)
        
        # 其他几行，让用户输入字符，例如 Chinese
        for i in range(4):
            checkbox = QCheckBox()
            line_edit = QLineEdit()
            layout.addWidget(checkbox)
            layout.addWidget(line_edit)
            self.checkboxes.append(checkbox)
            self.line_edits.append(line_edit)

        # 确认按钮
        self.confirm_button = QPushButton("确认")
        layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.accept)

        # 读取配置文件
        self.load_config_from_file()

        if parent:
            self.move(parent.geometry().center() - self.rect().center())

    def load_config_from_file(self):
        try:
            with open("language_import_config.txt", "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if i == 0:
                        checked, _ = line.strip().split(",")
                        self.checkboxes[i].setChecked(checked == "1")
                    else:
                        checked, text = line.strip().split(",")
                        self.checkboxes[i].setChecked(checked == "1")
                        self.line_edits[i-1].setText(text)
        except FileNotFoundError:
            pass  # 文件不存在时，不执行任何操作

    def save_config_to_file(self):
        with open("language_import_config.txt", "w") as f:
            for i, checkbox in enumerate(self.checkboxes):
                if i == 0:
                    f.write(f"{int(checkbox.isChecked())},\n")
                else:
                    line_edit = self.line_edits[i-1]
                    f.write(f"{int(checkbox.isChecked())},{line_edit.text()}\n")

    def accept(self):
        self.save_config_to_file()
        super(LanguageImportDialog, self).accept()

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
        
        self.initUI()
        #self.connectWwise()
        self.load_p4_config()

    def open_documentation(self):
        # 打开指定的网址
        QDesktopServices.openUrl(QUrl("https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4"))

    # P4

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

    def show_language_import_dialog(self):
        dialog = LanguageImportDialog(self)
        dialog.exec_()

    # Reaper
    def connectReaper(self):
        self.PrintLog("    正在连接Reaper...")
        self.reaper=reaperManager()
        print(self.reaper.projTitle)
        if self.reaper.connection:
            self.PrintLog("连接Reaper工程成功！ 连接到的工程为："+self.reaper.projTitle)
            self.PrintLog("Reaper工程地址为: "+self.reaper.projPath.split(self.reaper.projTitle)[0])
            self.PrintLog("")
            
        else:
            self.PrintLog("<<< 连接Reaper工程失败！ >>>")
            self.reaper = 0
        pass

    def RenderFromReaper(self): 
        self.connectReaper()
        if not self.reaper:
            self.PrintLog("<<< 请先确保Reaper连接成功 >>>")
            return
        
        self.PrintLog("开始导出到临时目录 ...")


        #print (_timeStomp)
        if not self.path:
            _timeStomp=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            #self.path=os.path.join(os.path.expanduser("~"), 'Desktop')+"\Reaper音效导出\\"+self.reaper.projTitle+"\\"+_timeStomp
            self.path=self.reaper.projPath.split(self.reaper.projTitle)[0]+"\\"+self.reaper.projTitle+"\\Output\\"+_timeStomp
            self.labelFolder.setText(self.path)
        

        self.reaper.SetReaperRenderSetting_Default(self.path)
        self.reaper.SetReaperRenderSetting_RenderName("$region")
        #self.reaper.openRenderSetting()
        self.reaper.renderWithCurrentSetting()
        self.PrintLog("导出已完成! 文件被导出到路径："+self.path)
        #print(self.tempOutpuPath)
        self.PrintLog("--- 点击‘在文件浏览器中打开’即可快速打开该地址。点击‘2’以继续 ---")
        self.PrintLog("")

    def initUI(self):
        self.setWindowTitle("ReplaceWwiseWavesWithP4 @SZZ    Version: 4.0  2024.08.29")
        self.setGeometry(100, 100, 880, 700)
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling) # 设置高DPI缩放
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
        QAction{
            font-family: "微软雅黑";
            background-color: #464646;
            color: #F0F0F0;            
        }
        QMenuBar{
            font-family: "微软雅黑";
            background-color: #2B2B2B;
            color: #F0F0F0;            
        }
        QMenu::item {
            background-color: #2B2B2B;
            color: #F0F0F0;
        }
        QMenu::item:hover {
            background-color: #5A5A5A !important;
            color: #F0F0F0;
        }
        """)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # Menu
        menu_bar = self.menuBar()

        menu_setting=menu_bar.addMenu("设置")
        action_p4setting = QAction("设置P4账号", self)
        action_p4setting.triggered.connect(self.show_p4_config_dialog)
        menu_setting.addAction(action_p4setting)
        
        action_language_import = QAction("多语言导入设置", self)
        action_language_import.triggered.connect(self.show_language_import_dialog)
        menu_setting.addAction(action_language_import)

        doc_menu = menu_bar.addMenu("说明文档")
        open_doc_action = QAction("GitHub主页", self)
        open_doc_action.triggered.connect(self.open_documentation)
        doc_menu.addAction(open_doc_action)

        # Font
        bold_font = QFont()
        bold_font.setBold(True)
        bold_font.setPointSize(13)

        font2 = QFont()
        font2.setPointSize(9)
        
        # button0 = QPushButton("连接到 Wwise", self)
        # button0.clicked.connect(self.connectWwise)
        # button0.setGeometry(15, 105, 110, 30)

        # self.wwise_status_label = QLabel("Wwise连接状态 : Not connected", self)
        # self.wwise_status_label.setFont(font2)
        # self.wwise_status_label.setGeometry(500, 40, 200, 25)
        # self.wwise_status_label.setAlignment(Qt.AlignCenter)

        label1 = QLabel("步骤1: 选择或者导出一个文件夹",self)
        label1.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        label1.setGeometry(20, 60, 260, 20)

        self.labelFolder = QLabel("待导入文件未选择...", self)
        self.labelFolder.setWordWrap(True)  # 允许自动换行
        self.labelFolder.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        self.labelFolder.setGeometry(320, 95, 260, 60)

        buttonFolder = QPushButton("1.选择文件夹", self)
        buttonFolder.setFont(bold_font)
        buttonFolder.clicked.connect(self.UpdatePath)
        buttonFolder.setGeometry(20, 95, 260, 50)

        buttonFolder = QPushButton("1.Reaper傻瓜导出", self)
        buttonFolder.setFont(bold_font)
        buttonFolder.clicked.connect(self.RenderFromReaper)
        buttonFolder.setGeometry(20, 165, 260, 50)

        buttonFolder2 = QPushButton("在文件浏览器中打开", self)
        buttonFolder2.setFont(bold_font)
        buttonFolder2.clicked.connect(self.OpenPath)
        buttonFolder2.setGeometry(350, 165, 200, 50)
        
        # wwise
        label1 = QLabel("步骤2: 将整批wave替换到Wwise内",self)
        label1.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        label1.setGeometry(600, 60, 260, 20)

        label = QLabel("Wwise 端口 :", self)
        label.setGeometry(660, 105, 90, 20)

        self.entry = QLineEdit("8080", self)
        self.entry.setGeometry(750, 105, 40, 20)

        self.check1 = QCheckBox("自动在P4中Checkout", self)
        self.check1.stateChanged.connect(self.updateP4Usage)
        self.check1.setGeometry(660, 125, 130, 30)

        button1 = QPushButton("2.自动导入Wwise", self)
        button1.setFont(bold_font)
        button1.clicked.connect(self.Process)
        button1.setGeometry(620, 165, 220, 50)


        # 添加分割线
        self.line1 = QFrame(self)
        self.line1.setStyleSheet("background-color: #787878")
        self.line1.setGeometry(QRect(300, 45, 2, 180))
        self.line1.setFrameShape(QFrame.VLine)
        self.line1.setFrameShadow(QFrame.Sunken)

        self.line2 = QFrame(self)
        self.line2.setStyleSheet("background-color: #787878")
        self.line2.setGeometry(QRect(600, 45, 2, 180))
        self.line2.setFrameShape(QFrame.VLine)
        self.line2.setFrameShadow(QFrame.Sunken)

        # self.line3 = QFrame(self)
        # self.line3.setStyleSheet("background-color: #787878")
        # self.line3.setGeometry(QRect(720, 45, 2, 180))
        # self.line3.setFrameShape(QFrame.VLine)
        # self.line3.setFrameShadow(QFrame.Sunken)

        # self.config_p4_button = QPushButton("配置P4账号信息", self)
        # self.config_p4_button.setGeometry(750, 105, 100, 30)
        # self.config_p4_button.clicked.connect(self.show_p4_config_dialog)
        
        self.logtext = QTextEdit(self)
        self.logtext.setReadOnly(True)
        self.logtext.setGeometry(10, 230, 860, 430)

    def PrintLog(self, string):
        self.logtext.append(string + '\n')
        self.logtext.ensureCursorVisible()  # 确保光标可见，滚动到最低端
        self.logtext.verticalScrollBar().setValue(self.logtext.verticalScrollBar().maximum())  # 确保滚动条在最低端
        QApplication.processEvents()  # 处理挂起的事件，确保界面更新
        

    def connectWwise(self):
        self.PrintLog("")
        self.PrintLog("... 尝试使用"+self.entry.text()+"端口连接Wwise ...")
        try:
            self.wwise=WwiseManager(self.entry.text())
            self.wwiseProjectPathRoot=self.wwise.WwiseProjectPathRoot
        except:
            self.PrintLog("<<< 连接Wwise失败, 请打开Wwise或者检查Wwise WAMP端口设置 >>>")
            # self.wwise_status_label.setText("Status: Failed")
            # self.wwise_status_label.setStyleSheet("color: red;")
            return
        if self.wwise and self.wwiseProjectPathRoot:
            #self.wwise_status_label.setText("Status: Connected")
            self.PrintLog("    Wwise工程："+self.wwiseProjectPathRoot)
            self.PrintLog("=== 连接Wwise成功! ===")
            #self.wwise_status_label.setStyleSheet("color: green;")
        else:
            self.PrintLog("<<< 连接Wwise失败, 请打开Wwise或者检查Wwise WAMP端口设置 >>>")
            # self.wwise_status_label.setText("Status: Failed")
            # self.wwise_status_label.setStyleSheet("color: red;")
      
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
        _path=QFileDialog.getExistingDirectory(self, "请选择一个文件夹", os.path.expanduser("~"))
        if _path:
            self.path = _path
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
            #FIXME
            self.PrintLog("")
            self.PrintLog("... 尝试使用以下配置连接P4 ...")
            self.showP4config()
            try:
                self.p4.forceConnect()
                self.PrintLog("=== P4登录成功!自动Checkout已开启 ===")
            except:
                self.PrintLog("<<< 连接P4失败 >>>")
                self.check1.setChecked(False)
                self.PrintLog("=== CheckOut已禁用，请在“设置-设置P4账号”配置正确的P4账号信息 ===")
                return
            #self.PrintLog("P4功能已成功开启")

            
    def load_language_import_config(self):
        language_paths = []
        try:
            with open("language_import_config.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    checked, lang = line.strip().split(",")
                    language_paths.append((checked == "1", lang))
        except FileNotFoundError:
            pass
        return language_paths
      
    def Process(self): 

        self.connectWwise()

        if (not self.wwise) or (not self.wwiseProjectPathRoot):
            self.PrintLog("<<< 请先确保Wwise连接成功再进行导入 >>>")
            return
        if not self.path:
            self.PrintLog("<<< 请先选择导入文件夹 >>>")
            return
           
        self.PrintLog("")
        self.PrintLog("... 开始批处理 ...")
        # 加载用户配置的语言路径
        language_paths = self.load_language_import_config()
        
        _count = 0
        _count1 = 0
        _count2 = 0
        
        for file, root in self.findallfiles(self.path):
            _fullname = os.path.join(root, file)
            _fullname = os.path.normpath(_fullname)  # 去掉反斜杠
            filepath, fullname = os.path.split(_fullname)
            fname, ext = os.path.splitext(fullname)
            if ext != '.wav':
                continue

            _count += 1
            found_and_replaced = False
            
            for i, (checked, lang) in enumerate(language_paths):
                if not checked:
                    continue

                if i == 0:  # 第一项代表 SFX 路径
                    _originFolder = self.wwiseProjectPathRoot + "\Originals\SFX\\"
                else:  # 其他项代表用户自定义的路径
                    _originFolder = self.wwiseProjectPathRoot + f"\Originals\Voices\{lang}\\"

                self.PrintLog(f"    检查路径：{_originFolder}")
                
                _oldFile = self.findFileInRoot(fname, _originFolder)
                if _oldFile:
                    self.PrintLog("    *替换 {} ...".format('\\Originals\\' + _oldFile.split('\\Originals\\')[-1]))
                    if self.replaceFile(_fullname, _oldFile):
                        _count1 += 1
                    found_and_replaced = True
                    break  # 一旦找到并替换了文件，跳出当前的路径循环

            if not found_and_replaced:
                self.PrintLog(f"    *跳过 {str(file)}: 在所有配置的路径中找不到同名文件!")
                newpath = os.path.join(self.path, "SkippedFiles")
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                shutil.move(_fullname, os.path.join(newpath, fullname))
                _count2 += 1

        self.PrintLog("")
        self.PrintLog(f"批处理完成! {str(_count)} 个文件中，成功替换了 {str(_count1)} 个文件，跳过了 {str(_count2)} 个文件。")
        if _count2 > 0:
            self.PrintLog("跳过的文件已整理到 /SkippedFiles/ 文件夹中")

    
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
                    self.PrintLog("        ----！替换成功, 请稍后手动checkout")
                    return False
        
        else:
            try:
                self.PrintLog("        --！未登录P4，直接覆盖文件...")
                os.chmod(in_oldf,stat.S_IWRITE)
            except:
                self.PrintLog("        ----！文件替换失败，请检查文件是否被锁： "+str(in_oldf))
                return False
            else:
                try:
                    shutil.copy(in_newf,in_oldf)  # 替换相同的文件会抛出error
                except:
                    self.PrintLog("        ----警告!该文件替换前后无差别")
                self.PrintLog("        ----！替换成功, 如有需要，请自行进行版本控制")
                return False
        
if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())

