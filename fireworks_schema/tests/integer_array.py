"""test sample classes"""
from dataclasses import dataclass
from fireworks.utilities.fw_serializers import FWSerializable
from fireworks.utilities.fw_serializers import serialize_fw
from fireworks_schema import fw_schema_serialize, fw_schema_deserialize


@dataclass
class IntegerArray(FWSerializable):
    """a sample class to test schema registration and document validation"""
    _fw_name = '{{' + __loader__.name + '.' + __qualname__ + '}}'
    data: list = None

    @serialize_fw
    @fw_schema_serialize
    def to_dict(self):
        return {'data': self.data}

    @classmethod
    @fw_schema_deserialize
    def from_dict(cls, m_dict):
        return cls(data=m_dict['data'])
