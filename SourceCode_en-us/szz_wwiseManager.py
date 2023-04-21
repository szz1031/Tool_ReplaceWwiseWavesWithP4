from waapi import WaapiClient
import os
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, wait
import asyncio

class WwiseManager:

    #default path
    defaultSelectedObject={
        'name': 'Default Work Unit',
        'path': '\\Actor-Mixer Hierarchy\\Default Work Unit',
        'type': 'WorkUnit'
        }

    _lastSelectedObject=''

    toolname="ReplaceWwiseWavesWithP4"
    info=''
    savedPropertyValue=''
    savedProperty=''
    
    WwiseInfo=''
    WwiseProjectInfo=''
    WwiseProjectPathRoot=''
    
    
    myUrl=""
    
    def try_connect_waapi(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            with WaapiClient(url=self.myUrl) as client:
                client.call("ak.soundengine.postMsgMonitor", self._msgToArgs("Waapi Connect Success"))
                return True
        except Exception as e:
            print(f"Error connecting to Wwise: {e}")
            return False

    def __init__(self,in_portId='8070'):
        self.myUrl= "ws://127.0.0.1:"+in_portId+"/waapi" # WAMP port 
        self._lastSelectedObject=self.defaultSelectedObject
        timeout = 5  # 设置超时时间，单位为秒

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.try_connect_waapi)
            done, not_done = wait([future], timeout=timeout)

            if future in done:
                if future.result():
                    self._getWwiseInfo()
                    self._getWwiseProjectInfo()
                else:
                    return
            else:
                print("Connection to Wwise timed out.")
                return
        
    
    def _msgToArgs(self,msg): #在wwise里打log的格式转换
        args={
            "message": self.toolname+": "+msg
        }
        return args
    
    def getSelectedWwiseObjects(self): #获取所有选择的wwise对象，返回List，包含 "path","name","type","parent","id"
        args_info={
            "options":{
                "return":["path", "name", "type","parent","id"]
            }
        }
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.ui.getSelectedObjects",args_info)
            client.call("ak.soundengine.postMsgMonitor",self._msgToArgs("Choose Selected Objects"))
        try:
            self._lastSelectedObject=result['objects'][0]
        except:
            print("Please Select a Wwise Object, Use DefualtWorkUnit Instead")
            self._lastSelectedObject=self.defaultSelectedObject
            return
        return result

    def getLastSelectedWwiseObjectPath(self): # 获取上一个选择的Wwise对象，返回path
        try:            
            self.getSelectedWwiseObjects()
            path=self._lastSelectedObject['path']
        except:
            print("!!faild get path!!")
            return
        return path
    
    
    def moveObject(self,in_objID,in_targetID): # 按照id移动objec
        with WaapiClient(url=self.myUrl) as client:
            moveArges={
                        "parent": in_targetID,
                        "object": in_objID,
                        "onNameConflict": "replace"
                    }
            #pprint(moveArges)
            client.call("ak.wwise.core.object.move",moveArges)
        return
    
    def findallfiles(self,path):  # 遍历文件夹的generator，包括子文件夹，返回（文件名，文件地址）
        for root,dirs,files in os.walk(path):
            for file in files:            
                yield file,root 
    
    def importAudio(self,in_parentPath,filePath,in_originalPath):
        '''
        导入单个音频文件，语言为SFX，格式为Sound
        '''
        
        filepath,fullname=os.path.split(filePath)
        fname,ext=os.path.splitext(fullname)
        
        args={
            "importOperation": "replaceExisting",
            "autoAddToSourceControl": True,
            "default":{
                "importLanguage": "SFX"
            },
            "imports":[]
        }
        
        newImport={
                    "objectPath":in_parentPath+"\\<Sound>"+fname,
                    "audioFile": filePath,
                    "originalsSubFolder": in_originalPath
                }

        args['imports'].append(newImport)
        #print("---------Import---------")
        #pprint(args)
        #print("------------------")
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.audio.import",args)
        return result
    
    def branchImportDirectoryUnderSelectedWwisePath(self,in_wwiseObjectPath,in_osPath,in_originalPath): #批量导入整个文件夹，指定wwiseobjectpath和originpath
        '''
        批量导入整个文件夹的音频，会在origin里生成和源一样的层级结构
        '''
        args={
            "importOperation": "replaceExisting",
            "autoAddToSourceControl": True,
            "default":{
                "importLanguage": "SFX"
            },
            "imports":[]
        }
        
        for file,root in self.findallfiles(in_osPath):
            _fullname = os.path.join(root,file)
            _fullname = os.path.normpath(_fullname)  #去掉反斜杠
            
            filepath,fullname=os.path.split(_fullname)
            fname,ext=os.path.splitext(fullname)

            newImport={
                    "objectPath":in_wwiseObjectPath+"\\<Sound>"+fname,
                    "audioFile": _fullname,
                    "originalsSubFolder": in_originalPath
                }

            args['imports'].append(newImport)
            
        print("---------Import---------")
        pprint(args)
        print("------------------")
        with WaapiClient(url=self.myUrl) as client:
            client.call("ak.wwise.core.audio.import",args)
            client.call("ak.soundengine.postMsgMonitor",self._msgToArgs("Import "+in_osPath))
          
    def _getWwiseInfo(self): # 获取Wwise应用程序信息
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.getInfo")  
        if result:
            self.WwiseInfo=result
    
    def getWwiseVersion(self): # 获取Wwise版本（用于区分2019和2021的不同waapi参数）
        if not self.WwiseInfo or self.WwiseInfo=='':
            self._getWwiseInfo()
        return self.WwiseInfo['version']['displayName'][1:]
    
    def _getWwiseProjectInfo(self): # 获取Wwise工程的信息，包含“name” “filePath”
        if not self.WwiseProjectInfo or self.WwiseProjectInfo=='':
            
            #2021 的写法
            _args={
                "waql":"\"\\\"",
                "options": {
                    "return":[
                        "name",
                        "filePath"
                        ]
                }
            }
            with WaapiClient(url=self.myUrl) as client:
                result=client.call("ak.wwise.core.object.get",_args)  
            self.WwiseProjectInfo=result["return"][0]
        self.WwiseProjectPathRoot= os.path.dirname(self.WwiseProjectInfo['filePath'])
        return self.WwiseProjectInfo
    
    def getPathID(self,in_path): # 通过wwise对象路径获取GUID 找不到时返回False
        #2021
        _args={
            "waql":"\""+in_path+"\"",
            "options": {
                "return":[
                    "name",
                    "id"
                    ]
            }
        }
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.get",_args)  
        #pprint(result)
        if not result:
            return False
        return result["return"][0]["id"]
    
    def _WwiseCMD(self,in_cmd,in_ObjList):
        _arg={
            "command":in_cmd,
            "objects":in_ObjList
        }
        with WaapiClient(url=self.myUrl) as client:
            client.call("ak.wwise.ui.commands.execute",_arg)  
        
    def checkOutWorkUnit(self,in_workUnit): # checkout 指定workunit。可以输入path、guid
        self._WwiseCMD("WorkgroupCheckoutWWU",[in_workUnit])
    
    def createStateGroup(self,in_parentPath,in_stateGroupName,in_stateNameList): # 生成整个stateGroup，返回waapi的完整result
        
        # 判断该请求是否合法
        if not self.getPathID(in_parentPath) or "States" not in in_parentPath:
            print("Invalid ParentPath !! Stop Create State")
            return 
        
        _childList=[]
        
        for item in in_stateNameList:
            _child={
                "type": "State",
                "name": item
            }
            _childList.append(_child)
        
        args_create_State={
            "parent": in_parentPath,
            "autoAddToSourceControl": True,
            "onNameConflict": "merge",
            "type": "StateGroup",
            "name": in_stateGroupName,
            "children":_childList
        }
        #pprint(args_create_State)
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.create",args_create_State)
        return result
    
    def createMusicSwitch(self,in_parentPath,in_musicSwitchName,in_playlistNameList): # 生成MusicSwitch和一系列MusicPlayListContainer，返回waapi的完整result
        
        # 判断该请求是否合法
        if not self.getPathID(in_parentPath) or "Interactive Music Hierarchy" not in in_parentPath:
            print("Invalid ParentPath !! Stop Create MusicSwitch")
            return 
        
        # 生成children内容
        _childList=[]
        for item in in_playlistNameList:
            _child={
                "type": "MusicPlaylistContainer",
                "name": item
            }
            _childList.append(_child)
        
        args_create={
            "parent": in_parentPath,
            "autoAddToSourceControl": True,
            "onNameConflict": "merge",
            "type": "MusicSwitchContainer",
            "name": in_musicSwitchName,
            "children":_childList
        }
        
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.create",args_create)
        return result
    
    def createEvent(self,in_parentPath,in_EventName,in_targetPath): # 生成Event壳和下属的PlayAction，返回waapi的完整result
        
        # 判断该请求是否合法
        if not self.getPathID(in_parentPath) or "Events" not in in_parentPath:
            print("Invalid ParentPath !! Stop Create Event")
            return 
        
        args_createEvent_Play={
                    "parent": in_parentPath,
                    "type": "Event",
                    "name": in_EventName,
                    "onNameConflict": "replace",
                    "children": [
                            {
                                "name": "",
                                "type": "Action",
                                "@ActionType": 1,
                                "@Target": in_targetPath
                            }
                    ]
                }
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.create",args_createEvent_Play)
        return result
    
    def createWorkUnit(self,in_parentPath,in_name): # merge形式生成WWU，返回waapi result
        
        args_create={
            "parent": in_parentPath,
            "autoAddToSourceControl": True,
            "onNameConflict": "merge",
            "type": "WorkUnit",
            "name": in_name,
        }
        
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.create",args_create)
        return result
    
    def createFolder(self,in_parentPath,in_name):
        args_create={
            "parent": in_parentPath,
            "autoAddToSourceControl": True,
            "onNameConflict": "merge",
            "type": "Folder",
            "name": in_name,
        }
        
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.create",args_create)
        return result
    
    def createMusicPlaylistContainer(self,in_parentPath,in_name):
        args_create={
            "parent": in_parentPath,
            "autoAddToSourceControl": True,
            "onNameConflict": "merge",
            "type": "MusicPlaylistContainer",
            "name": in_name,
        }
        
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.create",args_create)
        return result
    
    
    def setReference(self,in_object,in_reference,in_value): # 用于设置bus、attenuation等设置
        _args={
            "object":in_object,
            "reference":in_reference,
            "value":in_value
        }
        
        with WaapiClient(url=self.myUrl) as client:
            result=client.call("ak.wwise.core.object.setReference",_args)
        return result
    
'''
w=WwiseManager()
#print(w.getSelectedWwiseObjects())     # 用来获取测试路径


'''

