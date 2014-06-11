#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rtsplib
import unittest
import time

class RTSPTest(unittest.TestCase):
	def test_describe(self):
		r = rtsplib.describe('rtsp://172.16.41.59:80/frameidxtest.mpg', verbose=True)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

	def test_setup(self):
		headers = {'Transport': 'RTP/AVP;unicast;destination=172.16.33.233;client_port=5000'}
		s = rtsplib.Session()
		r = s.setup('rtsp://172.16.41.59:80/frameidxtest.mpg', headers=headers, verbose=True)
		# r = rtsplib.setup('rtsp://172.16.41.59:80/1_vod.mpg', headers=headers, verbose=True)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

		# r = s.get_parameter('rtsp://172.16.41.59:80/frameidxtest.mpg', verbose=True)
		# self.assertEqual('RTSP/1.0 200 OK', r.status_line)
        #
		r = s.get_parameter('rtsp://172.16.41.59:80/frameidxtest.mpg', verbose=True)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)
        #
		r = s.get_parameter('rtsp://172.16.41.59:80/frameidxtest.mpg', verbose=True, headers={'Media-Properties':'', 'Media-Range':''})
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

		r = s.get_parameter('rtsp://172.16.41.59:80/frameidxtest.mpg', contents='position\r\nsession_state\r\n\r\n', verbose=True)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

		r = s.get_parameter('rtsp://172.16.41.59:80/frameidxtest.mpg', verbose=True, headers={'Media-Properties':'', 'Media-Range':''}, contents='position\r\nsession_state\r\n\r\n')
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

if __name__ == '__main__':
	unittest.main()
