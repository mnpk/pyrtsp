#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rtsp
import unittest

class RTSPTest(unittest.TestCase):
	def test_describe(self):
		r = rtsp.describe('rtsp://172.16.41.59:80/1_vod.mpg')
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

	def test_setup(self):
		headers = {'Transport': 'RTP/AVP;unicast;destination=172.16.33.233;client_port=5000'}
		r = rtsp.setup('rtsp://172.16.41.59:80/1_vod.mpg', headers=headers)
		self.assertEqual('RTSP/1.0 200 OK', r.status_line)

if __name__ == '__main__':
	unittest.main()
