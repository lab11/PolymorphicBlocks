# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from edg_core.edgrpc.hdl_pb2 import (
    Refinements as hdl_pb2___Refinements,
)

from edg_core.edgir.lit_pb2 import (
    ValueLit as lit_pb2___ValueLit,
)

from edg_core.edgir.ref_pb2 import (
    LocalPath as ref_pb2___LocalPath,
)

from edg_core.edgir.schema_pb2 import (
    Design as schema_pb2___Design,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class CompilerRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    modules: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text] = ...

    @property
    def design(self) -> schema_pb2___Design: ...

    @property
    def refinements(self) -> hdl_pb2___Refinements: ...

    def __init__(self,
        *,
        modules : typing___Optional[typing___Iterable[typing___Text]] = None,
        design : typing___Optional[schema_pb2___Design] = None,
        refinements : typing___Optional[hdl_pb2___Refinements] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"design",b"design",u"refinements",b"refinements"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"design",b"design",u"modules",b"modules",u"refinements",b"refinements"]) -> None: ...
type___CompilerRequest = CompilerRequest

class CompilerResult(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class Value(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

        @property
        def path(self) -> ref_pb2___LocalPath: ...

        @property
        def value(self) -> lit_pb2___ValueLit: ...

        def __init__(self,
            *,
            path : typing___Optional[ref_pb2___LocalPath] = None,
            value : typing___Optional[lit_pb2___ValueLit] = None,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions___Literal[u"path",b"path",u"value",b"value"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"path",b"path",u"value",b"value"]) -> None: ...
    type___Value = Value

    error: typing___Text = ...

    @property
    def design(self) -> schema_pb2___Design: ...

    @property
    def solvedValues(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___CompilerResult.Value]: ...

    def __init__(self,
        *,
        design : typing___Optional[schema_pb2___Design] = None,
        error : typing___Optional[typing___Text] = None,
        solvedValues : typing___Optional[typing___Iterable[type___CompilerResult.Value]] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"design",b"design",u"error",b"error",u"result",b"result"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"design",b"design",u"error",b"error",u"result",b"result",u"solvedValues",b"solvedValues"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"result",b"result"]) -> typing_extensions___Literal["design","error"]: ...
type___CompilerResult = CompilerResult
