import cgi
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from uuid import uuid4

import scrapper.main
from forms import form

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


IDS_LIST = [record['UNIQUE ID'] for record in jsoned_records]


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        section = ''
        footer = '</body></html>'

        if self.path == '/posts':
            self.send_response(200)
            head = '<html><body>'
            number = 1
            section = ''
            for data in jsoned_records:
                section += f"record {number}:"
                section += '<p>'
                section += json.dumps(data)
                section += '</p>'
                number += 1
            response_content = head.encode() + section.encode() + footer.encode()
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.record_data()
            self.wfile.write(response_content)

        elif self.path.removeprefix('/posts/') in IDS_LIST:
            self.send_response(200)
            head = f'<html><body>'
            for record in jsoned_records:
                if self.path.removeprefix('/posts/') in record['UNIQUE ID']:
                    section += '<p>'
                    section += json.dumps(record)
                    section += '</p>'
                else:
                    continue
            response_content = head.encode() + section.encode() + footer.encode()
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.record_data()
            self.wfile.write(response_content)

        elif self.path.removeprefix('/posts/') == 'new':
            self.send_response(200)
            head = '<html><body>'
            section += form
            response_content = head.encode() + section.encode() + footer.encode()
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.record_data()
            self.wfile.write(response_content)

        else:
            self.send_response(404)

    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
            pdict['boundary'] = bytes(pdict["boundary"], 'utf-8')
            fields = cgi.parse_multipart(self.rfile, pdict)
            income_data = {'UNIQUE ID': str(uuid4()), 'POST URL': fields.get('POST URL')[0],
                           'AUTHOR': fields.get('AUTHOR')[0], 'USER KARMA': fields.get('USER KARMA')[0],
                           'CAKE DAY': fields.get('CAKE DAY')[0], 'COMMENTS NUMBER': fields.get('COMMENTS NUMBER')[0],
                           'VOTES NUMBER': fields.get('VOTES NUMBER')[0],
                           'POST CATEGORY': fields.get('POST CATEGORY')[0], 'POST KARMA': fields.get('POST KARMA')[0],
                           'COMMENT KARMA': fields.get('COMMENT KARMA')[0], 'POST DATE': fields.get('POST DATE')[0]}
            if income_data['UNIQUE ID'] not in IDS_LIST:
                jsoned_records.append(income_data)
                with open(self.record_data(), 'a', encoding='utf-8') as f:
                    f.write(str(income_data))
                self.send_response(201)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                raw_number = 0
                with open(self.record_data(), 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if income_data['UNIQUE ID'] in line:
                            raw_number += len(lines)
                output = {income_data['UNIQUE ID']: raw_number}
                self.wfile.write(json.dumps(output).encode())
            else:
                raise ValueError

    def do_DELETE(self):
        self.send_response(200)
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
