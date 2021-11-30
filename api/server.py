"""Module is used for running server and processing request methods: GET, POST, PUT, DELETE"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import List

from pymongo.errors import DuplicateKeyError

from scrapper.logger import create_logger
from database.db_requests import insert_record, find_record, update_record, delete_record

LOGGER = create_logger()


class Server(BaseHTTPRequestHandler):
    """Server itself. All request methods implemented here"""

    # Process GET request method
    def do_GET(self):
        if self.path == '/posts/':
            # Find all documents in db with find_document()
            total_posts: List[dict] = find_record()
            if len(total_posts) == 0:
                self.send_response(404)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                for data in total_posts:
                    self.wfile.write(json.dumps(data).encode())
        else:
            try:
                # Find a document with given id
                one_post = find_record(self.path.split('/posts/')[-1])
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(one_post).encode())
            except TypeError:
                self.send_response(404)

    # Process POST request method
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        content: dict = json.loads(self.rfile.read(content_len).decode())
        try:
            # Process POST method with db request
            insert_record(content)
            # Get post_id of inserted record
            posted_record: dict = find_record(content['post_id'])
            # Create dict with post_id and row
            output: dict = {posted_record['_id']: len(find_record())}
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())
        except DuplicateKeyError:
            self.send_response(404)

    # Process PUT request method
    def do_PUT(self):
        try:
            content_len = int(self.headers.get('Content-Length'))
            content: dict = json.loads(self.rfile.read(content_len).decode())
            # Update document
            update_record(self.path.split('/posts/')[-1], content)
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except TypeError:
            self.send_response(404)

    # Process DELETE request method
    def do_DELETE(self):
        # Delete document
        try:
            delete_record(self.path.split('/posts/')[-1])
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except TypeError:
            self.send_response(404)


def run_server():
    """Set ip address and port. Run server"""
    server = HTTPServer(('', 8087), Server)
    LOGGER.info('Server running on port: 8087')
    server.serve_forever()


run_server()
