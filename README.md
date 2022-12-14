# Tool_ReplaceWwiseWavesWithP4
*(English Version will be in the upcoming release）*  
这是一个方便使用P4对Wwise进行版本控制时，快速迭代音频资源的小工具  
可以免去反复迭代资源时的繁琐步骤  
**请注意：本工具仅在Wwise2021版本进行了测试**

![图片1](https://user-images.githubusercontent.com/52338219/203681670-5960f688-7874-41e0-a6ed-0f0510015535.png)  
## [点击此处跳转下载界面](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/releases)

## Installation
**1.电脑中安装了Perforce的情况下，打开控制台（Win+R 输入cmd然后回车）**  
![图片2](https://user-images.githubusercontent.com/52338219/203682044-033c33dd-a1ba-47b3-99c8-997dae674d28.png)

**2.依次输入如下指令，配置电脑环境的P4账号密码等信息：**  
p4 set P4PORT=您的P4服务器地址和端口  
p4 set P4USER=您的P4用户名  
p4 set P4PASSWD=您的P4密码  
p4 set P4CLIENT=WorkSpace全称  
![图片3](https://user-images.githubusercontent.com/52338219/203682135-a68529ba-2915-494c-8f72-78741689a71f.png)  
(可以直接从P4登录窗口粘贴)  


**3.打开wwise的用户设置，将WAMPport改为8070（可以不用改）**  
![图片5](https://user-images.githubusercontent.com/52338219/203683152-dbbe03b2-5893-44b8-ab8d-38d9315108d2.png)


## How To Use  
**1.开启Wwise后运行 .exe工具**  
它会自动尝试连接wwise和登录P4  
*如果WAMP端口不是8070，则会连接失败，此时请工具里填上正确的port然后点击Connect Wwise*  
*如果P4登录失败，请点击显示P4账号信息进行检查，然后回到Install的第二步*  
全部成功的话会如下显示：  
![图片6](https://user-images.githubusercontent.com/52338219/203683508-8308d0e9-b1d7-4c5a-8822-b6d97c7b0e10.png)  


**2.点击SelectFolder选择要导入的文件夹路径，点击“批量替换”开始工作**  
等待“批处理完成”提示出现  
可以回看过程中的记录  
*如果有文件在Wwise内找不到可替换的对象时（新增的资源），则会被归档*  
![图片8](https://user-images.githubusercontent.com/52338219/203745063-d02d7e4a-0281-4bba-98a3-b47180be1cf9.png)  
*(“完美替换”是指成功替换并且在P4中成功checkout)*

## Use Without P4
如果不用P4，也是可以使用此工具的。  
点击“批量替换”之前，将右边“自动Checkout”关闭即可。  
![图片7](https://user-images.githubusercontent.com/52338219/203690232-6e849533-3146-4782-8c96-1cfa001ca0e0.png)

## Contact
Wechat: kkxszz  
Email: kkxszz@gmail.com  

## 写给开发者
开发环境是Python3.7，需要安装waapiclient （环境搭建可以参考溪夜老师的博客）  
szz_wwiseManager.py 中留有一些我封装过的常用waapi功能，欢迎交流~  
![image](https://user-images.githubusercontent.com/52338219/203762564-8c1877a2-3900-4f23-addb-ce5aa2cf8c29.png)

