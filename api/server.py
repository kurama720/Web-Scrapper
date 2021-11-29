"""Module is used for running server and processing request methods: GET, POST, PUT, DELETE"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import List

from pymongo.errors import DuplicateKeyError

from scrapper.logger import create_logger
from database.db_requests import insert_document, find_document, update_document, delete_document

LOGGER = create_logger()


class Server(BaseHTTPRequestHandler):
    """Server itself. All request methods implemented here"""

    # Process GET request method
    def do_GET(self):
        if self.path == '/posts/':
            # Find all documents in db with find_document()
            data_from_db: List[dict] = find_document({})
            if len(data_from_db) == 0:
                self.send_response(404)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                for data in data_from_db:
                    self.wfile.write(json.dumps(data).encode())
        else:
            try:
                # Find a document with given id
                one_post = find_document({'_id': self.path.split('/posts/')[-1]})
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
        # Insert a document
        try:
            insert_document(content)
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            # Find document with proper author name
            doc: dict = find_document({'author_name': content['author']})
            # Get id and row number of posted doc
            output: dict = {doc['_id']: len(find_document({}))}
            self.wfile.write(json.dumps(output).encode())
        except DuplicateKeyError:
            self.send_response(404)

    # Process PUT request method
    def do_PUT(self):
        content_len = int(self.headers.get('Content-Length'))
        content: dict = json.loads(self.rfile.read(content_len).decode())
        try:
            # Update document
            update_document({'_id': self.path.split('/posts/')[-1]}, content)
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except TypeError:
            self.send_response(404)

    # Process DELETE request method
    def do_DELETE(self):
        # Delete document
        try:
            delete_document({'_id': self.path.split('/posts/')[-1]})
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except TypeError:
            self.send_response(404)


def main():
    """Set ip address and port. Run server"""
    server = HTTPServer(('', 8087), Server)
    LOGGER.info('Server running on port: 8087')
    server.serve_forever()


main()
