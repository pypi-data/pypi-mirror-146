# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: uac/Session.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ..uac import UACService_pb2 as uac_dot_UACService__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='uac/Session.proto',
  package='ai.verta.uac',
  syntax='proto3',
  serialized_options=b'P\001Z:github.com/VertaAI/modeldb/protos/gen/go/protos/public/uac',
  serialized_pb=b'\n\x11uac/Session.proto\x12\x0c\x61i.verta.uac\x1a\x1cgoogle/api/annotations.proto\x1a\x14uac/UACService.proto\"i\n\x07Session\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x15\n\rverta_user_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x11\n\tttl_epoch\x18\x04 \x01(\x04\x12\x1a\n\x12session_secret_key\x18\x05 \x01(\t\"X\n\x14\x43reateSessionRequest\x12\x15\n\rverta_user_id\x18\x01 \x01(\t\x12\x14\n\x0csession_name\x18\x02 \x01(\t\x12\x13\n\x0bttl_seconds\x18\x03 \x01(\x04\"{\n\x12\x46indSessionRequest\x12\x0b\n\x03ids\x18\x01 \x03(\x04\x12\x15\n\rverta_user_id\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x03(\t\x1a\x33\n\x08Response\x12\'\n\x08sessions\x18\x01 \x03(\x0b\x32\x15.ai.verta.uac.Session\"#\n\x14\x44\x65leteSessionRequest\x12\x0b\n\x03ids\x18\x01 \x03(\x04\x32\xf2\x02\n\x0eSessionService\x12p\n\rcreateSession\x12\".ai.verta.uac.CreateSessionRequest\x1a\x15.ai.verta.uac.Session\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/v1/session/createSession:\x01*\x12~\n\x0b\x66indSession\x12 .ai.verta.uac.FindSessionRequest\x1a).ai.verta.uac.FindSessionRequest.Response\"\"\x82\xd3\xe4\x93\x02\x1c\"\x17/v1/session/findSession:\x01*\x12n\n\rdeleteSession\x12\".ai.verta.uac.DeleteSessionRequest\x1a\x13.ai.verta.uac.Empty\"$\x82\xd3\xe4\x93\x02\x1e*\x19/v1/session/deleteSession:\x01*B>P\x01Z:github.com/VertaAI/modeldb/protos/gen/go/protos/public/uacb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,uac_dot_UACService__pb2.DESCRIPTOR,])




_SESSION = _descriptor.Descriptor(
  name='Session',
  full_name='ai.verta.uac.Session',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ai.verta.uac.Session.id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='verta_user_id', full_name='ai.verta.uac.Session.verta_user_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='ai.verta.uac.Session.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ttl_epoch', full_name='ai.verta.uac.Session.ttl_epoch', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_secret_key', full_name='ai.verta.uac.Session.session_secret_key', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=87,
  serialized_end=192,
)


_CREATESESSIONREQUEST = _descriptor.Descriptor(
  name='CreateSessionRequest',
  full_name='ai.verta.uac.CreateSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='verta_user_id', full_name='ai.verta.uac.CreateSessionRequest.verta_user_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_name', full_name='ai.verta.uac.CreateSessionRequest.session_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ttl_seconds', full_name='ai.verta.uac.CreateSessionRequest.ttl_seconds', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=282,
)


_FINDSESSIONREQUEST_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.FindSessionRequest.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sessions', full_name='ai.verta.uac.FindSessionRequest.Response.sessions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=356,
  serialized_end=407,
)

_FINDSESSIONREQUEST = _descriptor.Descriptor(
  name='FindSessionRequest',
  full_name='ai.verta.uac.FindSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ids', full_name='ai.verta.uac.FindSessionRequest.ids', index=0,
      number=1, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='verta_user_id', full_name='ai.verta.uac.FindSessionRequest.verta_user_id', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='ai.verta.uac.FindSessionRequest.name', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_FINDSESSIONREQUEST_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=284,
  serialized_end=407,
)


_DELETESESSIONREQUEST = _descriptor.Descriptor(
  name='DeleteSessionRequest',
  full_name='ai.verta.uac.DeleteSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ids', full_name='ai.verta.uac.DeleteSessionRequest.ids', index=0,
      number=1, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=409,
  serialized_end=444,
)

_FINDSESSIONREQUEST_RESPONSE.fields_by_name['sessions'].message_type = _SESSION
_FINDSESSIONREQUEST_RESPONSE.containing_type = _FINDSESSIONREQUEST
DESCRIPTOR.message_types_by_name['Session'] = _SESSION
DESCRIPTOR.message_types_by_name['CreateSessionRequest'] = _CREATESESSIONREQUEST
DESCRIPTOR.message_types_by_name['FindSessionRequest'] = _FINDSESSIONREQUEST
DESCRIPTOR.message_types_by_name['DeleteSessionRequest'] = _DELETESESSIONREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Session = _reflection.GeneratedProtocolMessageType('Session', (_message.Message,), {
  'DESCRIPTOR' : _SESSION,
  '__module__' : 'uac.Session_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.Session)
  })
_sym_db.RegisterMessage(Session)

CreateSessionRequest = _reflection.GeneratedProtocolMessageType('CreateSessionRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATESESSIONREQUEST,
  '__module__' : 'uac.Session_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.CreateSessionRequest)
  })
_sym_db.RegisterMessage(CreateSessionRequest)

FindSessionRequest = _reflection.GeneratedProtocolMessageType('FindSessionRequest', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _FINDSESSIONREQUEST_RESPONSE,
    '__module__' : 'uac.Session_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.FindSessionRequest.Response)
    })
  ,
  'DESCRIPTOR' : _FINDSESSIONREQUEST,
  '__module__' : 'uac.Session_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.FindSessionRequest)
  })
_sym_db.RegisterMessage(FindSessionRequest)
_sym_db.RegisterMessage(FindSessionRequest.Response)

DeleteSessionRequest = _reflection.GeneratedProtocolMessageType('DeleteSessionRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETESESSIONREQUEST,
  '__module__' : 'uac.Session_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.DeleteSessionRequest)
  })
_sym_db.RegisterMessage(DeleteSessionRequest)


DESCRIPTOR._options = None

_SESSIONSERVICE = _descriptor.ServiceDescriptor(
  name='SessionService',
  full_name='ai.verta.uac.SessionService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=447,
  serialized_end=817,
  methods=[
  _descriptor.MethodDescriptor(
    name='createSession',
    full_name='ai.verta.uac.SessionService.createSession',
    index=0,
    containing_service=None,
    input_type=_CREATESESSIONREQUEST,
    output_type=_SESSION,
    serialized_options=b'\202\323\344\223\002\036\"\031/v1/session/createSession:\001*',
  ),
  _descriptor.MethodDescriptor(
    name='findSession',
    full_name='ai.verta.uac.SessionService.findSession',
    index=1,
    containing_service=None,
    input_type=_FINDSESSIONREQUEST,
    output_type=_FINDSESSIONREQUEST_RESPONSE,
    serialized_options=b'\202\323\344\223\002\034\"\027/v1/session/findSession:\001*',
  ),
  _descriptor.MethodDescriptor(
    name='deleteSession',
    full_name='ai.verta.uac.SessionService.deleteSession',
    index=2,
    containing_service=None,
    input_type=_DELETESESSIONREQUEST,
    output_type=uac_dot_UACService__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\002\036*\031/v1/session/deleteSession:\001*',
  ),
])
_sym_db.RegisterServiceDescriptor(_SESSIONSERVICE)

DESCRIPTOR.services_by_name['SessionService'] = _SESSIONSERVICE

# @@protoc_insertion_point(module_scope)
