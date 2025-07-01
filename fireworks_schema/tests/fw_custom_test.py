"""Unit tests for custom JSON schema"""

__author__ = 'Ivan Kondov'
__copyright__ = 'Copyright 2025, Karlsruhe Institute of Technology'
__email__ = 'ivan.kondov@kit.edu'
__maintainer__ = 'Ivan Kondov'

import os
import unittest
import json
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError
from jsonschema import Draft7Validator
from fireworks.fw_config import JSON_SCHEMA_VALIDATE
from fireworks.utilities.fw_serializers import load_object_from_file
import fireworks_schema
from .integer_array import IntegerArray

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples', 'custom')
SCHEMA_PATH = os.path.join(SAMPLES_DIR, 'integerarray.json')
fireworks_schema.register_schema(SCHEMA_PATH)


class CustomSchemaTest(unittest.TestCase):
    """validate a custom JSON schema"""

    def test_validate_schema(self):
        """validate the schema against the metaschema"""
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as fileh:
            schema_dict = json.load(fileh)
        try:
            Draft7Validator.check_schema(schema_dict)
        except SchemaError as err:
            self.fail('Schema validation error: '+str(err))


class CustomSchemaValidatorTest(unittest.TestCase):
    """test the custom schema validator using a sample document"""

    def setUp(self):
        self.schema_name = 'IntegerArray'

    def test_validate(self):
        """validate a set of samples against the schema directly"""
        instance_path = os.path.join(SAMPLES_DIR, 'integer_array.json')
        with open(instance_path, 'r', encoding='utf-8') as fileh:
            instance = json.load(fileh)
        try:
            fireworks_schema.validate(instance, self.schema_name)
        except ValidationError as err:
            self.fail('Validation error: '+str(err))


class CustomSchemaFWserialiserTest(unittest.TestCase):
    """test validators in fw_serializers.py, requires JSON_SCHEMA_VALIDATE"""

    def setUp(self):
        if not JSON_SCHEMA_VALIDATE:
            raise unittest.SkipTest('Skipping because JSON_SCHEMA_VALIDATE=False')
        self.sample_path = os.path.join(SAMPLES_DIR, 'integer_array.json')
        self.schema_name = 'IntegerArray'

    def test_validate_load_object_from_file(self):
        """validate IntegerArray schema via load_object_from_file()"""
        try:
            load_object_from_file(self.sample_path)
        except ValidationError as err:
            self.fail('Validation error: '+str(err))

    def test_integer_array_from_file(self):
        """validate IntegerArray schema via FWSerializable.from_file()"""
        try:
            IntegerArray.from_file(self.sample_path)
        except ValidationError as err:
            self.fail('Validation error: '+err.message)


class CustomSchemaDecoratorTest(unittest.TestCase):
    """test validators via decorating the from_dict() and to_dict() methods"""

    def setUp(self):
        if not JSON_SCHEMA_VALIDATE:
            raise unittest.SkipTest('Skipping because JSON_SCHEMA_VALIDATE=False')
        instance_path = os.path.join(SAMPLES_DIR, 'integer_array.json')
        with open(instance_path, 'r', encoding='utf-8') as fileh:
            self.instance = json.load(fileh)

    def test_validate_from_dict(self):
        """validate IntegerArray schema via decorating from_dict()"""
        del self.instance['_fw_name']
        with self.assertRaises(ValidationError):
            IntegerArray.from_dict(self.instance)

    def test_validate_to_dict(self):
        """validate IntegerArray schema via decorating to_dict()"""
        obj = IntegerArray.from_dict(self.instance)
        obj.data.append('a')
        with self.assertRaises(ValidationError):
            obj.to_dict()


if __name__ == '__main__':
    unittest.main()
