"""WSGI entrypoint for the existing Rosebound application routes.

Waitress handles HTTP parsing, connection limits, timeouts and worker threads.
This adapter reuses the route layer without running the development HTTP server.
"""
from email.message import Message
from http import HTTPStatus
from io import BytesIO
import logging
import os
from server import Handler, connect

MAX_BODY = 24000

class Request(Handler):
    def __init__(self, environ, body):
        self.path = environ.get('PATH_INFO', '/')
        if environ.get('QUERY_STRING'):
            self.path += '?' + environ['QUERY_STRING']
        self.headers = Message()
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                self.headers[key[5:].replace('_', '-')] = value
        self.headers['Content-Type'] = environ.get('CONTENT_TYPE', '')
        self.headers['Content-Length'] = str(len(body))
        self.client_address = (environ.get('REMOTE_ADDR', 'unknown'), 0)
        self.rfile = BytesIO(body)
        self.wfile = BytesIO()
        self.status = 200
        self.response_headers = []

    def send_response(self, status, message=None):
        self.status = status
        self.response_headers = []

    def send_header(self, key, value):
        self.response_headers.append((key, str(value)))

    def end_headers(self):
        pass


def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')
    request = Request(environ, b'')
    try:
        if environ.get('PATH_INFO') == '/api/health' and method in ('GET', 'HEAD'):
            with connect() as db:
                db.execute('SELECT 1').fetchone()
            request.send(200, {'status': 'ok'})
        elif method in ('GET', 'HEAD'):
            request.do_GET()
        elif method == 'POST':
            size = int(environ.get('CONTENT_LENGTH') or 0)
            if size < 0 or size > MAX_BODY:
                request.send(413, {'error': 'Request too large'})
            else:
                request.rfile = BytesIO(environ['wsgi.input'].read(size))
                request.headers.replace_header('Content-Length', str(size))
                request.do_POST()
        else:
            request.send(405, {'error': 'Method not allowed'})
            request.send_header('Allow', 'GET, HEAD, POST')
    except Exception:
        logging.exception('Rosebound request failed')
        request.wfile = BytesIO()
        request.send(500, {'error': 'Something went wrong. Please try again.'})
    payload = request.wfile.getvalue()
    request.send_header('Content-Length', str(len(payload)))
    request.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
    request.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
    if os.environ.get('ROSEBOUND_SECURE_COOKIE') == '1':
        request.send_header('Strict-Transport-Security', 'max-age=31536000')
    start_response(f'{request.status} {HTTPStatus(request.status).phrase}', request.response_headers)
    return [b'' if method == 'HEAD' else payload]


if __name__ == '__main__':
    from waitress import serve
    serve(application, host='0.0.0.0', port=int(os.environ.get('PORT', '5001')),
          threads=4, max_request_body_size=MAX_BODY, channel_timeout=30,
          clear_untrusted_proxy_headers=True)
