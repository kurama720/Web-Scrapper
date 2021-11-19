from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from uuid import uuid4

from scrapper.logger import create_logger

jsoned_records = []

LOGGER = create_logger()

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.record_data()
        self.make_ids()

        if self.path == '/posts':
            if len(jsoned_records) == 0:
                self.send_response(404)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                for data in jsoned_records:
                    self.wfile.write(data.encode())

        elif self.path.removeprefix('/posts/') in self.make_ids():
            output = ''
            for data in jsoned_records:
                if self.path.removeprefix('/posts/') in json.loads(data)['UNIQUE ID']:
                    output += data
                    if output == '':
                        self.send_response(404)
                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/json')
                        self.end_headers()
                        self.wfile.write(output.encode())
        else:
            self.send_response(404)

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        content = self.rfile.read(content_len).decode()
        content = json.loads(content)
        content['UNIQUE ID'] = str(uuid4())
        if content['UNIQUE ID'] not in self.make_ids():
            jsoned_records.append(json.dumps(content))
            with open(self.record_data(), 'a', encoding='utf-8') as f:
                f.write(json.dumps(content))
            raw_number = 0
            with open(self.record_data(), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if content['UNIQUE ID'] in line:
                        raw_number += len(lines)
            output = {content['UNIQUE ID']: raw_number}
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())
        else:
            self.wfile.write('Record with such id exists already'.encode())

    def do_PUT(self):
        if self.path.removeprefix('/posts/') not in self.make_ids():
            self.send_response(404)
        else:
            content_len = int(self.headers.get('Content-Length'))
            content = self.rfile.read(content_len).decode()
            for record in jsoned_records:
                if self.path.removeprefix('/posts/') == json.loads(record)['UNIQUE ID']:
                    place = jsoned_records.index(record)
                    for key, new_value in json.loads(content).items():
                        updated_record = self.update_record(record, key, new_value)
                        jsoned_records.remove(record)
                        jsoned_records.insert(place, json.dumps(updated_record))
                    self.record_data()
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()

    def do_DELETE(self):
        if self.path.removeprefix('/posts/') not in self.make_ids():
            self.send_response(404)
        else:
            for record in jsoned_records:
                if self.path.removeprefix('/posts/') in json.loads(record)['UNIQUE ID']:
                    jsoned_records.remove(record)
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()

    @staticmethod
    def update_record(old_record, key, new_value):
        old_record = json.loads(old_record)
        for k, v in old_record.items():
            if k == key:
                old_record[k] = new_value
                return old_record

    @staticmethod
    def record_data():
        current_datetime = datetime.now()
        # Create appropriate file name
        file_name = 'reddit-{year}-{month}-{day}.json'.format(
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
        ids_list = []
        for record in jsoned_records:
            record = json.loads(record)
            ids_list.append(record['UNIQUE ID'])
        return ids_list


def main():
    port = 8087
    server = HTTPServer(('', port), Server)
    LOGGER.info('Server running on port: %s' % port)
    server.serve_forever()


main()
