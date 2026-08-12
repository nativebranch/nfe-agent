#!/usr/bin/env python3
"""Re-send payment request, wait for reply, capture it + frame 04 again."""
import json, time, urllib.request, base64, os
from websocket import create_connection

BASE = "http://127.0.0.1:9223"
OUT = "/home/csg/Documentos/moneyloop/ata-agent/demo/frames"
tabs = json.loads(urllib.request.urlopen(BASE + "/json", timeout=10).read())
target = next(t for t in tabs if t.get("type") == "page" and "127.0.0.1:8090" in (t.get("url") or ""))
ws = create_connection(target["webSocketDebuggerUrl"], timeout=300)
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
    time.sleep(0.4)
    r = cdp("Page.captureScreenshot", {"format": "png"})
    open(os.path.join(OUT, name + ".png"), "wb").write(base64.b64decode(r["result"]["data"]))
    cdp("Emulation.clearDeviceMetricsOverride")

msg = "Gere um pedido de pagamento de 3000 reais em USDC"
ev(f"""(() => {{
  const i = document.getElementById('input'); const b = document.getElementById('send');
  const s = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  s.call(i, {json.dumps(msg)});
  i.dispatchEvent(new Event('input', {{bubbles:true}}));
  return b.disabled;
}})()""")
time.sleep(0.4)
ev("document.getElementById('send').click()")
# poll for a new agent message (count before/after)
base = ev("document.getElementById('msgs').children.length")
reply = None
for attempt in range(12):
    time.sleep(15)
    msgs = ev("document.getElementById('msgs').children.length") or 0
    if msgs > base:
        reply = ev("document.getElementById('msgs').innerText") or ""
        break
print("NEW MSG:", reply is not None)
if reply:
    print(reply[-900:])
    shot("04_payment")
ws.close()
