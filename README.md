# pyrtsp

python rtsp for humans.

Simple rtsp client, inspired by [requests](https://github.com/kennethreitz/requests)

It's simple like,

```python
>>> r = pyrtsp.describe("rtsp://172.16.41.59:80/test.mpg")
>>> r.status_code
200
>>> r.headers["content-type"]
'application/sdp'
>>> r.content
...
```

and, has a verbose mode.
```python
>>> pyrtsp.describe("rtsp://172.16.41.59:80/1_vod.mpg", verbose=True)
                               ----------------------------------------------------
                              | DESCRIBE rtsp://172.16.41.59:80/1_vod.mpg RTSP/1.0 |
                              |                                            CSeq: 0 |
                              |                                                    |
                              |                                                    \
                               ----------------------------------------------------
 -----------------------------------------------
| RTSP/1.0 200 OK                               |
| CSeq: 0                                       |
| Content-Type: application/sdp                 |
| Content-Length: 171                           |
|                                               |
| v=0                                           |
| o=- 1406079985 1406079985 IN IP4 172.16.41.59 |
| s=CastisVod                                   |
| c=IN IP4 172.16.41.59                         |
| t=0 0                                         |
| a=control:*                                   |
| a=range:npt=0-60.164000;bytes=0-5620824       |
| m=video 0 RTP/AVP 33                          |
/                                               |
 -----------------------------------------------
<session.Response instance at 0x7f309f54a5a8>
>>>
```
## Features

- Support RTSP methods including Describe, Setup and Get_parameter
- Support Session with keep-alive socket
- Support verbose mode with SMS-like text UI

## Installation

soon





