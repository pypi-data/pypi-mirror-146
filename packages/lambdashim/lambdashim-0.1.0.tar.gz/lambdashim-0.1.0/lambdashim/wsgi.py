import base64
import sys
from dataclasses import dataclass, field
from io import StringIO, BytesIO
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

from .typing import Environ, ExcInfo, ResponseStream, ResponseHeaders, WriteCallable, WsgiApplication

__all__ = [
    "LambdaWSGI",
    "StartResponse",
    "environ",
]


def convert_str(s: Union[bytes, str]) -> str:
    """convert bytes to string, if required"""
    try:
        return s.decode("utf-8")
    except UnicodeDecodeError:
        return s


@dataclass(frozen=True)
class LambdaWSGI:
    app: WsgiApplication

    def handle(self, event: Dict[str, Any], context: Dict[str, Any]):
        sr = StartResponse()
        output = self.app(environ(event, context), sr)
        return sr.response(output)


@dataclass
class StartResponse:
    status: str = "500"
    headers: ResponseHeaders = field(default_factory=list)
    body: StringIO = field(default_factory=StringIO)

    def __call__(self, status: str, headers: ResponseHeaders, exc_info: Optional[ExcInfo] = None) -> WriteCallable:
        self.status = status.split()[0]
        self.headers[:] = headers
        return self.body.write

    def response(self, output: ResponseStream) -> Dict[str, str]:
        headers = dict(self.headers)
        if headers.get("Content-Type") in ["image/png", "image/gif", "application/octet-stream"]:
            is_base64 = True
            body = base64.b64encode(b"".join(output)).decode("ascii")
        else:
            is_base64 = False
            body = self.body.getvalue() + "".join(map(convert_str, output))
        return {
            "statusCode": str(self.status),
            "headers": headers,
            "body": body,
            "isBase64Encoded": is_base64,
        }


def environ(event: Dict[str, Any], context: Dict[str, Any]) -> Environ:
    body = b""
    str_body = event.get("body")
    if str_body:
        body = bytes(str_body, "utf-8")
    env = {
        "REQUEST_METHOD": event["httpMethod"],
        "SCRIPT_NAME": "",
        "PATH_INFO": event["path"],
        "QUERY_STRING": urlencode(event["queryStringParameters"] if "queryStringParameters" in event else {}),
        "REMOTE_ADDR": "127.0.0.1",
        "CONTENT_LENGTH": str(len(body) or ''),
        "HTTP": "on",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.input": BytesIO(body),
        "wsgi.errors": sys.stderr,
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
    }
    headers = event.get("headers", {})
    if headers:
        for k, v in headers.items():
            k = k.upper().replace("-", "_")

            if k == "CONTENT_TYPE":
                env["CONTENT_TYPE"] = v
            elif k == "HOST":
                env["SERVER_NAME"] = v
            elif k == "X_FORWARDED_FOR":
                env["REMOTE_ADDR"] = v.split(", ")[0]
            elif k == "X_FORWARDED_PROTO":
                env["wsgi.url_scheme"] = v
            elif k == "X_FORWARDED_PORT":
                env["SERVER_PORT"] = v

            env["HTTP_" + k] = v

    return env
