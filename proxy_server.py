from http.server import BaseHTTPRequestHandler, HTTPServer
import os, json, urllib.parse, socket, select

PORT = 8080
APPS_FILE = "apps.json"

class SwitchProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        host = self.headers.get("Host", "")
        clean_path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Forward external web requests (Google & SwitchBrowse)
        if host and "nintendo" not in host and "192.168." not in host and "127.0.0.1" not in host and "localhost" not in host:
            self.forward_http()
            return

        # API 1: XploreSW File Browser & Download
        if clean_path == "/api/files":
            target_dir = query.get("dir", [os.path.expanduser("~")])
            if not os.path.exists(target_dir):
                target_dir = os.path.expanduser("~")
            items = []
            try:
                for entry in os.scandir(target_dir):
                    items.append({
                        "name": entry.name,
                        "path": entry.path,
                        "is_dir": entry.is_dir()
                    })
            except PermissionError:
                pass
            items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
            payload = json.dumps({
                "current": os.path.abspath(target_dir),
                "parent": os.path.dirname(os.path.abspath(target_dir)),
                "items": items
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if clean_path == "/api/download":
            file_path = query.get("path", [""])
            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(file_path)}"')
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404, "File not found")
            return

        # API 2: App Store List
        if clean_path == "/api/apps":
            apps = []
            if os.path.isfile(APPS_FILE):
                with open(APPS_FILE, "r", encoding="utf-8") as f:
                    apps = json.load(f)
            payload = json.dumps(apps).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        # Serve Local Webmenu Files
        local_file = clean_path.lstrip("/")
        if local_file and os.path.isfile(local_file):
            with open(local_file, "rb") as f:
                data = f.read()
            self.send_response(200)
            if local_file.endswith(".html"):
                self.send_header("Content-Type", "text/html; charset=utf-8")
            elif local_file.endswith(".ttf"):
                self.send_header("Content-Type", "font/ttf")
            elif local_file.endswith(".woff2"):
                self.send_header("Content-Type", "font/woff2")
            else:
                self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # Default to index.html for Switch Captive Portal Check
        if os.path.isfile("index.html"):
            with open("index.html", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    def do_CONNECT(self):
        host, _, port_str = self.path.partition(":")
        port = int(port_str) if port_str else 443
        try:
            remote = socket.create_connection((host, port), timeout=10)
            self.send_response(200, "Connection Established")
            self.end_headers()
            conns = [self.connection, remote]
            while True:
                r, _, _ = select.select(conns, [], [], 10)
                if not r:
                    break
                for s in r:
                    data = s.recv(8192)
                    if not data:
                        remote.close()
                        return
                    (remote if s is self.connection else self.connection).sendall(data)
        except Exception:
            self.send_error(502, "Bad Gateway")

    def forward_http(self):
        self.send_error(502, "HTTP forwarding not needed")

# i was planning to do pictopicto
# i guess it did NOT work out...

print(f"[PROXY] 'the webmenu channel' running on 192.168.1.176:{PORT}")
HTTPServer(("0.0.0.0", PORT), SwitchProxyHandler).serve_forever()
