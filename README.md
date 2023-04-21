# Tool_ReplaceWwiseWavesWithP4

*(English Version will be in the upcoming release）*  

这是一个方便使用P4对Wwise进行版本控制时，快速迭代音频资源的小工具  

请注意：本工具仅在**Wwise2021、Wwise2022**版本进行了测试  

### [点击此处跳转下载界面](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/releases)

## How To Use  


### 1.开启Wwise后运行 .exe工具  

请工具里填上正确的WAMP端口(Wwise默认是8080)然后点击“连接到Wwise”   

![图1](https://user-images.githubusercontent.com/52338219/232001837-74939a9a-2270-419d-9c55-f1af6e014baa.png)  


### 2.【不使用P4可以跳过此步骤】点击“配置P4账号信息”进行账号设置  

您的设置会保存到本地，下次打开时不用再次输入   

![image](https://user-images.githubusercontent.com/52338219/232003095-8bd136cf-994e-4016-a8e5-a97fb1521f5c.png)  


### 3.点击SelectFolder选择要导入的文件夹路径，点击“批量替换”开始工作  
  
如果有文件在Wwise内找不到可替换的对象时，则会被归档到原路径下的一个文件夹内  

![image](https://user-images.githubusercontent.com/52338219/232007129-070b0331-401f-47c6-b411-1d1d836ef875.png)  

*(“完美替换”是指成功替换并且在P4中成功checkout)*


## Contact

Wechat: kkxszz  
Email: kkxszz@gmail.com  

## 写给开发者  

开发环境是Python3.7，需要安装以下模块:  

```sh
$ pip install p4python  
$ pip install waapi-client  
$ pip install PyQt5  
```

顺便分享一些waapi封装库，欢迎交流~  

![image](https://user-images.githubusercontent.com/52338219/203762564-8c1877a2-3900-4f23-addb-ce5aa2cf8c29.png)  

*非码出身，该分享肯定有很多不足之处，非常欢迎接受同行的批评和建议！*  
