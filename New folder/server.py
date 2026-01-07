import http.server
import socketserver
import json
import threading
import os
import mimetypes
from urllib.parse import urlparse, parse_qs
from carver import carver_instance

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # API Endpoints
        if parsed_path.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = {
                "running": carver_instance.is_running,
                "progress": carver_instance.progress,
                "status": carver_instance.current_status,
                "files_found": carver_instance.files_found,
                "recent_files": carver_instance.carved_files[-5:] # Send last 5
            }
            self.wfile.write(json.dumps(status).encode())
            return
            
        if parsed_path.path == '/api/files':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(carver_instance.carved_files).encode())
            return

        # Serve Static Files
        if parsed_path.path == '/':
            self.path = '/index.html'
            
        # Map to web directory
        try:
            # Security check: prevent directory traversal
            requested_path = self.path.lstrip('/')
            full_path = os.path.join(WEB_DIR, requested_path)
            
            if os.path.commonpath([full_path, WEB_DIR]) == WEB_DIR and os.path.exists(full_path) and os.path.isfile(full_path):
                self.send_response(200)
                mime_type, _ = mimetypes.guess_type(full_path)
                self.send_header('Content-type', mime_type or 'application/octet-stream')
                self.end_headers()
                with open(full_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, str(e))

    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/carve':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            input_path = data.get('input_path')
            output_dir = data.get('output_dir', 'carved_output')
            
            if not input_path:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Missing input_path"}')
                return

            # Start carving in a separate thread
            thread = threading.Thread(target=carver_instance.carve, args=(input_path, output_dir))
            thread.start()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"message": "Carving started"}')
            return
            
        self.send_error(404)

def run_server():
    # Ensure web dir exists
    if not os.path.exists(WEB_DIR):
        os.makedirs(WEB_DIR)
        
    with socketserver.ThreadingTCPServer(("", PORT), RequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
