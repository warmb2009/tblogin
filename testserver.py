# -*- coding:utf-8 -*-

from http.server import HTTPServer,BaseHTTPRequestHandler  
import io,shutil  
import cgi
from tbinfo import *
from config import PID


class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
            }
        )

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes('Client: %s\n' % str(self.client_address), encoding='utf-8'))
        self.wfile.write(bytes('Path: %s\n' % self.path, encoding='utf-8'))
        self.wfile.write(b'Form data:\n')
        print(self.client_address)
        print(self.path)

        # Echo back information about what was posted in the form
        if self.path == '/ajax/tbadd/':
            name = form['name'].value
            sender = form['sender'].value
            content = form['content'].value
            print('名称:', name)
            print('发送:', sender)
            print('内容:',content)
            
            dic = get_commodity_info(content, PID)
            if dic is not False:
                print('字典:', dic)
            else:
                print('error of get info')
        else:
            print(self.path, ' not recognize')
            print('|', self.path.strip(), '|')
        return 'success'


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8081), PostHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
