"""Module is used for running server and processing request methods: GET, POST, PUT, DELETE"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from scrapper.logger import create_logger
from database.db_requests import insert_record, find_record, update_record, delete_record

posted_records = []

LOGGER = create_logger()


class Server(BaseHTTPRequestHandler):
    """Server itself. All request methods implemented here"""

    # Process GET request method
    def do_GET(self):
        if not find_record(all_records=True):
            self.send_response(404)
        else:
            if self.path == '/posts':
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                for data in find_record(all_records=True):
                    self.wfile.write(json.dumps(data).encode())

            elif find_record(self.path.split('/posts/')[-1]):
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(find_record(self.path.split('/posts/')[-1])).encode())
            else:
                self.send_response(404)

    # Process POST request method
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        content = json.loads(self.rfile.read(content_len).decode())
        insert_record(content)
        record_id = find_record(all_records=True)[-1]['UNIQUE ID']
        raw_number = len(find_record(all_records=True))
        output = {record_id: raw_number}
        self.send_response(201)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(json.dumps(output).encode())

    # Process PUT request method
    def do_PUT(self):
        if not find_record(self.path.split('/posts/')[-1]):
            self.send_response(404)
        else:
            content_len = int(self.headers.get('Content-Length'))
            content = json.loads(self.rfile.read(content_len).decode())
            update_record(self.path.split('/posts/')[-1], content)
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()

    # Process DELETE request method
    def do_DELETE(self):
        if not find_record(self.path.split('/posts/')[-1]):
            self.send_response(404)
        else:
            delete_record(self.path.split('/posts/')[-1])
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()


def main():
    server = HTTPServer(('', 8087), Server)
    LOGGER.info('Server running on port: 8087')
    server.serve_forever()


main()
