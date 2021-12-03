"""Module is used for running server and processing request methods: GET, POST, PUT, DELETE"""
from typing import List
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from psycopg2 import errors
from pymongo.errors import DuplicateKeyError

from scrapper.logger import create_server_logger
from database.db_mongo.db_requests import insert_record, find_record, update_record, delete_record


# Import a duplicate primary key exception
UniqueViolationError = errors.lookup('23505')
LOGGER = create_server_logger()


class Server(BaseHTTPRequestHandler):
    """Server itself. All request methods implemented here"""

    # Process GET request method
    def do_GET(self):
        if self.path == '/posts/':
            try:
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
            except Exception as ex:
                self.send_response(404)
                LOGGER.error(f"{ex}")
        else:
            try:
                # Find a document with given id
                one_record = find_record(self.path.split('/posts/')[-1])
                if one_record is None:
                    self.send_response(404)
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(one_record).encode())
            except TypeError:
                self.send_response(404)
            except Exception as ex:
                self.send_response(404)
                LOGGER.error(f"{ex}")

    # Process POST request method
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        content: dict = json.loads(self.rfile.read(content_len).decode())
        if '_id' not in content.keys():
            self.send_response(404)
        try:
            # Process POST method with db request
            insert_record(content)
            # Create dict with post_id and row
            output: dict = {content['_id']: len(find_record())}
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())
        except (DuplicateKeyError, TypeError, UniqueViolationError):
            self.send_response(404)
        except (KeyError, IndexError):
            self.send_response(404)
            LOGGER.error("Wrong field or a required field is missing")
        except Exception as ex:
            self.send_response(404)
            LOGGER.error(f"{ex}")

    # Process PUT request method
    def do_PUT(self):
        try:
            content_len = int(self.headers.get('Content-Length'))
            content: dict = json.loads(self.rfile.read(content_len).decode())
            # Update document
            # Process PUT method with db request
            update_record(self.path.split('/posts/')[-1], content)
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except TypeError:
            self.send_response(404)
        except KeyError:
            self.send_response(404)
            LOGGER.error("Wrong field")
        except Exception as ex:
            self.send_response(404)
            LOGGER.error(f"{ex}")

    # Process DELETE request method
    def do_DELETE(self):
        try:
            delete_record(self.path.split('/posts/')[-1])
            self.send_response(201)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
        except TypeError:
            self.send_response(404)
        except Exception as ex:
            self.send_response(404)
            LOGGER.error(f"{ex}")


def run_server():
    server = HTTPServer(('', 8087), Server)
    LOGGER.info('Server running on port: 8087')
    server.serve_forever()


run_server()
