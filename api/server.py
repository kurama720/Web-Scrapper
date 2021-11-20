"""Module is used for running server and processing request methods: GET, POST, PUT, DELETE"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from uuid import uuid4

from scrapper.logger import create_logger
from database.db_connection import posts_collection
from database.db_requests import insert_document, find_document, update_document, delete_document

LOGGER = create_logger()


class Server(BaseHTTPRequestHandler):
    """Server itself. All request methods implemented here"""

    # Process GET request method
    def do_GET(self):
        if len(find_document(posts_collection, {}, all_doc=True)) == 0:
            self.send_response(404)
        else:
            if self.path == '/posts':
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                for data in find_document(posts_collection, {}, all_doc=True):
                    self.wfile.write(json.dumps(data).encode())

            elif find_document(posts_collection, {'_id': self.path.split('/posts/')[-1]}):
                data = find_document(posts_collection, {'_id': self.path.split('/posts/')[-1]})
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            else:
                self.send_response(404)

    # Process POST request method
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        content = json.loads(self.rfile.read(content_len).decode())
        content['_id'] = str(uuid4())
        if find_document(posts_collection, content['_id']):
            self.send_response(404)
        else:
            insert_document(posts_collection, content)
            output = {content['_id']: len(find_document(posts_collection, {}, all_doc=True))}
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())

    # Process PUT request method
    def do_PUT(self):
        content_len = int(self.headers.get('Content-Length'))
        content = json.loads(self.rfile.read(content_len).decode())
        if find_document(posts_collection, {'_id': self.path.split('/posts/')[-1]}):
            update_document(posts_collection, {'_id': self.path.split('/posts/')[-1]}, content)
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        else:
            self.send_response(404)

    # Process DELETE request method
    def do_DELETE(self):
        if find_document(posts_collection, {'_id': self.path.split('/posts/')[-1]}):
            delete_document(posts_collection, {'_id': self.path.split('/posts/')[-1]})
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        else:
            self.send_response(404)


def main():
    """Set ip address and port. Run server"""
    server = HTTPServer(('', 8087), Server)
    LOGGER.info('Server running on port: 8087')
    server.serve_forever()


main()
