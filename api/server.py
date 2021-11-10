from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from uuid import uuid4

import scrapper.main

FIELDS = ['UNIQUE ID', 'POST URL', 'AUTHOR', 'USER KARMA', 'CAKE DAY', 'COMMENTS NUMBER', 'VOTES NUMBER',
          'POST CATEGORY', 'POST KARMA', 'COMMENT KARMA', 'POST DATE']

jsoned_records = []


def get_data():
    # from scrapper.main import recording_data
    for record in scrapper.main.recording_data:
        i = 0
        dict_record = {}
        while i < len(FIELDS):
            dict_record[FIELDS[i]] = record[i]
            i = i + 1
        jsoned_records.append(dict_record)


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        status = 200
        head = ''
        section = ''
        if self.path == '/':
            response_content = '<h1>404 Not Found</h1>'.encode()

        if self.path == '/posts':
            head += '<html><body><h1>Records list</h1>'
            number = 1
            for data in jsoned_records:
                section += f"record {number}:"
                section += '<p>'
                section += json.dumps(data)
                section += '</p>'
                number += 1
            footer = '</body></html>'
            response_content = head.encode() + section.encode() + footer.encode()

        else:
            head += f'<html><body><h1>The record with the UNIQUE ID: {self.path.removeprefix("/posts/")}</h1>'
            for record in jsoned_records:
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
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.record_data()
        self.wfile.write(response_content)

    def do_POST(self):
        self.send_response(201)
        with open(self.record_data(), 'r', encoding='utf-8') as f:
            text = f.readlines()
            number = len(text) + 1
        dict_record = {'UNIQUE ID': str(uuid4()), 'RAW NUMBER': number}
        jsoned_records.append(dict_record)
        with open(self.record_data(), 'a', encoding='utf-8') as f:
            f.write(str(dict_record))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(dict_record).encode())

    def do_DELETE(self):
        self.send_response(201)
        for record in jsoned_records:
            if self.path.removeprefix('/posts/') in record['UNIQUE ID']:
                jsoned_records.remove(record)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @staticmethod
    def record_data():
        current_datetime = datetime.now()
        # Create appropriate file name
        file_name = 'reddit-{year}-{month}-{day}.txt'.format(
            year=current_datetime.year,
            month=current_datetime.month,
            day=current_datetime.day,
        )
        with open(file_name, 'w', encoding='utf8') as f:
            for i in jsoned_records:
                f.write(f"{str(i)}\n")
        with open('file_info.txt', 'w') as file:
            file.write(f"{file_name}\n")
            with open(file_name, 'r') as f:
                text = f.readlines()
                size = len(text)
            file.write(str(f"{size}\n"))

        return file_name


def main():
    get_data()
    ip = 'localhost'
    port = 8087
    server = HTTPServer(('', port), Server)
    print('Server running on %s:%s' % (ip, port))
    server.serve_forever()


main()
