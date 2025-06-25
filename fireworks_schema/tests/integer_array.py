"""test sample classes"""
from dataclasses import dataclass
from fireworks.utilities.fw_serializers import FWSerializable
from fireworks.utilities.fw_serializers import serialize_fw


@dataclass
class IntegerArray(FWSerializable):
    """a sample class to test schema registration and document validation"""
    _fw_name = '{{' + __loader__.name + '.' + __qualname__ + '}}'
    data: list = None

    @serialize_fw
    def to_dict(self):
        return {'data': self.data}

    @classmethod
    def from_dict(cls, m_dict):
        return cls(data=m_dict['data'])
