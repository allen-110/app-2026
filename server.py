# server.py
import subprocess
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

TOKEN = os.environ.get("EXEC_TOKEN", "changeme")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        token = params.get("token", [""])[0]
        if token != TOKEN:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"unauthorized")
            return

        cmd = params.get("cmd", [""])[0]
        if not cmd:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"missing cmd param")
            return

        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=15
            )
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(output.encode())

    def log_message(self, format, *args):
        pass  # 不打印访问日志，避免命令内容泄露到日志里

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()
