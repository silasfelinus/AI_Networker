#!/usr/bin/env python3
"""
serve_workspace.py — Local dev server for the Conductor workspace.

Serves workspace.html with live image uploads: click any image in the
browser to replace it. The server saves the file and rebuilds automatically.

Usage (from repo root):
    python scripts/serve_workspace.py
    python scripts/serve_workspace.py --port 9000
"""

import cgi
import json
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).parent.parent
IMAGES_DIR = REPO_ROOT / "projects" / "images"
WORKSPACE_FILE = REPO_ROOT / "workspace.html"
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_workspace.py"
ALLOWED_EXT = {".webp", ".png", ".jpg", ".jpeg"}
MIME = {
    ".html": "text/html; charset=utf-8",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".yaml": "text/plain; charset=utf-8",
    ".md": "text/plain; charset=utf-8",
}


def rebuild():
    r = subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=str(REPO_ROOT),
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} {fmt % args}")

    def _send(self, code, mime, body):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code, data):
        self._send(code, "application/json", json.dumps(data))

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/workspace.html"):
            self._send(200, MIME[".html"], WORKSPACE_FILE.read_bytes())
        elif path.startswith("/projects/images/"):
            f = REPO_ROOT / path.lstrip("/")
            if f.exists() and f.is_file():
                self._send(200, MIME.get(f.suffix.lower(), "application/octet-stream"), f.read_bytes())
            else:
                self._send(404, "text/plain", "not found")
        else:
            self._send(404, "text/plain", "not found")

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/upload":
            env = {
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers.get("content-type", ""),
                "CONTENT_LENGTH": self.headers.get("content-length", "0"),
            }
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ=env)

            slug = (form.getvalue("slug") or "").strip()
            variant = (form.getvalue("variant") or "").strip()

            if not slug or not variant:
                self._json(400, {"error": "slug and variant are required"})
                return

            if "file" not in form:
                self._json(400, {"error": "no file in request"})
                return

            item = form["file"]
            ext = Path(item.filename or "").suffix.lower() if hasattr(item, "filename") else ""
            if ext not in ALLOWED_EXT:
                self._json(400, {"error": f"extension '{ext}' not allowed; use .webp .png .jpg .jpeg"})
                return

            dest = IMAGES_DIR / f"{slug}-{variant}{ext}"
            dest.write_bytes(item.file.read())

            ok, out = rebuild()
            if ok:
                self._json(200, {"ok": True, "saved": str(dest.relative_to(REPO_ROOT))})
            else:
                self._json(500, {"error": "rebuild failed", "detail": out})

        elif path == "/rebuild":
            ok, out = rebuild()
            self._json(200 if ok else 500, {"ok": ok, "detail": out})

        else:
            self._send(404, "text/plain", "not found")


def main():
    port = 8000
    args = sys.argv[1:]
    if "--port" in args:
        port = int(args[args.index("--port") + 1])

    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"\n  Conductor Workspace Server")
    print(f"  Open  →  http://127.0.0.1:{port}/")
    print(f"  Click any placeholder image to upload a replacement.")
    print(f"  Stop  →  Ctrl+C\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")


if __name__ == "__main__":
    main()
