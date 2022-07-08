from xmlrpc.client import ServerProxy
import time
import GetVideoInfo
import GetBangumiInfo
import GetDownloadUrl
import Settings
import Process
import os
from os import path

# 删除文件名里不该有的东西
def PrepareFileName(str):
    return str.replace("/", "").replace("\\","").replace(":","").replace("*","").replace("?","").replace("\"","").replace("<","").replace(">", "").replace("|","")

# 获取下载状态
def Aria2DownloadStatus(gid):
    if gid == 0:
        return "complete"
    s = ServerProxy(Settings.rpcserver)
    return s.aria2.tellStatus(gid,["status"])["status"]

# 获取下载文件所在路径
#def Aria2GetPath(gid):
#    s = ServerProxy(Settings.rpcserver)
#    status = s.aria2.tellStatus(gid,["files"])
#    return status["files"][0]["path"]

# 等待下载完成
def Aria2Wait(gid):
    s = ServerProxy(Settings.rpcserver)
    while True: 
        time.sleep(1)
        status = s.aria2.tellStatus(gid,["status","downloadSpeed","completedLength","totalLength","files"])
        if status["status"] == "active" or status["status"] == "waiting" or status["status"] == "paused":
            print("DownloadVideo：下载状态：",status["status"],"，速度：",status["downloadSpeed"],"byte/s，",status["completedLength"],"/",status["totalLength"])
        elif status["status"] == "complete":
            print("DownloadVideo：下载完成：",status["files"][0]["path"])
            return True
        elif status["status"] == "error" or status["status"] == "removed":
            print("DownloadVideo：下载失败。")
            return False

# 检查文件，返回True为需要下载，False为跳过下载
def CheckFile(filepath):
    if path.exists(filepath + ".mkv"):
        return False
    else:
        return True

# 检查文件，返回True为需要下载，False为跳过下载
def Aria2CheckFile(filepath):
    if path.exists(filepath):
        if path.exists(filepath + ".aria2"):
            os.remove(filepath)
            os.remove(filepath + ".aria2")
            return True
        else:
            return False
    else:
        return True

# 调用Aria2下载
def Aria2Download(url,sync=True,out="",dir=Settings.dir):
    s = ServerProxy(Settings.rpcserver)
    ua = Settings.ua
    ref = "https://www.bilibili.com/"
    if out.strip() != "":
        if not Aria2CheckFile(path.join(dir,out)):
            print("DownloadVideo:文件已存在，跳过下载")
            return 0
        options = {"dir": dir, "out": out,"referer":ref,"user-agent":ua,"allow-overwrite":True}
    else:
        options = {"dir": dir,"referer":ref,"user-agent":ua,"allow-overwrite":True}
    gid = s.aria2.addUri(url,options)
    if sync:
        if not Aria2Wait(gid):
            time.sleep(2)
            gid = Aria2Download(url,sync,out,dir)
    return gid

# 通过AVID或BVID，CID列表下载
def DownloadByList(list,sessdata,quality=-1):
    gidList = []
    failList = []
    code = 1 # 代码 0：全部成功；1：全部失败；2：部分失败
    for i in list:
        if len(list) == 1:
            fileName = PrepareFileName(i["title"])
            folderName = Settings.dir
        else:
            fileName = PrepareFileName(i["subtitle"])
            folderName = path.join(Settings.dir,PrepareFileName(i["title"]))
        if not CheckFile(path.join(folderName,fileName)):
            print("DownloadVideo:下载已完成，跳过下载")
            continue
        urlobj = GetDownloadUrl.GetDownloadUrl(cid=i["cid"],aid=i["aid"],bvid=i["bvid"],quality=quality,sessdata=sessdata)
        if(urlobj["code"] == 0):
            videoGid = Aria2Download(url=urlobj["videoUrl"],out=fileName + "_video.m4s",dir=folderName)
            audioGid = Aria2Download(url=urlobj["audioUrl"],out=fileName + "_audio.m4s",dir=folderName)
            if Settings.syncdownload and Settings.automerge:
                if Aria2DownloadStatus(videoGid) == "complete" and Aria2DownloadStatus(audioGid) == "complete":
                    Process.AutoMerge(path.join(folderName,fileName) + "_video.m4s")
            gidList.append({"code":urlobj["code"],"videoGid":videoGid,"audioGid":audioGid})
            if code == 1:
                code = 0
        else:
            failList.append({"code":urlobj["code"],"item":i})
            if code == 0:
                code = 2
    print("DownloadVideo:下载处理完成，成功：",len(gidList),"失败：",len(failList))
    return {"code":code,"gidList":gidList,"failList":failList}

def DownloadRange(downloadlist):
    rstr = input("DownloadVideo:请输入下载范围（留空下载全部）：")
    if len(rstr.split("-")) == 2:
        results = downloadlist[int(rstr.split("-")[0]) - 1:int(rstr.split("-")[1])]
    else:
        try:
            i = int(rstr)
            results = downloadlist[i - 1]
        except:
            results = downloadlist
    return results

# 通过AVID下载
def DownloadByAVID(aid,sessdata,quality=-1):
    data = GetVideoInfo.GetPageList(aid=aid,sessdata=sessdata)
    downloadlist = DownloadRange(data["results"])
    return DownloadByList(list=downloadlist,quality=quality,sessdata=sessdata)
    
# 通过BVID下载
def DownloadByBVID(bvid,sessdata,quality=-1):
    data = GetVideoInfo.GetPageList(bvid=bvid,sessdata=sessdata)
    downloadlist = DownloadRange(data["results"])
    return DownloadByList(list=downloadlist,quality=quality,sessdata=sessdata)

# 通过MDID下载
def DownloadByMDID(mdid,sessdata,quality=-1):
    data = GetBangumiInfo.GetMediaInfo(mdid=mdid,sessdata=sessdata)
    downloadlist = DownloadRange(data["results"])
    return DownloadByList(list=downloadlist,quality=quality,sessdata=sessdata)
# 通过SSID下载
def DownloadBySSID(ssid,sessdata,quality=-1):
    data = GetBangumiInfo.GetBangumiInfo(ssid=ssid,sessdata=sessdata)
    downloadlist = DownloadRange(data["results"])
    return DownloadByList(list=downloadlist,quality=quality,sessdata=sessdata)

# 通过EPID下载
def DownloadByEPID(epid,sessdata,quality=-1):
    data = GetBangumiInfo.GetBangumiInfo(epid=epid,sessdata=sessdata)
    downloadlist = DownloadRange(data["results"])
    return DownloadByList(list=downloadlist,quality=quality,sessdata=sessdata)

if __name__ == '__main__':
    if Settings.sessdata != "":
        sessdata = Settings.sessdata
    else:
        sessdata = input("请输入SESSDATA：")
    if Settings.quality != 0:
        quality = Settings.quality
    else:
        qstr = input("请输入清晰度代码（不填将自动选择最高画质）：")
        if qstr.strip() == "":
            quality = -1
        else:
            quality = int(qstr)
    id = input("请输入各种ID（支持BVID，AID，MDID，SSID，EPID）：")
    if id.startswith("av") or id.startswith("AV"):
        aid = id[2:]
        DownloadByAVID(aid=aid,quality=quality,sessdata=sessdata)
    elif id.startswith("bv") or id.startswith("BV"):
        bvid = id
        DownloadByBVID(bvid=bvid,quality=quality,sessdata=sessdata)
    elif id.startswith("md") or id.startswith("MD"):
        mdid = id[2:]
        DownloadByMDID(mdid=mdid,quality=quality,sessdata=sessdata)
    elif id.startswith("ss") or id.startswith("SS"):
        ssid = id[2:]
        DownloadBySSID(ssid=ssid,quality=quality,sessdata=sessdata)
    elif id.startswith("ep") or id.startswith("EP"):
        epid = id[2:]
        DownloadByEPID(epid=epid,quality=quality,sessdata=sessdata)
    else:
        print("无法识别你的输入！")