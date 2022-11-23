import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog,Canvas
from szz_wwiseManager import WwiseManager
from szz_p4Manager import p4Manager
import os
import stat
import shutil



class GUI:
    wwise=0
    reaper=0
    wwiseProjectPathRoot=''
    path=''
    useP4=False
    
    def __init__(self):
        self.InitalMainWindow()
        

    def connectWwise(self):
        self.PrintLog("")
        self.PrintLog("    使用"+varPortID.get()+"端口连接Wwise...")
        try:
            self.wwise=WwiseManager(varPortID.get())
            self.wwiseProjectPathRoot=self.wwise.WwiseProjectPathRoot
        except:
            self.PrintLog("<<< 连接Wwise失败, 请打开Wwise或者检查Wwise WAMP端口设置 >>>")
            return
        if self.wwise and self.wwiseProjectPathRoot:
            self.PrintLog("    Wwise工程："+self.wwiseProjectPathRoot)
            self.PrintLog("连接Wwise成功! ")
        else:
            self.PrintLog("<<< 连接Wwise失败, 请打开Wwise或者检查Wwise WAMP端口设置 >>>")
      
    def showP4config(self):
        '''
        显示P4环境信息
        '''
        p4=p4Manager().p4client
        self.PrintLog(" --- P4 Server："+p4.port)
        self.PrintLog(" --- P4 User："+p4.user)
        self.PrintLog(" --- P4 Password："+p4.password)
        self.PrintLog(" --- P4 WorkSpace："+p4.client)
        self.PrintLog("")
        

    def InitalMainWindow(self,in_width="880",in_height="600",in_version="1.3",in_titleName="ReplaceWwiseWavesWithP4",in_autherName="SZZ",in_date="2022.11.23"): # 窗口布局
  
        window=tk.Tk()
        window.title(in_titleName+' @'+in_autherName+'    Version: '+in_version+'  '+in_date)
        window.geometry(in_width+'x'+in_height)
        f1 = tkFont.Font(family='microsoft yahei', size=11, weight='bold')
        f2 = tkFont.Font(family='times', size=11, slant='italic')

        # 布线
        canvas = Canvas(window,height=200,width=800)
        canvas.create_line(135, 15, 135, 140,dash=(4, 2))
        canvas.create_line(470, 15, 470, 140,dash=(4, 2))
        canvas.create_line(720, 15, 720, 140,dash=(4, 2))
        canvas.place(x=0,y=0)


        # 按钮
        button0=tk.Button(window,text="Connect Wwise",command=self.connectWwise)
        button0.place(x=15,y=65)

        global varPortID
        varPortID=tk.StringVar()
        varPortID.set("8070")
        entry=tk.Entry(window,textvariable=varPortID,width=4)
        entry.place(x=90,y=30)
        lable=tk.Label(window,text="Waapi Port :")
        lable.place(x=8,y=30)
        
        
        button1=tk.Button(window,text="2.批量替换wwise内wav",font=f1,command=self.Process)
        button1.place(x=500,y=50)

        button99=tk.Button(window,text="显示P4账号信息",command=self.showP4config)
        button99.place(x=750,y=30)
        global varInt
        varInt=tk.BooleanVar()
        varInt.set(1)
        check1=tk.Checkbutton(window,text="自动Checkout",variable=varInt,command=self.updateP4Usage)
        check1.place(x=745,y=70)

        
        button88=tk.Button(window,text="test",command=self.test)
        #button88.place(x=700,y=60)

        global varTextFolder
        varTextFolder=tk.StringVar()
        varTextFolder.set("Please select a folder")
        labelFolder=tk.Label(window,textvariable = varTextFolder,wraplength=260)
        labelFolder.place(x=150,y=15)
        buttonFolder=tk.Button(window,text="1.Select Folder",font=f1,command = self.UpdatePath)
        buttonFolder.place(x=150,y=90)
        buttonFolder2=tk.Button(window,text="Open Folder",font=f2,command = self.OpenPath)
        buttonFolder2.place(x=300,y=90)
        
        
        # Log 窗口
        self.logtext=tk.Text(window,width=120,height=30)
        self.logtext.place(x=10,y=150,anchor=tk.NW)


        
        self.connectWwise()
        self.updateP4Usage()
        window.lift()
        window.mainloop()
    
    def PrintLog(self,string):  # 在用户界面里打印提示 
        self.logtext.insert(tk.END, string + '\n'+'\n') 
        self.logtext.see(tk.END)
        self.logtext.update()
    
    def UpdatePath(self):                   # 用户选择文件路径
        self.PrintLog("")
        self.PrintLog("Select Folder ...")
        path_ = tk.filedialog.askdirectory()   
        if path_=='':
            return
        self.path = path_
        varTextFolder.set(path_)
        self.PrintLog ("Get Directory: "+ path_)
        _count=0
        for file,root in self.findallfiles(self.path):
            fname,ext=os.path.splitext(file)
            if ext!=".wav":
                continue
            _count+=1
        self.PrintLog("  总共有 "+str(_count)+" 个待导入wave文件")
        
        
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
        
        if varInt.get():
            
            self.PrintLog("")
            self.PrintLog("    尝试登陆P4...")
            p4=p4Manager()
            try:
                p4.forceConnect()
                self.PrintLog("    WorkSpace:"+str(p4.workSpaceName))
                self.PrintLog("P4登录成功!")
            except:
                self.PrintLog("《《《P4无法登录，禁用自动checkout功能！请检查P4配置信息是否正确》》》")
                self.PrintLog("《您也可以无视以上提示，手动checkout文件》")
                varInt.set(0)
            
            self.useP4=varInt.get()
            
        else:
            self.useP4=varInt.get()
            self.PrintLog("选择禁用P4")
            
    
            
    def Process(self): 
        if (not self.wwise) or (not self.wwiseProjectPathRoot):
            self.PrintLog("<<< 请先确保Wwise连接成功 >>>")
            return
        if not self.path:
            self.PrintLog("<<< 请先选择导入文件夹 >>>")
            return
           
        self.PrintLog("")
        self.PrintLog("开始批处理 ...")
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
                self.PrintLog("    ·准备替换 "+str("\Originals\\"+_oldFile.split("\Originals\\")[-1])+" ...")
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
        if varInt.get():
            try:
                p4=p4Manager()
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
        
newWindow=GUI()

