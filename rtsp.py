from session import Session

def request(method, url, **kwargs):
	s = Session()
	return s.request(method, url, **kwargs)

def describe(url, **kwargs):
	return request('DESCRIBE', url, **kwargs)

def setup(url, **kwargs):
	return request('SETUP', url, **kwargs)

def get_parameter(url, **kwargs):
	return request('GET_PARAMETER', url, **kwargs)
