import socket
from urlparse import urlparse
from view import MessageView
from idict import CaseInsensitiveDict

class Request:
	def __init__(self, method, url, headers=None, contents=''):
		self.method = method
		self.url = url
		self.headers = CaseInsensitiveDict(headers)
		self.contents = contents
		if contents:
			self.headers['Content-Length'] = len(contents)

	def string(self):
		string = "%s %s RTSP/1.0\r\n" % (self.method, self.url)
		string += ''.join(["%s: %s\r\n" % (key, self.headers[key]) for key in self.headers.keys()])
		string += '\r\n'
		if self.contents:
			string += self.contents
		return string

class Response:
	def __init__(self, header, body):
		if not header:
			return
		self.status_line = header.split('\r\n')[0]
		self.rtsp_version, self.status_code, self.reason = self.status_line.split(' ', 2)
		headers = {}
		for line in header.split('\r\n')[1:]:
			if ':' in line:
				key, value = line.split(':', 1)
				headers[key] = value.strip()
		self.headers = CaseInsensitiveDict(headers)
		self.contents = body
	def is_redirect(self):
		if self.status_code == '301':
			return True
		# hack for SRMserver
		if self.rtsp_version == 'REDIRECT':
			return True
		return False



class Session:
	def __init__(self, verbose=False):
		self.view = MessageView()
		self.verbose = verbose
		self.init_socket()

	def init_socket(self):
		self.cseq = 0
		self.s = None
		self.session = None

	def sendlog(self, msg):
		if self.verbose:
			self.view.send(msg)

	def recvlog(self, msg):
		if self.verbose:
			self.view.recv(msg)

	def connect(self, url):
		if self.s:
			return True
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.settimeout(0.5)
		try:
			self.s.connect((urlparse(url).hostname, urlparse(url).port));
			# print "connected to", urlparse(url).hostname, ":", urlparse(url).port
		except socket.error, msg:
			print "failed to connect:", msg
			return False
		return True

	def request(self, method, url, headers={}, auto_redirect=True, contents=''):
		self.connect(url)
		headers['CSeq'] = self.cseq
		self.cseq += 1
		if self.session:
			headers['Session'] = self.session.split(';')[0]
		msg = Request(method, url, headers, contents).string()
		self.s.sendall(msg)
		self.sendlog(msg)
		data = ''
		try:
			data_chunk = self.s.recv(2048)
			data += data_chunk
		except socket.error, e:
			print e
		if not data_chunk:
			self.recvlog('no data received')
		self.recvlog(data)
		if not data:
			return None
		response_header, response_body = data.split('\r\n\r\n', 1)
		r = Response(response_header, response_body)
		if auto_redirect and r.is_redirect():
			self.s.close()
			self.init_socket()
			return self.request(method, r.headers['location'], headers=headers)
		if 'session' in r.headers:
			self.session = r.headers['session']
		return r

	def describe(self, url, **kwargs):
		return self.request('DESCRIBE', url, **kwargs)

	def setup(self, url, **kwargs):
		return self.request('SETUP', url, **kwargs)

	def get_parameter(self, url, **kwargs):
		return self.request('GET_PARAMETER', url, **kwargs)
