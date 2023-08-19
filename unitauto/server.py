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
import coverage

from unitauto import methodutil
from unitauto.methodutil import null, true, false, to_json_str, list_method, invoke_method, KEY_PACKAGE, KEY_CLASS, \
    KEY_CONSTRUCTOR, KEY_CLASS_ARGS, KEY_THIS, KEY_METHOD, KEY_METHOD_ARGS, KEY_TYPE, KEY_VALUE, KEY_RETURN, KEY_KEY, \
    KEY_ASYNC, KEY_CALLBACK

import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from functools import partial
import os


CHARSET = 'uft-8'
HOST = ('localhost', 8083)

RESPONSE_CODE_SUCCESS = 200
KEY_CONTENT_TYPE = 'Content-Type'
KEY_CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'application/json; charset=UTF-8'


COVERAGE = coverage.coverage()


class Request(SimpleHTTPRequestHandler):
    timeout = 5
    server_version = "Apache"

    def send_headers(self, origin, method='POST', content_type: str = CONTENT_TYPE):
        if methodutil.not_empty(content_type):
            self.send_header(KEY_CONTENT_TYPE, content_type)
        self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,content-type')
        self.send_header('Access-Control-Allow-Methods', 'POST,GET,OPTIONS')
        self.send_header('Access-Control-Request-Method', method)

        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/coverage/'):
            self.do_POST()
            return

        super().do_GET()

    def do_OPTIONS(self):
        self.do_POST()

    def do_POST(self):
        method = self.command
        client_address = self.client_address
        host = 'http://' + client_address[0] + ':' + str(client_address[1])
        path = self.path
        print(method + ' ' + host + path)
        # if path not in ['/method/list', '/method/invoke']:
        #     raise Exception('only support /method/list, /method/invoke')

        origin = self.headers.get('origin') or self.headers.get('Origin') or 'http://apijson.cn'

        if method == 'OPTIONS':
            self.send_response(RESPONSE_CODE_SUCCESS)
            self.send_headers(origin, method)
            # self.wfile.write('ok'.encode())
            return

        cl = self.headers.get(KEY_CONTENT_LENGTH)
        bs = self.rfile.read(0 if methodutil.is_empty(cl) else int(cl))
        req = null if bs is None else bs.decode()  # bs.decode(CHARSET)
        # req = urllib.unquote(bs).decode(CHARSET, 'ignore')

        wfile = self.wfile

        if path.startswith('/coverage/'):
            res = {
                methodutil.KEY_CODE: methodutil.CODE_SUCCESS,
                methodutil.KEY_MSG: methodutil.MSG_SUCCESS
            }
            res_str = to_json_str(res)

            if path == '/coverage/start':
                try:
                    COVERAGE.stop()
                except Exception as e:
                    print(e)

                COVERAGE.start()
            elif path == '/coverage/stop':
                COVERAGE.stop()
            elif path == '/coverage/save':
                COVERAGE.save()
            else:
                if path == '/coverage/report':
                    res['coverage'] = COVERAGE.report()
                    res['url'] = '/htmlcov/index.html'
                    try:
                        COVERAGE.json_report()
                        f = open('coverage.json', 'r')
                        t = f.read()
                        try:
                            res['json'] = json.loads(t)
                        except Exception as e:
                            print(e)
                            res['json'] = t
                    except Exception as e:
                        print(e)

                    try:
                        COVERAGE.html_report()
                        f = open('htmlcov/index.html', 'r')
                        res['html'] = f.read()
                        # res['html'] = '../htmlcov/index.html'  # f.read()
                    except Exception as e:
                        print(e)

                    res_str = to_json_str(res)
                elif path == '/coverage/index.html':
                    self.send_response(301)
                    self.send_header('Location', host + '/unitauto-py/htmlcov/index.html')
                else:
                    COVERAGE.html_report()

                    ind = methodutil.index(path, '/')
                    f = open('../htmlcov/' + path[ind+1:], 'r')
                    res_str = f.read()
                    self.send_headers(origin, method, content_type='text/html')
                    wfile.write(res_str.encode())
                    return

            self.send_response(RESPONSE_CODE_SUCCESS)
            self.send_headers(origin, method)
            wfile.write(res_str.encode())
            return

        done = [false]

        def callback(res):
            res_str = to_json_str(res)
            res_byte = res_str.encode()
            self.send_response(RESPONSE_CODE_SUCCESS)
            self.send_headers(origin, method)
            if done[0] or wfile is None or wfile.closed:
                return

            wfile.write(res_byte)
            done[0] = true
            try:
                wfile.close()
            except BaseException as e:
                # print(e)
                pass
            # cause error 'unresolved reference'  wfile = null

        if path == '/method/list':
            rsp = list_method(req)
            callback(rsp)
        elif path == '/method/invoke':
            invoke_method(req, callback)
            while true:
                if done[0]:
                    break


def start(host=HOST):
    wk_dir = os.getcwd()
    Request.extensions_map = {
        k: v + ';charset=UTF-8' for k, v in Request.extensions_map.items()
    }

    # server = HTTPServer(host, Request)
    # # print("Starting server, listen at: %s:%s" % host)
    # server.serve_forever()
    # server.server_bind()
    # print('http://localhost:8083/')

    http.server.test(Request, port=host[1])  # HandlerClass=partial(SimpleHTTPRequestHandler, directory=wk_dir + '/htmlcov'), port=8083, bind='')


def test():
    rsp0 = invoke_method({
        KEY_PACKAGE: 'unitauto.test',
        KEY_METHOD: 'test'
    })
    print('\nunitauto.test.test() = \n' + to_json_str(rsp0))

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
    print('\nunitauto.test.testutil.minus(2, 3) = \n' + to_json_str(rsp1))

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
    print('\nunitauto.test.testutil.Test.get_id() = \n' + to_json_str(rsp2))

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
    print('\nunitauto.test.testutil.Test.get_name() = \n' + to_json_str(rsp3))

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
    print('\nunitauto.test.testutil.Test.get_sex_str() = \n' + to_json_str(rsp4))

    rsp5 = invoke_method({
        KEY_ASYNC: true,
        KEY_PACKAGE: 'unitauto.test',
        KEY_CLASS: 'testutil',
        KEY_METHOD: 'async_test',
        KEY_METHOD_ARGS: [
            {
                KEY_TYPE: 'int',
                KEY_VALUE: 2
            },
            {
                KEY_TYPE: 'int',
                KEY_VALUE: 5
            }
        ]
    })
    print('\nunitauto.test.testutil.async_test(2, 5) = \n' + to_json_str(rsp5))

    def callback(rsp):
        print('unitauto.test.testutil.compute_async(2, 5, callback) = \n' + to_json_str(rsp))

    rsp6 = invoke_method({
        KEY_PACKAGE: 'unitauto.test',
        KEY_CLASS: 'testutil',
        KEY_METHOD: 'compute_async',
        KEY_METHOD_ARGS: [
            {
                # KEY_KEY: 'a',
                KEY_TYPE: 'int',
                KEY_VALUE: 2
            },
            {
                # KEY_KEY: 'b',
                KEY_TYPE: 'int',
                KEY_VALUE: 5
            },
            {
                KEY_KEY: 'callback',
                KEY_TYPE: 'def(a,b)',
                KEY_VALUE: {
                    KEY_TYPE: 'int',
                    KEY_RETURN: 'a - b',
                    KEY_CALLBACK: true
                }
            }
        ]
    }, callback)
    print('\nunitauto.test.testutil.compute_async(2, 5, callback) = \n' + to_json_str(rsp6))


if __name__ == '__main__':
    test()
    start()

