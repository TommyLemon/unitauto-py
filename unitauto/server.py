# encoding=utf-8
# MIT License
#
# Copyright (c) 2023 TommyLemon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
from unitauto import methodutil
from unitauto.methodutil import null, true, false, to_json_str, list_method, invoke_method, KEY_PACKAGE, KEY_CLASS, \
    KEY_CONSTRUCTOR, KEY_CLASS_ARGS, KEY_THIS, KEY_METHOD, KEY_METHOD_ARGS, KEY_TYPE, KEY_VALUE

from http.server import HTTPServer, BaseHTTPRequestHandler


CHARSET = 'uft-8'
HOST = ('localhost', 8083)

RESPONSE_CODE_SUCCESS = 200
KEY_CONTENT_TYPE = 'Content-Type'
KEY_CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'application/json; charset=UTF-8'


class Request(BaseHTTPRequestHandler):
    timeout = 5
    server_version = "Apache"

    def do_OPTIONS(self):
        self.do_POST()

    def do_POST(self):
        method = self.command
        client_address = self.client_address
        host = 'http://' + client_address[0] + ':' + str(client_address[1])
        path = self.path
        print(method + ' ' + host + path)
        if path not in ['/method/list', '/method/invoke']:
            raise Exception('only support /method/list, /method/invoke')

        origin = self.headers.get('origin') or self.headers.get('Origin') or 'http://apijson.cn'

        self.send_response(RESPONSE_CODE_SUCCESS)
        self.send_header(KEY_CONTENT_TYPE, CONTENT_TYPE)
        self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,content-type')
        self.send_header('Access-Control-Allow-Methods', 'POST,GET,OPTIONS')
        self.send_header('Access-Control-Request-Method', method)

        self.end_headers()

        if method == 'OPTIONS':
            # self.wfile.write('ok'.encode())
            return

        bs = self.rfile.read(int(self.headers[KEY_CONTENT_LENGTH]))
        req = bs.decode()  # bs.decode(CHARSET)
        # req = urllib.unquote(bs).decode(CHARSET, 'ignore')
        if path == '/method/list':
            rsp = list_method(req)
        else:
            rsp = invoke_method(req)

        rsp_str = to_json_str(rsp)
        self.wfile.write(rsp_str.encode())


def start(host=HOST):
    server = HTTPServer(host, Request)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()


def test():
    rsp0 = invoke_method({
        KEY_PACKAGE: 'unitauto.test',
        KEY_METHOD: 'test'
    })
    print('unitauto.test.test() = \n' + to_json_str(rsp0))

    rsp1 = invoke_method({
        KEY_PACKAGE: 'unitauto.test',
        KEY_CLASS: 'testutil',
        KEY_METHOD: 'minus',
        KEY_METHOD_ARGS: [
            {
                KEY_TYPE: 'int',
                KEY_VALUE: 2
            },
            {
                KEY_TYPE: 'int',
                KEY_VALUE: 3
            }
        ]
    })
    print('unitauto.test.testutil.minus(2, 3) = \n' + to_json_str(rsp1))

    rsp2 = invoke_method({
        KEY_PACKAGE: 'unitauto.test',
        KEY_CLASS: 'testutil$Test',
        KEY_CLASS_ARGS: [
            1,
            0,
            'UnitAuto'
        ],
        KEY_METHOD: 'get_id'
    })
    print('unitauto.test.testutil.Test.get_id() = \n' + to_json_str(rsp2))

    rsp3 = invoke_method({
        KEY_PACKAGE: 'unitauto.test',
        KEY_CLASS: 'testutil$Test',
        KEY_CONSTRUCTOR: 'get_test_instance',
        KEY_CLASS_ARGS: [
            2,
            1,
            'UnitAuto@Python'
        ],
        KEY_METHOD: 'get_name'
    })
    print('unitauto.test.testutil.Test.get_name() = \n' + to_json_str(rsp3))

    rsp4 = invoke_method({
        KEY_PACKAGE: 'unitauto.test',
        KEY_CLASS: 'testutil$Test',
        KEY_THIS: {
            KEY_TYPE: 'unitauto.test.testutil$Test',
            KEY_VALUE: {
                'id': 3,
                'sex': 1,
                'name': 'UnitAuto'
            }
        },
        KEY_METHOD: 'get_sex_str'
    })
    print('unitauto.test.testutil.Test.get_sex_str() = \n' + to_json_str(rsp4))


if __name__ == '__main__':
    test()
    start()

