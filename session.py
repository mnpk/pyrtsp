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
	def __init__(self, lines=[]):
		if not lines:
			return
		self.status_line = lines[0]
		self.rtsp_version, self.status_code, self.reason = self.status_line.split(' ', 3)
		# self.method = lines[0].split()[0]
		headers = {}
		for line in lines[1:]:
			if ':' in line:
				key, value = line.split(':', 1)
				headers[key] = value.strip()
		self.headers = CaseInsensitiveDict(headers)
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
	def request(self, method, url, headers={}, auto_redirect=True, verbose=True):
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
		lines = []
		while True:
			try:
				data = self.s.recv(1024)
			except socket.timeout:
				# self.view.recv('receive timeout')
				break
			if not data: break
			if verbose: self.view.recv(data)
			for line in data.split('\r\n'):
				lines.append(line)
		r = Response(lines)
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