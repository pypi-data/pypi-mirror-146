from dacite import from_dict
from dataclasses import dataclass
import dateutil.parser
from typing import List, Optional

@dataclass
class HarResponseContent:
    mimeType: str
    size: int

@dataclass
class HarQueryString:
    name: str
    value: str

@dataclass
class HarHeaders:
    name: str
    value: str

@dataclass
class HarEntryRequest:
    method: str
    url: str
    queryString: List[HarQueryString]
    headersSize: int
    bodySize: int
    headers: List[HarHeaders]
    httpVersion: str

@dataclass
class HarEntryResponse:
    httpVersion: str
    redirectURL: str
    status: int
    statusText: str
    content: HarResponseContent
    headersSize: int
    bodySize: int
    headers: List[HarHeaders]
    _transferSize: int

@dataclass
class HarEntryTimings:
    blocked: float
    dns: float
    connect: float
    send: float
    wait: float
    receive: float
    ssl: float
    _queued: Optional[float]

@dataclass
class HarEntry:
    startedDateTime: str
    _requestId: str
    _initialPriority: str
    _priority: str
    pageref: str
    time: float
    request: HarEntryRequest
    response: HarEntryResponse
    connection: str
    serverIPAddress: str
    timings: HarEntryTimings
    def __post_init__(self):
        self.startedDateTime = dateutil.parser.isoparse(self.startedDateTime)

@dataclass
class HarPage:
    id: str
    startedDateTime: str
    title: str
    def __post_init__(self):
        self.startedDateTime = dateutil.parser.isoparse(self.startedDateTime)

@dataclass
class HarCreator:
    name: str
    version: str
    comment: str

@dataclass
class HarLog:
    version: str
    creator: HarCreator
    pages: List[HarPage]
    entries: List[HarEntry]

@dataclass
class HarPar:
    log: HarLog

def harpar_factory(data: dict) -> HarPar:
    return from_dict(data_class=HarPar, data=data)
