"""Module is used for running server and processing request methods: GET, POST, PUT, DELETE"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from psycopg2 import errors

from scrapper.logger import create_logger
from database.db_requests import insert_record, find_record, update_record, delete_record

posted_records = []

LOGGER = create_logger()
# Import a duplicate primary key exception
UniqueViolationError = errors.lookup('23505')


class Server(BaseHTTPRequestHandler):
    """Server itself. All request methods implemented here"""

    # Process GET request method
    def do_GET(self):
        if self.path == '/posts/':
            total_posts = find_record()
            if not total_posts:
                self.send_response(404)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                for data in total_posts:
                    self.wfile.write(json.dumps(data).encode())
        else:
            one_record = find_record(self.path.split('/posts/')[-1])
            if one_record is None:
                self.send_response(404)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(one_record).encode())

    # Process POST request method
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        content = json.loads(self.rfile.read(content_len).decode())
        try:
            insert_record(content)
            all_db_data = find_record()
            output = {all_db_data[-1]['post_id']: len(all_db_data)}
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())
        except UniqueViolationError:
            self.send_response(404)

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
