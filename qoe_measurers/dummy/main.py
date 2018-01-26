#Source : https://wiki.python.org/moin/BaseHttpServer

from http.server import BaseHTTPRequestHandler,HTTPServer
import time

HOST_NAME="127.0.0.1"
PORT_NUMBER=8000

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()

    def do_GET(s):
        """Response do a GET"""
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Dummy server</title></head>"\
                .encode('utf-8'))
        s.wfile.write("<body><p>Dumb basic server</p>"\
                .encode('utf-8'))
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write(("<p>You accessed path: </p>"+s.path)\
                .encode('utf-8'))
        s.wfile.write("</body></html>"
                .encode('utf-8'))

def main():
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(str(time.asctime())+" Server Starts - %s:%s"%(HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server interrupted")
        pass
    httpd.server_close()
    print(str(time.asctime())+"Server Stops - %s:%s" %\
            (HOST_NAME, PORT_NUMBER))

if __name__== "__main__":
    main()
