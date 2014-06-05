# Simple RTSP Client #

Simple python rtsp client.(inspired by [requests](https://github.com/kennethreitz/requests))

It's simple like,

    >>> r = rtsp.describe("rtsp://172.16.41.59:80/test.mpg")
    >>> r.status_code
    200
    >>> r.headers["content-type"]
    'application/sdp'
    >>> r.content
    ...

## Features

- Support RTSP Describe, Setup and Get_parameter
- Support Session
- Support verbose mode with SMS-like text UI
![rtsp_verbose.png](https://bitbucket.org/repo/bAakbo/images/1912345104-rtsp_verbose.png)

## Installation

no install script yet
