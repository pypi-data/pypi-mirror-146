from http.client import HTTPMessage
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Union
from urllib.parse import SplitResult

from botocore.awsrequest import AWSRequest
from botocore.compat import HAS_CRT as HAS_CRT
from botocore.compat import MD5_AVAILABLE as MD5_AVAILABLE
from botocore.credentials import Credentials, ReadOnlyCredentials

CredentialsUnion = Union[Credentials, ReadOnlyCredentials]

EMPTY_SHA256_HASH: str
PAYLOAD_BUFFER: int
ISO8601: str
SIGV4_TIMESTAMP: str
SIGNED_HEADERS_BLACKLIST: List[str]
UNSIGNED_PAYLOAD: str
STREAMING_UNSIGNED_PAYLOAD_TRAILER: str

class BaseSigner:
    REQUIRES_REGION: bool = ...
    def add_auth(self, request: AWSRequest) -> Optional[AWSRequest]: ...

class SigV2Auth(BaseSigner):
    def __init__(self, credentials: CredentialsUnion) -> None:
        self.credentials: CredentialsUnion
    def calc_signature(self, request: AWSRequest, params: Mapping[str, Any]) -> Tuple[str, str]: ...
    def add_auth(self, request: AWSRequest) -> AWSRequest: ...

class SigV3Auth(BaseSigner):
    def __init__(self, credentials: CredentialsUnion) -> None:
        self.credentials: CredentialsUnion
    def add_auth(self, request: AWSRequest) -> None: ...

class SigV4Auth(BaseSigner):
    REQUIRES_REGION: bool = ...
    def __init__(self, credentials: CredentialsUnion, service_name: str, region_name: str) -> None:
        self.credentials: CredentialsUnion
    def headers_to_sign(self, request: AWSRequest) -> HTTPMessage: ...
    def canonical_query_string(self, request: AWSRequest) -> str: ...
    def canonical_headers(self, headers_to_sign: Iterable[str]) -> str: ...
    def signed_headers(self, headers_to_sign: Iterable[str]) -> str: ...
    def payload(self, request: AWSRequest) -> str: ...
    def canonical_request(self, request: AWSRequest) -> str: ...
    def scope(self, request: AWSRequest) -> str: ...
    def credential_scope(self, request: AWSRequest) -> str: ...
    def string_to_sign(self, request: AWSRequest, canonical_request: str) -> str: ...
    def signature(self, string_to_sign: str, request: AWSRequest) -> bytes: ...
    def add_auth(self, request: AWSRequest) -> None: ...

class S3SigV4Auth(SigV4Auth): ...

class SigV4QueryAuth(SigV4Auth):
    DEFAULT_EXPIRES: int = ...
    def __init__(
        self, credentials: CredentialsUnion, service_name: str, region_name: str, expires: int = ...
    ) -> None: ...

class S3SigV4QueryAuth(SigV4QueryAuth):
    def payload(self, request: AWSRequest) -> str: ...

class S3SigV4PostAuth(SigV4Auth):
    def add_auth(self, request: AWSRequest) -> None: ...

class HmacV1Auth(BaseSigner):
    QSAOfInterest: List[str] = ...
    def __init__(
        self,
        credentials: CredentialsUnion,
        service_name: Optional[str] = ...,
        region_name: Optional[str] = ...,
    ) -> None:
        self.credentials: CredentialsUnion
    def sign_string(self, string_to_sign: str) -> str: ...
    def canonical_standard_headers(self, headers: Mapping[str, Any]) -> str: ...
    def canonical_custom_headers(self, headers: Mapping[str, Any]) -> str: ...
    def unquote_v(self, nv: str) -> Union[Tuple[str, str], str]: ...
    def canonical_resource(self, split: SplitResult, auth_path: Optional[str] = ...) -> str: ...
    def canonical_string(
        self,
        method: str,
        split: SplitResult,
        headers: Mapping[str, Any],
        expires: Optional[int] = ...,
        auth_path: Optional[str] = ...,
    ) -> Any: ...
    def get_signature(
        self,
        method: str,
        split: SplitResult,
        headers: Mapping[str, Any],
        expires: Optional[int] = ...,
        auth_path: Optional[str] = ...,
    ) -> Any: ...
    def add_auth(self, request: AWSRequest) -> None: ...

class HmacV1QueryAuth(HmacV1Auth):
    DEFAULT_EXPIRES: int = ...
    def __init__(self, credentials: CredentialsUnion, expires: int = ...) -> None:
        self.credentials: CredentialsUnion

class HmacV1PostAuth(HmacV1Auth):
    def add_auth(self, request: AWSRequest) -> None: ...

AUTH_TYPE_MAPS: Dict[str, BaseSigner]
