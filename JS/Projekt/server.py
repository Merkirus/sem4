from http.server import BaseHTTPRequestHandler
import socketserver
import cgi
import wea
import constants
import json

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
        data = wea.get_weather(form.getvalue('city'), form.getvalue('date'))
        if not isinstance(data, constants.Error):
            self.wfile.write(str.encode(json.dumps(data)))
        else:
            self.wfile.write(str.encode(str(data.name)))

if __name__ == "__main__":
    server_address = (str(constants.Server.URL.value), int(constants.Server.PORT.value))
    with socketserver.TCPServer(server_address, Server) as httpd:
        httpd.serve_forever()
