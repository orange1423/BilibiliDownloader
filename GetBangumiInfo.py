# 由 MDID,SSID,EPID 获取视频信息
import requests
import json
import Settings

# 由 MDID 获取视频信息
def GetMediaInfo(mdid,sessdata=""):
    # 检查是否提供了MDID
    if mdid == "":
        print("GetBangumiInfo:必须提供mdid")
        return
    # 准备GET请求的信息
    cookies = {}
    params = {"media_id":mdid}
    if sessdata.strip() != "":
        cookies = {"SESSDATA":sessdata}
    # 发出和解析请求
    r = requests.get("https://api.bilibili.com/pgc/review/user",params=params,cookies=cookies)
    jsonobj = json.loads(r.text)
    if jsonobj["code"] == 0:
        title = jsonobj["result"]["media"]["title"]
        ssid = jsonobj["result"]["media"]["season_id"]
        print("GetBangumiInfo:取得剧集:",title,"SSID:",ssid)
        return GetBangumiInfo(ssid=ssid,sessdata=sessdata)
    else:
        print("GetBangumiInfo:请求: ",r.url," 错误: ",jsonobj["message"])
        return {"code":jsonobj["code"],"results":[]}

# 由 SSID,EPID 获取视频信息
def GetBangumiInfo(ssid="",epid="",sessdata=""):
    # 检查是否提供了SSID或EPID
    if ssid == "" and epid == "":
        print("GetBangumiInfo:必须提供ssid与epid其中之一")
        return
    # 准备GET请求的信息
    cookies = {}
    params = {}
    if sessdata.strip() != "":
        cookies = {"SESSDATA":sessdata}
    if ssid != "":
        params = {"season_id":ssid}
    else:
        params = {"ep_id":epid}
    # 发出和解析请求
    r = requests.get("https://api.bilibili.com/pgc/view/web/season",params=params,cookies=cookies)
    jsonobj = json.loads(r.text)
    results = []
    if jsonobj["code"] == 0:
        for data in jsonobj["result"]["episodes"]:
            print("GetBangumiInfo:取得视频:",data["title"],"，标题为:",data["long_title"],"，AID:",data["aid"],"，BVID:",data["bvid"],"，CID:",data["cid"])
            result = {"title":jsonobj["result"]["title"],"subtitle":data["title"] + "." + data["long_title"],"aid":data["aid"],"bvid":data["bvid"],"cid":data["cid"]}
            results.append(result)
        rstr = input("请输入下载范围（留空下载全部）：")
        if len(rstr.split("-")) == 2:
            results = results[int(rstr.split("-")[0]) - 1:int(rstr.split("-")[1])]
        return {"code":jsonobj["code"],"results":results}
    else:
        print("GetBangumiInfo:请求: ",r.url," 错误: ",jsonobj["message"])
        return {"code":jsonobj["code"],"results":[]}

if __name__ == '__main__':
    if Settings.sessdata != "":
        sessdata = Settings.sessdata
    else:
        sessdata = input("请输入SESSDATA：")
    id = input("请输入SSID或EPID或MDID：")
    if id.startswith("ss") or id.startswith("SS"):
        ssid = id[2:]
        GetBangumiInfo(ssid=ssid,sessdata=sessdata)
    elif id.startswith("ep") or id.startswith("EP"):
        epid = id[2:]
        GetBangumiInfo(epid=epid,sessdata=sessdata)
    elif id.startswith("md") or id.startswith("MD"):
        mdid = id[2:]
        GetMediaInfo(mdid=mdid,sessdata=sessdata)
    else:
        print("无法识别你的输入！")
        