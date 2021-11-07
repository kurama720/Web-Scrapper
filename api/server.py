from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import scrapper.main

FIELDS = ['UNIQUE ID', 'POST URL', 'AUTHOR', 'USER KARMA', 'CAKE DAY', 'COMMENTS NUMBER', 'VOTES NUMBER',
          'POST CATEGORY', 'POST KARMA', 'COMMENT KARMA', 'POST DATE']

list1 = []


def get_data():
    # from scrapper.main import recording_data
    for record in scrapper.main.recording_data:
        i = 0
        dict2 = {}
        while i < len(FIELDS):
            dict2[FIELDS[i]] = record[i]
            i = i + 1
        list1.append(dict2)


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
        section = ''

        if self.path == '/posts':
            head = '<html><body><h1>Records list</h1>'
            number = 1
            for data in list1:
                section += f"record {number}:"
                section += '<p>'
                section += json.dumps(data)
                section += '</p>'
                number += 1
            footer = '</body></html>'
            response_content = head.encode() + section.encode() + footer.encode()

        else:
            head = f'<html><body><h1>The record with the UNIQUE ID {self.path.removeprefix("/posts/")}</h1>'
            for record in list1:
                if self.path.removeprefix('/posts/') in record['UNIQUE ID']:
                    section += '<p>'
                    section += json.dumps(record)
                    section += '</p>'
                else:
                    continue
            if section == '':
                section += '404 Not found'
            footer = '</body></html>'
            response_content = head.encode() + section.encode() + footer.encode()

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return response_content

    def respond(self):
        content = self.handle_http()
        self.wfile.write(content)


def main():
    get_data()
    ip = 'localhost'
    port = 8087
    server = HTTPServer(('', port), Server)
    print('Server running on %s:%s' % (ip, port))
    server.serve_forever()


main()
