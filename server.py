# server.py
import subprocess
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

TOKEN = os.environ.get("EXEC_TOKEN", "changeme")

PAGE = """<!DOCTYPE html>
<html>
<head>
<title>Console</title>
<style>
body { background:#1e1e1e; color:#eee; font-family: monospace; padding:20px; }
input, button { padding:8px; font-family: monospace; }
#cmd { width: 70%%; }
#out { background:#000; color:#0f0; padding:15px; margin-top:15px; white-space:pre-wrap; min-height:300px; border-radius:4px; }
</style>
</head>
<body>
<h3>Container Console</h3>
<input id="token" type="password" placeholder="token" />
<input id="cmd" type="text" placeholder="command, e.g. whoami" />
<button onclick="run()">Run</button>
<div id="out"></div>
<script>
async function run() {
  const token = document.getElementById('token').value;
  const cmd = document.getElementById('cmd').value;
  const out = document.getElementById('out');
  out.textContent = 'running...';
  try {
    const res = await fetch('/exec?token=' + encodeURIComponent(token) + '&cmd=' + encodeURIComponent(cmd));
    out.textContent = await res.text();
  } catch(e) {
    out.textContent = 'error: ' + e;
  }
}
document.getElementById('cmd').addEventListener('keydown', e => { if (e.key === 'Enter') run(); });
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PAGE.encode())
            return

        if parsed.path == "/exec":
            params = parse_qs(parsed.query)
            token = params.get("token", [""])[0]
            if token != TOKEN:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"unauthorized")
                return

            cmd = params.get("cmd", [""])[0]
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(output.encode())
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
