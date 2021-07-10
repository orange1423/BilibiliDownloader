# 对下载的内容进行合并处理
import os
from os import path
import Settings

def MergeVideo(video,audio,output):
    c = f"ffmpeg -i \"{video}\" -i \"{audio}\" -map 0:v -map 1:a -c copy \"{output}\""
    if(os.system(c) == 0):
        print("Process:文件合并完成：",output)
        return True
    else:
        print("Process:文件合并失败：",c)
        return False

def AutoMerge(filepath,delete=Settings.autodelete):
    if(filepath.endswith("_video.m4s")):
        flag = MergeVideo(filepath,filepath[0:-10] + "_audio.m4s",filepath[0:-10] + ".mkv")
        if(delete and flag):
            os.remove(filepath)
            os.remove(filepath[0:-10] + "_audio.m4s")

def AutoMergeAll(dir):
    for i in os.listdir(dir):
        filepath = path.join(dir,i)
        if path.isfile(filepath):
            AutoMerge(filepath)


if __name__ == '__main__':
    AutoMergeAll(input("请输入文件所在文件夹："))