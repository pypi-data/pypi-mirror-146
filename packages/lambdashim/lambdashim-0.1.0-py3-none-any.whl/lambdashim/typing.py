import types
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence, Tuple, Union

__all__ = [
    "Environ",
    "ExcInfo",
    "ResponseHeaders",
    "ResponseStream",
    "StartResponse",
    "StartResponseCallable",
    "StartResponseCallableWithExcInfo",
    "WriteCallable",
    "WsgiApplication",
]


# https://www.python.org/dev/peps/pep-3333/#the-write-callable
WriteCallable = Callable[[bytes], Any]

# https://docs.python.org/3/library/sys.html#sys.exc_info
ExcInfo = Tuple[type, BaseException, types.TracebackType]

ResponseHeaders = Sequence[Tuple[str, str]]

# https://www.python.org/dev/peps/pep-3333/#the-start-response-callable
StartResponseCallable = Callable[
    [
        str,  # status
        ResponseHeaders,  # response headers
    ],
    WriteCallable  # write() callable
]
StartResponseCallableWithExcInfo = Callable[
    [
        str,  # status
        ResponseHeaders,  # response headers
        Optional[ExcInfo]  # exc_info
    ],
    WriteCallable  # write() callable
]
StartResponse = Union[StartResponseCallable, StartResponseCallableWithExcInfo]

# https://www.python.org/dev/peps/pep-3333/#environ-variables
Environ = Mapping[str, object]

# https://www.python.org/dev/peps/pep-3333/#buffering-and-streaming
ResponseStream = Iterable[bytes]

# https://www.python.org/dev/peps/pep-3333/#specification-details
WsgiApplication = Callable[
    [
        Environ,  # environ
        StartResponse,  # start_response() function
    ],
    ResponseStream  # bytestring chunks
]