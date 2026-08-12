#!/usr/bin/env python3
"""Record ATA demo frames: drive the webapp flow, screenshot each key step."""
import json, time, urllib.request, base64, os
from websocket import create_connection

BASE = "http://127.0.0.1:9223"
OUT = "/home/csg/Documentos/moneyloop/ata-agent/demo/frames"
os.makedirs(OUT, exist_ok=True)
tabs = json.loads(urllib.request.urlopen(BASE + "/json", timeout=10).read())
target = next(t for t in tabs if t.get("type") == "page" and "127.0.0.1:8090" in (t.get("url") or ""))
ws = create_connection(target["webSocketDebuggerUrl"], timeout=180)
mid = 0
def cdp(method, params=None):
    global mid
    mid += 1
    ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        r = json.loads(ws.recv())
        if r.get("id") == mid:
            return r

def ev(expr):
    r = cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return r.get("result", {}).get("result", {}).get("value")

def shot(name):
    cdp("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False})
    time.sleep(0.5)
    r = cdp("Page.captureScreenshot", {"format": "png"})
    p = os.path.join(OUT, name + ".png")
    open(p, "wb").write(base64.b64decode(r["result"]["data"]))
    print("saved", name)
    cdp("Emulation.clearDeviceMetricsOverride")

# reload for a fresh state
cdp("Page.reload", {"ignoreCache": True})
time.sleep(3)
shot("01_home")

# upload the DANFE fixture via CDP file input
cdp("DOM.enable")
r = cdp("DOM.getDocument")
root = r["result"]["root"]["nodeId"]
r = cdp("DOM.querySelector", {"nodeId": root, "selector": "input[type=file]"})
fid = r["result"]["nodeId"]
cdp("DOM.setFileInputFiles", {"nodeId": fid, "files": ["/home/csg/Documentos/moneyloop/ata-agent/tests/fixtures/danfe_fixture.png"]})
print("file set; waiting for extract...")
time.sleep(10)
shot("02_uploaded")
ws.close()
