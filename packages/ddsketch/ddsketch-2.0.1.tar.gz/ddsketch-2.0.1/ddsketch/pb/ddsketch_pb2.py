# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ddsketch.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ddsketch.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0e\x64\x64sketch.proto\"}\n\x08\x44\x44Sketch\x12\x1e\n\x07mapping\x18\x01 \x01(\x0b\x32\r.IndexMapping\x12\x1e\n\x0epositiveValues\x18\x02 \x01(\x0b\x32\x06.Store\x12\x1e\n\x0enegativeValues\x18\x03 \x01(\x0b\x32\x06.Store\x12\x11\n\tzeroCount\x18\x04 \x01(\x01\"\xa7\x01\n\x0cIndexMapping\x12\r\n\x05gamma\x18\x01 \x01(\x01\x12\x13\n\x0bindexOffset\x18\x02 \x01(\x01\x12\x32\n\rinterpolation\x18\x03 \x01(\x0e\x32\x1b.IndexMapping.Interpolation\"?\n\rInterpolation\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06LINEAR\x10\x01\x12\r\n\tQUADRATIC\x10\x02\x12\t\n\x05\x43UBIC\x10\x03\"\xa6\x01\n\x05Store\x12(\n\tbinCounts\x18\x01 \x03(\x0b\x32\x15.Store.BinCountsEntry\x12\x1f\n\x13\x63ontiguousBinCounts\x18\x02 \x03(\x01\x42\x02\x10\x01\x12 \n\x18\x63ontiguousBinIndexOffset\x18\x03 \x01(\x11\x1a\x30\n\x0e\x42inCountsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x11\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_INDEXMAPPING_INTERPOLATION = _descriptor.EnumDescriptor(
  name='Interpolation',
  full_name='IndexMapping.Interpolation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LINEAR', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QUADRATIC', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUBIC', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=250,
  serialized_end=313,
)
_sym_db.RegisterEnumDescriptor(_INDEXMAPPING_INTERPOLATION)


_DDSKETCH = _descriptor.Descriptor(
  name='DDSketch',
  full_name='DDSketch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mapping', full_name='DDSketch.mapping', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='positiveValues', full_name='DDSketch.positiveValues', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='negativeValues', full_name='DDSketch.negativeValues', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zeroCount', full_name='DDSketch.zeroCount', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=143,
)


_INDEXMAPPING = _descriptor.Descriptor(
  name='IndexMapping',
  full_name='IndexMapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='gamma', full_name='IndexMapping.gamma', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='indexOffset', full_name='IndexMapping.indexOffset', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='interpolation', full_name='IndexMapping.interpolation', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _INDEXMAPPING_INTERPOLATION,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=146,
  serialized_end=313,
)


_STORE_BINCOUNTSENTRY = _descriptor.Descriptor(
  name='BinCountsEntry',
  full_name='Store.BinCountsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Store.BinCountsEntry.key', index=0,
      number=1, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='Store.BinCountsEntry.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=434,
  serialized_end=482,
)

_STORE = _descriptor.Descriptor(
  name='Store',
  full_name='Store',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='binCounts', full_name='Store.binCounts', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='contiguousBinCounts', full_name='Store.contiguousBinCounts', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='contiguousBinIndexOffset', full_name='Store.contiguousBinIndexOffset', index=2,
      number=3, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_STORE_BINCOUNTSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=316,
  serialized_end=482,
)

_DDSKETCH.fields_by_name['mapping'].message_type = _INDEXMAPPING
_DDSKETCH.fields_by_name['positiveValues'].message_type = _STORE
_DDSKETCH.fields_by_name['negativeValues'].message_type = _STORE
_INDEXMAPPING.fields_by_name['interpolation'].enum_type = _INDEXMAPPING_INTERPOLATION
_INDEXMAPPING_INTERPOLATION.containing_type = _INDEXMAPPING
_STORE_BINCOUNTSENTRY.containing_type = _STORE
_STORE.fields_by_name['binCounts'].message_type = _STORE_BINCOUNTSENTRY
DESCRIPTOR.message_types_by_name['DDSketch'] = _DDSKETCH
DESCRIPTOR.message_types_by_name['IndexMapping'] = _INDEXMAPPING
DESCRIPTOR.message_types_by_name['Store'] = _STORE

DDSketch = _reflection.GeneratedProtocolMessageType('DDSketch', (_message.Message,), dict(
  DESCRIPTOR = _DDSKETCH,
  __module__ = 'ddsketch_pb2'
  # @@protoc_insertion_point(class_scope:DDSketch)
  ))
_sym_db.RegisterMessage(DDSketch)

IndexMapping = _reflection.GeneratedProtocolMessageType('IndexMapping', (_message.Message,), dict(
  DESCRIPTOR = _INDEXMAPPING,
  __module__ = 'ddsketch_pb2'
  # @@protoc_insertion_point(class_scope:IndexMapping)
  ))
_sym_db.RegisterMessage(IndexMapping)

Store = _reflection.GeneratedProtocolMessageType('Store', (_message.Message,), dict(

  BinCountsEntry = _reflection.GeneratedProtocolMessageType('BinCountsEntry', (_message.Message,), dict(
    DESCRIPTOR = _STORE_BINCOUNTSENTRY,
    __module__ = 'ddsketch_pb2'
    # @@protoc_insertion_point(class_scope:Store.BinCountsEntry)
    ))
  ,
  DESCRIPTOR = _STORE,
  __module__ = 'ddsketch_pb2'
  # @@protoc_insertion_point(class_scope:Store)
  ))
_sym_db.RegisterMessage(Store)
_sym_db.RegisterMessage(Store.BinCountsEntry)


_STORE_BINCOUNTSENTRY.has_options = True
_STORE_BINCOUNTSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
_STORE.fields_by_name['contiguousBinCounts'].has_options = True
_STORE.fields_by_name['contiguousBinCounts']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
