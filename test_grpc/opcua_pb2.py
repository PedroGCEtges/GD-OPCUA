# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: opcua.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bopcua.proto\x12\x05opcua\"*\n\x0cOpcuaMessage\x12\x0b\n\x03tag\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x0e\n\x0c\x45mptyMessage2D\n\x0cOpcuaService\x12\x34\n\x06Notify\x12\x13.opcua.OpcuaMessage\x1a\x13.opcua.EmptyMessage\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'opcua_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_OPCUAMESSAGE']._serialized_start=22
  _globals['_OPCUAMESSAGE']._serialized_end=64
  _globals['_EMPTYMESSAGE']._serialized_start=66
  _globals['_EMPTYMESSAGE']._serialized_end=80
  _globals['_OPCUASERVICE']._serialized_start=82
  _globals['_OPCUASERVICE']._serialized_end=150
# @@protoc_insertion_point(module_scope)
