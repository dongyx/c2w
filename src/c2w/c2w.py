#!/usr/bin/env python3

"""c2w.py

convert a CLI programs to a web service

"""

__version__ = '0.0.1'

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import unquote
from tempfile import TemporaryFile
import subprocess
import argparse
import sys
import os

class WebifyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		global args

		progargs = []
		q = urlparse(self.path).query
		if q:
			progargs = [unquote(arg) for arg in q.split('&')]

		self.send_response(200)
		self.send_header('Content-Type', args.mime)
		self.end_headers()

		with subprocess.Popen([args.prog] + progargs,
			stdin=subprocess.PIPE,
			stdout=self.wfile
		) as sp:
			BLK_SZ = 1024
			remain = int(self.headers.get('Content-length', 0))

			while remain > 0:
				block = self.rfile.read(min(remain, BLK_SZ))
				if len(block) == 0:
					break
				sp.stdin.write(block)
				remain -= len(block)


	def do_POST(self):
		return self.do_GET()

def cgi():
	global args
	env = os.environ

	progargs = []
	q = env.get('QUERY_STRING', '')
	if q:
		progargs = [unquote(arg) for arg in q.split('&')]

	print(f'Content-Type: {args.mime}\r\n\r\n', end='', flush=True)
	subprocess.Popen([args.prog] + progargs).wait()

def main():
	global args

	parser = argparse.ArgumentParser(
		description='convert a CLI program to a Web service',
		epilog='author: DONG Yuxuan <http://dongyuxuan.me>',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)

	parser.add_argument('-m', '--mime', dest='mime', action='store',
		metavar='MIMETYPE', default='text/plain', help=' ')

	parser.add_argument('-H', '--host', dest='host', action='store',
		metavar='HOST', default='127.0.0.1', help='set the host c2w listens on. it has no effect if c2w runs as a CGI script.')

	parser.add_argument('-p', '--port', dest='port', action='store',
		metavar='PORT', type=int, default=8000, help='set the port c2w listens on. it has no effect if c2w runs as a CGI script.')

	parser.add_argument('-c', '--cgi', dest='cgi', action='store_true',
		help='run as a CGI script')

	parser.add_argument(dest='prog', metavar='PROGRAM')

	parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

	args = parser.parse_args()

	if args.cgi:
		cgi()
	else:
		print(f'Serving on {args.host}:{args.port}', file=sys.stderr)
		HTTPServer((args.host, args.port), WebifyHandler).serve_forever()

if __name__ == '__main__':
	main()
