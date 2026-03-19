#!/usr/bin/env python3
"""
🐝 خادم لعبة الحروف - للشبكة المحلية
══════════════════════════════════════
يعمل هذا الخادم على حاسوبك ويسمح للهواتف المتصلة بنفس الـ WiFi
بالوصول للعبة وصفحة البازر بدون إنترنت.

التثبيت (مرة واحدة):
  pip install websockets

التشغيل:
  python server.py

ثم افتح على أي جهاز في الشبكة:
  http://192.168.1.X:8000          ← اللعبة
  http://192.168.1.X:8000/buzzer   ← البازر
  ws://192.168.1.X:8765            ← WebSocket للبازر

استبدل 192.168.1.X بعنوان IP حاسوبك.
"""

import asyncio
import json
import os
import socket
import threading
import http.server
import webbrowser
from pathlib import Path

# ── Configuration ──
HTTP_PORT = 8000
WS_PORT   = 8765
DIRECTORY = Path(__file__).parent  # same folder as the HTML files

# ── Get local IP ──
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()

# ═══════════════════════════════════════
# HTTP SERVER (serves HTML/JSON files)
# ═══════════════════════════════════════
class GameHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def translate_path(self, path):
        # Allow /buzzer → /buzzer.html
        if path == '/buzzer' or path == '/buzzer/':
            path = '/buzzer.html'
        return super().translate_path(path)

    def end_headers(self):
        # Allow cross-origin (needed for BroadcastChannel across pages)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        # Quiet logging
        pass

def start_http():
    server = http.server.HTTPServer(('0.0.0.0', HTTP_PORT), GameHTTPHandler)
    server.serve_forever()

# ═══════════════════════════════════════
# WEBSOCKET SERVER (syncs buzzer)
# ═══════════════════════════════════════
connected_clients = set()
client_lock = asyncio.Lock()

async def ws_handler(websocket):
    async with client_lock:
        connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                # Relay to ALL other clients
                async with client_lock:
                    others = connected_clients - {websocket}
                if others:
                    msg_str = json.dumps(data)
                    await asyncio.gather(*[c.send(msg_str) for c in others], return_exceptions=True)
            except json.JSONDecodeError:
                pass
    except Exception:
        pass
    finally:
        async with client_lock:
            connected_clients.discard(websocket)

async def start_ws():
    try:
        import websockets
        async with websockets.serve(ws_handler, '0.0.0.0', WS_PORT):
            print(f"  ✅ WebSocket يعمل على: ws://{LOCAL_IP}:{WS_PORT}")
            await asyncio.Future()  # run forever
    except ImportError:
        print("\n  ❌ مكتبة websockets غير مثبتة!")
        print("  ثبّتها بالأمر: pip install websockets\n")
    except OSError as e:
        print(f"\n  ❌ خطأ في WebSocket: {e}")
        print(f"  تأكد أن المنفذ {WS_PORT} غير مستخدم\n")

# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════
def main():
    print("\n" + "═"*50)
    print("  🐝 خادم لعبة الحروف العربية")
    print("═"*50)
    print(f"\n  📁 الملفات من: {DIRECTORY}")
    print(f"\n  🌐 عناوين الوصول:")
    print(f"     اللعبة    → http://{LOCAL_IP}:{HTTP_PORT}")
    print(f"     البازر    → http://{LOCAL_IP}:{HTTP_PORT}/buzzer")
    print(f"     WebSocket → ws://{LOCAL_IP}:{WS_PORT}")
    print(f"\n  💡 افتح العناوين أعلاه على أي جهاز متصل بنفس الـ WiFi")
    print(f"  ⏹  اضغط Ctrl+C للإيقاف")
    print("\n" + "═"*50 + "\n")

    # Start HTTP in background thread
    http_thread = threading.Thread(target=start_http, daemon=True)
    http_thread.start()
    print(f"  ✅ HTTP يعمل على: http://{LOCAL_IP}:{HTTP_PORT}")

    # Open browser automatically
    try:
        webbrowser.open(f"http://localhost:{HTTP_PORT}")
    except:
        pass

    # Start WebSocket (async)
    asyncio.run(start_ws())

if __name__ == '__main__':
    main()
