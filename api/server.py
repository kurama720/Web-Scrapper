from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from uuid import uuid4
import re

import scrapper.main

FIELDS = ['UNIQUE ID', 'POST URL', 'AUTHOR', 'USER KARMA', 'CAKE DAY', 'COMMENTS NUMBER', 'VOTES NUMBER',
          'POST CATEGORY', 'POST KARMA', 'COMMENT KARMA', 'POST DATE']

jsoned_records = []


def get_data():
    for record in scrapper.main.recording_data:
        i = 0
        dict_record = {}
        while i < len(FIELDS):
            dict_record[FIELDS[i]] = record[i]
            i = i + 1
        jsoned_records.append(dict_record)


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.record_data()
        self.make_ids()
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
            self.wfile.write(response_content)

        elif self.path.removeprefix('/posts/') in self.make_ids():
            self.send_response(200)
            head = f'<html><body>'
            for record in jsoned_records:
                if self.path.removeprefix('/posts/') in record['UNIQUE ID']:
                    section += '<p>'
                    section += json.dumps(record)
                    section += '</p>'
            if section == '':
                section += '<p>No record with such id</p>'
            response_content = head.encode() + section.encode() + footer.encode()
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_content)
        else:
            self.send_response(404)

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        content = self.rfile.read(content_len).decode().replace('+', ' ').split('&')
        income_data = {'UNIQUE ID': str(uuid4()),
                       'POST URL': [i.removeprefix('POST_URL=') for i in content if 'POST_URL' in i][0],
                       'AUTHOR': [i.removeprefix('AUTHOR=') for i in content if 'AUTHOR' in i][0],
                       'USER KARMA': [i.removeprefix('USER KARMA=') for i in content if 'USER KARMA' in i][0],
                       'CAKE DAY': [i.removeprefix('CAKE DAY=') for i in content if 'CAKE DAY' in i][0],
                       'COMMENTS NUMBER': [i.removeprefix('COMMENTS NUMBER=') for i in content if 'COMMENTS NUMBER'
                                           in i][0],
                       'VOTES NUMBER': [i.removeprefix('VOTES NUMBER=') for i in content if 'VOTES NUMBER' in i][0],
                       'POST CATEGORY': [i.removeprefix('POST CATEGORY=') for i in content if 'POST CATEGORY'
                                         in i][0],
                       'POST KARMA': [i.removeprefix('POST KARMA=') for i in content if 'POST KARMA' in i][0],
                       'COMMENT KARMA': [i.removeprefix('COMMENT KARMA=') for i in content if 'COMMENT KARMA'
                                         in i][0],
                       'POST DATE': [i.removeprefix('POST DATE=') for i in content if 'POST DATE' in i][0]
                       }
        if income_data['UNIQUE ID'] not in self.make_ids():
            jsoned_records.append(income_data)
            with open(self.record_data(), 'a', encoding='utf-8') as f:
                f.write(str(income_data))
            raw_number = 0
            with open(self.record_data(), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if income_data['UNIQUE ID'] in line:
                        raw_number += len(lines)
            output = {income_data['UNIQUE ID']: raw_number}
            self.send_response(201)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())
        else:
            self.wfile.write('Record with such id exists already'.encode())

    def do_PUT(self):
        if self.path.removeprefix('/posts/') not in self.make_ids():
            self.send_response(404)
        else:
            content_len = int(self.headers.get('Content-Length'))
            content = self.rfile.read(content_len).decode().replace('+', ' ').split('&')
            for record in jsoned_records:
                if self.path.removeprefix('/posts/') == record['UNIQUE ID']:
                    if re.search('POST URL', str(content)) is not None:
                        record['POST URL'] = [i.removeprefix('POST_URL=') for i in content if 'POST_URL' in i][0]
                    if re.search('AUTHOR', str(content)) is not None:
                        record['AUTHOR'] = [i.removeprefix('AUTHOR=') for i in content if 'AUTHOR' in i][0]
                    if re.search('USER KARMA', str(content)) is not None:
                        record['USER KARMA'] = [i.removeprefix('USER KARMA=') for i in content if 'USER KARMA' in i][0]
                    if re.search('CAKE DAY', str(content)) is not None:
                        record['CAKE DAY'] = [i.removeprefix('CAKE DAY=') for i in content if 'CAKE DAY' in i][0]
                    if re.search('COMMENTS NUMBER', str(content)) is not None:
                        record['COMMENTS NUMBER'] = [i.removeprefix('COMMENTS NUMBER=') for i in content if
                                                     'COMMENTS NUMBER' in i][0]
                    if re.search('VOTES NUMBER', str(content)) is not None:
                        record['VOTES NUMBER'] = [i.removeprefix('VOTES NUMBER=') for i in content if 'VOTES NUMBER'
                                                  in i][0]
                    if re.search('POST CATEGORY', str(content)) is not None:
                        record['POST CATEGORY'] = [i.removeprefix('POST CATEGORY=') for i in content if 'POST CATEGORY'
                                                   in i][0]
                    if re.search('POST KARMA', str(content)) is not None:
                        record['POST KARMA'] = [i.removeprefix('POST KARMA=') for i in content if 'POST KARMA' in i][0]
                    if re.search('COMMENT KARMA', str(content)) is not None:
                        record['COMMENT KARMA'] = [i.removeprefix('COMMENT KARMA=') for i in content if 'COMMENT KARMA'
                                                   in i][0]
                    if re.search('POST DATE', str(content)) is not None:
                        record['POST DATE'] = [i.removeprefix('POST DATE=') for i in content if 'POST DATE' in i][0]
                    self.record_data()
            self.send_response(201)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def do_DELETE(self):
        if self.path.removeprefix('/posts/') not in self.make_ids():
            self.send_response(404)
        else:
            for record in jsoned_records:
                if self.path.removeprefix('/posts/') in record['UNIQUE ID']:
                    jsoned_records.remove(record)
            self.send_response(201)
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

    @staticmethod
    def make_ids():
        ids_list = [record['UNIQUE ID'] for record in jsoned_records]
        return ids_list


def main():
    get_data()
    ip = 'localhost'
    port = 8087
    server = HTTPServer(('', port), Server)
    print('Server running on %s:%s' % (ip, port))
    server.serve_forever()


main()
