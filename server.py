from http.server import BaseHTTPRequestHandler, HTTPServer
import json


dict1 = {}
with open('scrapper/text.txt') as fh:
    for line in fh:
        command, description = line.strip().split(None, 1)
        dict1[command] = description.strip()

out_file = open("serialized.json", "w")
json.dump(dict1, out_file)
out_file.close()


class ServiceHandler(BaseHTTPRequestHandler):
    # sets basic headers for the server
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        # reads the length of the Headers
        length = int(self.headers['Content-Length'])
        # reads the contents of the request
        content = self.rfile.read(length)
        temp = str(content).strip('b\'')
        self.end_headers()
        return temp

    def do_GET(self):
        # defining all the headers
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        # prints all the keys and values of the json file
        self.wfile.write('Main page'.encode())
        # with open('serialized.json', 'r', encoding='utf8') as f:
        #     self.wfile.write(json.dumps(out_file).encode())


def main():
    ip = '127.0.0.1'
    port = 8087
    server = HTTPServer(('', port), ServiceHandler)
    print('Server running on %s:%s' % (ip, port))
    server.serve_forever()


if __name__ == '__main__':
    main()
