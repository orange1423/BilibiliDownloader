# 由 AID，BVID，CID 获取某一视频的下载地址
import requests
import json
import Settings

def GetQuality(cid,aid="",bvid="",sessdata=""):
    # 检查是否提供了AVID或BVID
    if aid == "" and bvid == "":
        print("GetDownloadUrl:必须提供aid与bvid其中之一")
        return
    # 准备GET请求的信息
    cookies = {}
    params = {}
    if sessdata.strip() != "":
        cookies = {"SESSDATA":sessdata}
    if aid != "":
        params = {"avid":aid,"cid":cid,"fnval":16}
    else:
        params = {"bvid":bvid,"cid":cid,"fnval":16}
    # 发出和解析请求
    r = requests.get("https://api.bilibili.com/x/player/playurl",params=params,cookies=cookies)
    jsonobj = json.loads(r.text)
    if jsonobj["code"] == 0:
        qualityNum = jsonobj["data"]["accept_quality"][0]
        print("GetDownloadUrl:取得最高清晰度：",qualityNum)
        return {"code":jsonobj["code"],"qualityNum":qualityNum}
    else:
        print("GetDownloadUrl:请求：",r.url," 错误：",jsonobj["message"])
        return {"code":jsonobj["code"]}

def GetDownloadUrl(cid,quality=-1,aid="",bvid="",sessdata=""):
    # 检查是否提供了AVID或BVID
    if aid == "" and bvid == "":
        print("GetDownloadUrl:必须提供aid与bvid其中之一")
        return
    # 自动取得最高清晰度
    if (quality == -1):
        getq = GetQuality(cid=cid,aid=aid,bvid=bvid,sessdata=sessdata)
        if getq["code"] == 0:
            quality = getq["qualityNum"]
        else:
            return {"code":getq["code"]}
    # 准备GET请求的信息
    cookies = {}
    params = {}
    if sessdata.strip() != "":
        cookies = {"SESSDATA":sessdata}
    if aid != "":
        params = {"avid":aid,"cid":cid,"fnval":16,"qn":quality}
    else:
        params = {"bvid":bvid,"cid":cid,"fnval":16,"qn":quality}
    # 发出和解析请求
    r = requests.get("https://api.bilibili.com/x/player/playurl",params=params,cookies=cookies)
    jsonobj = json.loads(r.text)
    if jsonobj["code"] == 0:
        videoUrl = [jsonobj["data"]["dash"]["video"][0]["baseUrl"]]
        audioUrl = [jsonobj["data"]["dash"]["audio"][0]["baseUrl"]]
        if Settings.backupurl:
            for i in jsonobj["data"]["dash"]["video"][0]["backupUrl"]:
                videoUrl.append(i)
            for i in jsonobj["data"]["dash"]["audio"][0]["backupUrl"]:
                videoUrl.append(i)
        qualityNum = jsonobj["data"]["dash"]["video"][0]["id"]
        print("GetDownloadUrl:取得视频清晰度代码：",qualityNum)
        print("GetDownloadUrl:取得视频下载地址：",videoUrl)
        print("GetDownloadUrl:取得音频下载地址：",audioUrl)
        return {"code":jsonobj["code"],"qualityNum":qualityNum,"videoUrl":videoUrl,"audioUrl":audioUrl,"jsonobj":jsonobj}
    else:
        print("GetDownloadUrl:请求：",r.url," 错误：",jsonobj["message"])
        return {"code":jsonobj["code"]}

if __name__ == '__main__':
    sessdata = input("请输入SESSDATA：")
    id = input("请输入BVID或AID：")
    aid = ""
    bvid = ""
    if id.startswith("av") or id.startswith("AV"):
        aid = id[2:]
    elif id.startswith("bv") or id.startswith("BV"):
        bvid = id
    else:
        print("无法识别你的输入！")
        exit()
    cid = input("请输入CID：")
    qstr = input("请输入清晰度代码：")
    if qstr.strip() == "":
        quality = -1
    else:
        quality = int(qstr)
    GetDownloadUrl(cid=cid,aid=aid,bvid=bvid,sessdata=sessdata,quality=quality)