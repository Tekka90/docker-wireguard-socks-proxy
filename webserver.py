import http.server
import socketserver

from homepage import Page

PORT = 8080
FAVICO = '/app/icon/favicon.ico'

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/icon/"):
            f = open('/app' + self.path,'rb')
            self.send_response(200)
            self.send_header('Content-type','mimetype')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        elif self.path == "/favicon.ico":
            f = open(FAVICO,'rb')
            self.send_response(200)
            self.send_header('Content-type','mimetype')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        else:
            page = Page(self)
            page.print()
        return

    def do_POST(self):        
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('ascii').split('=')[1]
        page = Page(self, body)
        page.print()

    
class ThreadingSimpleServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

server = ThreadingSimpleServer(('0.0.0.0', PORT), Handler)
print("serving at port", PORT)
try:
    while 1:
        server.handle_request()
except KeyboardInterrupt:
    print("\nShutting down server per users request.")


