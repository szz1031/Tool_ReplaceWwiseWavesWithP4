# Tool_ReplaceWwiseWavesWithP4

*[切换到中文 change to Chinese](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/blob/main/README.md)*  

This is a small tool for quickly reimport audio resources when using **P4** to version control **Wwise**  

Please note: this tool has only been tested on **Wwise2021 & Wwise2022** versions  

### [Download Page](https://github.com/szz1031/Tool_ReplaceWwiseWavesWithP4/releases)

## How To Use  


### 1.Run the .exe tool  

Please fill in the correct WAMP port in the tool (8080 for new installed Wwise) and click "Connect to Wwise"   

![图1](https://user-images.githubusercontent.com/52338219/232001837-74939a9a-2270-419d-9c55-f1af6e014baa.png)  


### 2.*（Skip this step if you don’t use P4V）* Click "Configure P4 account" to set up p4V environment  

Your settings will be saved locally, so you don't need to enter them again when you open this tool next time   

![image](https://user-images.githubusercontent.com/52338219/232003095-8bd136cf-994e-4016-a8e5-a97fb1521f5c.png)  


### 3.Click "Select Folder" to choose the folder to import, click "Import To Wwise" to start working  
  
If there is a file that cannot be replaced in Wwise, it will be archived in a folder under the original path  

![image](https://user-images.githubusercontent.com/52338219/232007129-070b0331-401f-47c6-b411-1d1d836ef875.png)  



## Contact

Wechat: kkxszz  
Email: kkxszz@gmail.com  

## For Developers  

I Use Python3.7 to develope this tool, and following modules are needed:

```sh
$ pip install p4python  
$ pip install waapi-client  
$ pip install PyQt5  
```
  
*I'm not a professional programmer, and i welcome any kind of segguestions or corrections*  

