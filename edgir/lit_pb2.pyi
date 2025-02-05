"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import edgir.common_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

#* The core expression primitives we start with are the value
#literals that we can use
class FloatLit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VAL_FIELD_NUMBER: builtins.int
    val: builtins.float = ...
    def __init__(self,
        *,
        val : builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"val",b"val"]) -> None: ...
global___FloatLit = FloatLit

class IntLit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VAL_FIELD_NUMBER: builtins.int
    val: builtins.int = ...
    def __init__(self,
        *,
        val : builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"val",b"val"]) -> None: ...
global___IntLit = IntLit

class BoolLit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VAL_FIELD_NUMBER: builtins.int
    val: builtins.bool = ...
    def __init__(self,
        *,
        val : builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"val",b"val"]) -> None: ...
global___BoolLit = BoolLit

class TextLit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VAL_FIELD_NUMBER: builtins.int
    val: typing.Text = ...
    def __init__(self,
        *,
        val : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"val",b"val"]) -> None: ...
global___TextLit = TextLit

class RangeLit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    MINIMUM_FIELD_NUMBER: builtins.int
    MAXIMUM_FIELD_NUMBER: builtins.int
    @property
    def minimum(self) -> global___ValueLit: ...
    @property
    def maximum(self) -> global___ValueLit: ...
    def __init__(self,
        *,
        minimum : typing.Optional[global___ValueLit] = ...,
        maximum : typing.Optional[global___ValueLit] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"maximum",b"maximum",u"minimum",b"minimum"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"maximum",b"maximum",u"minimum",b"minimum"]) -> None: ...
global___RangeLit = RangeLit

class StructLit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class MembersEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        @property
        def value(self) -> global___ValueLit: ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Optional[global___ValueLit] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    MEMBERS_FIELD_NUMBER: builtins.int
    @property
    def members(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, global___ValueLit]: ...
    def __init__(self,
        *,
        members : typing.Optional[typing.Mapping[typing.Text, global___ValueLit]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"members",b"members"]) -> None: ...
global___StructLit = StructLit

class ValueLit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    FLOATING_FIELD_NUMBER: builtins.int
    INTEGER_FIELD_NUMBER: builtins.int
    BOOLEAN_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    STRUCT_FIELD_NUMBER: builtins.int
    RANGE_FIELD_NUMBER: builtins.int
    META_FIELD_NUMBER: builtins.int
    @property
    def floating(self) -> global___FloatLit: ...
    @property
    def integer(self) -> global___IntLit: ...
    @property
    def boolean(self) -> global___BoolLit: ...
    @property
    def text(self) -> global___TextLit: ...
    @property
    def struct(self) -> global___StructLit: ...
    @property
    def range(self) -> global___RangeLit: ...
    @property
    def meta(self) -> edgir.common_pb2.Metadata: ...
    def __init__(self,
        *,
        floating : typing.Optional[global___FloatLit] = ...,
        integer : typing.Optional[global___IntLit] = ...,
        boolean : typing.Optional[global___BoolLit] = ...,
        text : typing.Optional[global___TextLit] = ...,
        struct : typing.Optional[global___StructLit] = ...,
        range : typing.Optional[global___RangeLit] = ...,
        meta : typing.Optional[edgir.common_pb2.Metadata] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"boolean",b"boolean",u"floating",b"floating",u"integer",b"integer",u"meta",b"meta",u"range",b"range",u"struct",b"struct",u"text",b"text",u"type",b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"boolean",b"boolean",u"floating",b"floating",u"integer",b"integer",u"meta",b"meta",u"range",b"range",u"struct",b"struct",u"text",b"text",u"type",b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal[u"type",b"type"]) -> typing.Optional[typing_extensions.Literal["floating","integer","boolean","text","struct","range"]]: ...
global___ValueLit = ValueLit
