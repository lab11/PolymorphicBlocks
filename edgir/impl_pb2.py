# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: edgir/impl.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from edgir import common_pb2 as edgir_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x65\x64gir/impl.proto\x12\nedgir.impl\x1a\x12\x65\x64gir/common.proto\"1\n\tBlockImpl\x12$\n\x04meta\x18\x7f \x01(\x0b\x32\x16.edgir.common.Metadata\"0\n\x08PortImpl\x12$\n\x04meta\x18\x7f \x01(\x0b\x32\x16.edgir.common.Metadata\"0\n\x08LinkImpl\x12$\n\x04meta\x18\x7f \x01(\x0b\x32\x16.edgir.common.Metadata\"7\n\x0f\x45nvironmentImpl\x12$\n\x04meta\x18\x7f \x01(\x0b\x32\x16.edgir.common.Metadatab\x06proto3')



_BLOCKIMPL = DESCRIPTOR.message_types_by_name['BlockImpl']
_PORTIMPL = DESCRIPTOR.message_types_by_name['PortImpl']
_LINKIMPL = DESCRIPTOR.message_types_by_name['LinkImpl']
_ENVIRONMENTIMPL = DESCRIPTOR.message_types_by_name['EnvironmentImpl']
BlockImpl = _reflection.GeneratedProtocolMessageType('BlockImpl', (_message.Message,), {
  'DESCRIPTOR' : _BLOCKIMPL,
  '__module__' : 'edgir.impl_pb2'
  # @@protoc_insertion_point(class_scope:edgir.impl.BlockImpl)
  })
_sym_db.RegisterMessage(BlockImpl)

PortImpl = _reflection.GeneratedProtocolMessageType('PortImpl', (_message.Message,), {
  'DESCRIPTOR' : _PORTIMPL,
  '__module__' : 'edgir.impl_pb2'
  # @@protoc_insertion_point(class_scope:edgir.impl.PortImpl)
  })
_sym_db.RegisterMessage(PortImpl)

LinkImpl = _reflection.GeneratedProtocolMessageType('LinkImpl', (_message.Message,), {
  'DESCRIPTOR' : _LINKIMPL,
  '__module__' : 'edgir.impl_pb2'
  # @@protoc_insertion_point(class_scope:edgir.impl.LinkImpl)
  })
_sym_db.RegisterMessage(LinkImpl)

EnvironmentImpl = _reflection.GeneratedProtocolMessageType('EnvironmentImpl', (_message.Message,), {
  'DESCRIPTOR' : _ENVIRONMENTIMPL,
  '__module__' : 'edgir.impl_pb2'
  # @@protoc_insertion_point(class_scope:edgir.impl.EnvironmentImpl)
  })
_sym_db.RegisterMessage(EnvironmentImpl)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _BLOCKIMPL._serialized_start=52
  _BLOCKIMPL._serialized_end=101
  _PORTIMPL._serialized_start=103
  _PORTIMPL._serialized_end=151
  _LINKIMPL._serialized_start=153
  _LINKIMPL._serialized_end=201
  _ENVIRONMENTIMPL._serialized_start=203
  _ENVIRONMENTIMPL._serialized_end=258
# @@protoc_insertion_point(module_scope)
