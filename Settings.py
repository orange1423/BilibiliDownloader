import json
import os

if __name__ == '__main__':
    dir = input("下载保存目录：")
    sessdata = input("SESSDATA:")
    rpcserver = input("Aria2 RPC-Server:")
    syncdownload = bool(input("是否同步下载（如不同步下载，自动合并功能将失效）："))
    automerge = bool(input("是否自动合并视频："))
    autodelete = bool(input("合并后是否删除原文件："))
    ua = input("Aria2浏览器UA：")
    quality = input("默认下载清晰度代码（自动选择最高请填-1）：")
    settings = {
        "dir":dir,
        "sessdata":sessdata,
        "rpcserver":rpcserver,
        "syncdownload":syncdownload,
        "automerge":automerge,
        "autodelete":autodelete,
        "ua":ua,
        "quality":quality
    }
    with open("settings.json","w") as f:
        f.write(json.dumps(settings))
else:
    dir = "D:\\Download"
    sessdata = ""
    rpcserver = "http://localhost:6800/rpc"
    syncdownload = True
    automerge = True
    autodelete = True
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    quality = -1
    if os.path.exists("settings.json"):
        with open("settings.json","r") as f:
            jsonobj = json.loads(f.read())
        dir = jsonobj["dir"]
        sessdata = jsonobj["sessdata"]
        rpcserver = jsonobj["rpcserver"]
        syncdownload = jsonobj["syncdownload"]
        automerge = jsonobj["automerge"]
        autodelete = jsonobj["autodelete"]
        ua = jsonobj["ua"]
        quality = jsonobj["quality"]
    else:
        settings = {
        "dir":dir,
        "sessdata":sessdata,
        "rpcserver":rpcserver,
        "syncdownload":syncdownload,
        "automerge":automerge,
        "autodelete":autodelete,
        "ua":ua,
        "quality":quality
        }
        with open("settings.json","w") as f:
            f.write(json.dumps(settings))