
class reaperManager:
    connection=0
    RPR=''
    ReaperProj=''
    projTitle=''
    projPath=''
    
    
    def __init__(self) -> None:
        self.connectReaper()
        
    def connectReaper(self):
        
        try:
            import reapy
        except:
            print("failed import reapy")
            return 
        

        try:
            self.ReaperProj = reapy.Project() #唯一一处直接使用reapy模块 
        except:
            self.connection=0
            print("failed get project")
            return 
        self.RPR = reapy.reascript_api
        
        self.connection=1   
        proj,bufOut,bufOut_sz=self.RPR.GetProjectName(self.ReaperProj,"",256)
        self.projTitle=bufOut[:-4]
        ( proj, bufOut, bufOut_sz ) = self.RPR.GetProjectPathEx(self.ReaperProj, "", 512 )
        self.projPath=bufOut
        print("Reaper Proj Path= "+str(self.projPath))

    def SetReaperRenderSetting_Default(self,renderPath):  # 设置默认Render参数
        if not self.ReaperProj:
            print("none reaper project")
        self.RPR.GetSetProjectInfo(self.ReaperProj,"RENDER_SETTINGS",520,1)   #selected media items
        self.RPR.GetSetProjectInfo(self.ReaperProj,"RENDER_BOUNDSFLAG",3,1)   #all project regions
        self.RPR.GetSetProjectInfo(self.ReaperProj,"RENDER_ADDTOPROJ",0,1)
        self.RPR.GetSetProjectInfo(self.ReaperProj,"RENDER_TAILMS",0,1)  #tails
        #self.RPR.GetSetProjectInfo(self.ReaperProj,"RENDER_CHANNELS",1,1)   #mono
        self.RPR.GetSetProjectInfo_String(self.ReaperProj,"RENDER_FILE",renderPath,1)  #导出地址
        #self.RPR.GetSetProjectInfo_String(self.ReaperProj,"RENDER_PATTERN","$region",1)   #命名
        self.RPR.GetSetProjectInfo_String(self.ReaperProj,"RENDER_FORMAT2","",1)      #关闭second output
        #retval, mproj, desc, valuestrNeedBig,is_set= self.RPR.GetSetProjectInfo_String(proj,"RENDER_FORMAT","",0)
        self.RPR.GetSetProjectInfo_String(self.ReaperProj,"RENDER_FORMAT","evaw",1)  #指定wave格式
    
    def SetReaperRenderSetting_RenderName(self,in_renderName):
        self.RPR.GetSetProjectInfo_String(self.ReaperProj,"RENDER_PATTERN",in_renderName,1)   #命名
    
    def executeReaperAction(self,in_commandId):
        self.RPR.Main_OnCommandEx(in_commandId,0,self.ReaperProj)
        
    def executeReaperActionByName(self,in_commandName):
        id=self.RPR.NamedCommandLookup(in_commandName)
        self.executeReaperAction(id)
    
    def openRenderSetting(self):
        self.executeReaperAction(40015)
    
    def renderWithCurrentSetting(self):
        self.RPR.Main_OnCommandEx(42230,0,self.ReaperProj)   # Render with last render setting 
    
    def ProcessFileInReaper(self,in_filePath):       # 将文件导入第一轨，处理，最后删除所有items 返回导出的所有文件
        if not in_filePath:
            print("null input filepath")
            return
        outputList=[]
        self.RPR.SetOnlyTrackSelected(self.FirstTrack)  # 强制选择第一个轨道
        self.RPR.Main_OnCommandEx(40042,0,self.ReaperProj)   # move Cursor to 0
        self.RPR.Main_OnCommandEx(41044,0,self.ReaperProj)   # move Cursor right on beat
        self.RPR.InsertMedia(in_filePath,0)                 # Insert file onto selected track
        self.RPR.SelectAllMediaItems(self.ReaperProj,1)
        
        #process here
        self.AutoDynamicSplit()
        self.RPR.SelectAllMediaItems(self.ReaperProj,1)
        if self.RPR.CountSelectedMediaItems(self.ReaperProj) <2:
            self.AutoDynamicSplit() #有时候第一次会卡住运行失败 运行两次保险一点
        
        self.RPR.SelectAllMediaItems(self.ReaperProj,1)
        self.RPR.Main_OnCommandEx(42230,0,self.ReaperProj)   # Render with last render setting 
             
        item= self.RPR.GetMediaItem(self.ReaperProj,0)
        itemcount=0
        
        while str(item)!='(MediaItem*)0x0000000000000000':
            self.RPR.DeleteTrackMediaItem( self.FirstTrack, item )
            itemcount+=1
            
            if itemcount<10:
                outputList.append(in_filePath[:-4]+"_0"+str(itemcount)+".wav")
                #print(in_filePath[:-4]+"_0"+str(itemcount)+".wav")
            else:
                outputList.append(in_filePath[:-4]+"_"+str(itemcount)+".wav")
                #print(in_filePath[:-4]+"_"+str(itemcount)+".wav")
                
            item= self.RPR.GetMediaItem(self.ReaperProj,0)
        return outputList

    
    pass