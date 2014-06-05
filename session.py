import socket
from urlparse import urlparse
from view import MessageView
from idict import CaseInsensitiveDict

class Request:
	def __init__(self, method, url, headers=None):
		self.method = method
		self.url = url
		self.headers = CaseInsensitiveDict(headers)

	def string(self):
		string = "%s %s RTSP/1.0\r\n" % (self.method, self.url)
		string += ''.join(["%s: %s\r\n" % (key, self.headers[key]) for key in self.headers.keys()])
		string += '\r\n'
		return string

class Response:
	def __init__(self, header, body):
		if not header or not body:
			return
		self.status_line = header.split('\r\n')[0]
		self.rtsp_version, status_code, self.reason = self.status_line.split(' ', 2)
		self.status_code = int(status_code)
		headers = {}
		for line in header.split('\r\n')[1:]:
			if ':' in line:
				key, value = line.split(':', 1)
				headers[key] = value.strip()
		self.headers = CaseInsensitiveDict(headers)
		self.content = body
	def is_redirect(self):
		if self.status_code == 301:
			return True
		# hack for SRMserver
		if self.rtsp_version == 'REDIRECT':
			return True
		return False



class Session:
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.settimeout(0.5)
		self.view = MessageView()
		self.cseq = 0
		pass
	def request(self, method, url, headers={}, auto_redirect=True, verbose=False):
		try:
			self.s.connect((urlparse(url).hostname, urlparse(url).port));
			# print "connected to", urlparse(url).hostname, ":", urlparse(url).port
		except socket.error, msg:
			print "failed to connect:", msg
			return None
		headers['CSeq'] = self.cseq
		self.cseq += 1
		msg = Request(method, url, headers).string()
		self.s.send(msg)
		if verbose: self.view.send(msg)
		header = ''
		body = ''
		while True:
			try:
				data = self.s.recv(1024)
			except socket.timeout:
				# self.view.recv('receive timeout')
				break
			if not data: break
			if verbose: self.view.recv(data)
			header, body = data.split('\r\n\r\n', 1)
		r = Response(header, body)
		if auto_redirect and r.is_redirect():
			self.s.close()
			self.__init__()
			r = self.request(method, r.headers['location'], headers=headers, verbose=verbose)
		return r

	def describe(self, url, **kwargs):
		return request('DESCRIBE', url, **kwargs)

	def setup(self, url, **kwargs):
		return request('SETUP', url, **kwargs)

	def get_parameter(self, url, **kwargs):
		return request('GET_PARAMETER', url, **kwargs)
