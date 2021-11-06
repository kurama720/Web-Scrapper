from http.server import BaseHTTPRequestHandler, HTTPServer
from urls import urlpatterns
import json

import scrapper.main


FIELDS = ['UNIQUE ID', 'POST URL', 'AUTHOR', 'USER KARMA', 'CAKE DAY', 'COMMENTS NUMBER', 'VOTES NUMBER',
          'POST CATEGORY', 'POST KARMA', 'COMMENT KARMA', 'POST DATE']


def get_data():
    # from scrapper.main import recording_data
    list1 = []
    for record in scrapper.main.recording_data:
        i = 0
        dict2 = {}
        while i < len(FIELDS):
            dict2[FIELDS[i]] = record[i]
            i = i + 1
        list1.append(dict2)
    return list1


class Server(BaseHTTPRequestHandler):
    # sets basic headers for the server
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def handle_http(self):
        status = 200
        content_type = 'text/html'
        response_content = ''

        if self.path in urlpatterns:
            if self.path == '/posts':
                content_type = 'text/html'
                head = '<html><body><h1>Records list</h1>'
                number = 1
                section = ''
                for data in get_data():
                    section += f"record {number}:"
                    section += '<p>'
                    section += json.dumps(data)
                    section += '</p>'
                    number += 1
                footer = '</body></html>'
                response_content = head.encode() + section.encode() + footer.encode()
        else:
            content_type = 'text/html'
            response_content = '404 Not Found'.encode()

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return response_content

    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)


def main():
    ip = '127.0.0.1'
    port = 8087
    server = HTTPServer(('', port), Server)
    print('Server running on %s:%s' % (ip, port))
    server.serve_forever()


main()
