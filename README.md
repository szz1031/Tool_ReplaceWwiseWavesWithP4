# Tool_ReplaceWwiseWavesWithP4

**[切换到英文 Switch to English](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/blob/main/README.en-US.md)**  

这是一个方便使用P4对Wwise进行版本控制时，快速迭代音频资源的小工具  

请注意：本工具仅在**Wwise2021、Wwise2022**版本进行了测试  

### [点击此处跳转下载界面](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/releases)

## How To Use  


### 1.【可选】点击“设置-设置P4账号信息”进行账号设置  

您的设置会保存到本地，下次打开时不用再次输入   

![2](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/assets/52338219/fc8f65cc-9508-4ae3-b22a-9ba4495b9b89)


### 2.点击“选择文件夹”选择要导入的文件夹路径  
  
选择完毕之后，可以点击中间的“在文件夹浏览器中打开”进行快速预览

![3](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/assets/52338219/46f52f3e-7787-4ada-9bde-840588185e50)

### （可选）使用Reaper导出 （该功能不稳定，谨慎使用）

使用此功能，需要给Reaper配置python环境，[可参考](https://www.bilibili.com/read/cv26536797/)  
该工具会抓取当前激活的reaper工程，按照region matrix设置的情况，导出region命名的wave文件，归档到reaper工程目录内。  
导出后，可以点击“在文件夹浏览器中打开”进行快速预览

### 3.点击“自动导入Wwise”开始批量导入

需要在右侧正确填写Wwise工程设置里的Wwise端口，默认是8080  
(可选)如果配置了P4账号，打勾以便自动checkout
![4](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/assets/52338219/b0cbfcd5-29d1-4e3d-909b-28978e022331)


## Contact

Wechat: kkxszz  
Email: kkxszz@gmail.com  

## 写给开发者  

开发环境是Python3.9(reapy模块和PyQt对此有硬性要求)，需要安装以下模块:  

```sh
$ pip install p4python  
$ pip install waapi-client  
$ pip install PyQt5  
$ pip install python-reapy  
```

顺便分享一些waapi封装库，欢迎交流~  

![image](https://user-images.githubusercontent.com/52338219/203762564-8c1877a2-3900-4f23-addb-ce5aa2cf8c29.png)  

*非码出身，该分享肯定有很多不足之处，非常欢迎接受同行的批评和建议！*  
