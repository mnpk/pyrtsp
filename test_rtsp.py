#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rtsplib
import unittest
import time

url = 'rtsp://172.16.41.59:80/frameidxtest.mpg'
# url = 'rtsp://172.16.41.59:80/1_vod.mpg'

class RTSPTest(unittest.TestCase):
	def test_describe(self):
		r = rtsplib.describe(url, verbose=True)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

	def test_setup(self):
		s = rtsplib.Session(verbose=True)

		headers = {'Transport': 'RTP/AVP;unicast;destination=172.16.33.233;client_port=5000'}
		r = s.setup(url, headers=headers)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

		r = s.get_parameter(url)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

		r = s.get_parameter(url, headers={'Media-Properties':'', 'Media-Range':''})
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

		r = s.get_parameter(url, contents='position\r\nsession_state\r\n\r\n')
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

		r = s.get_parameter(url, headers={'Media-Properties':'', 'Media-Range':''}, contents='position\r\nsession_state\r\n\r\n')
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

if __name__ == '__main__':
	unittest.main()
