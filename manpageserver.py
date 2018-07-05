#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess

PORT_NUMBER = 6969

# This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        # zcat /usr/share/man/man1/grep.1.gz  | groff -mandoc -Thtml
        command = self.path[1:]
        # print 'command: ' + command
        manpage_file = subprocess.Popen("man -w " + command, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
        # print 'manpage_file: ' + manpage_file
        generate_html = "zcat " + manpage_file + " | groff -mandoc -Thtml"
        # print 'generate_html: ' + generate_html
        output = subprocess.Popen(generate_html, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
        self.wfile.write(output)
        return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port' , PORT_NUMBER
    
    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
