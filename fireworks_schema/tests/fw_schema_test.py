""" Unit tests for FireWorks JSON schema """

__author__ = 'Ivan Kondov'
__copyright__ = 'Copyright 2020, Karlsruhe Institute of Technology'
__email__ = 'ivan.kondov@kit.edu'
__maintainer__ = 'Ivan Kondov'

import os
import unittest
import json
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError
from jsonschema import Draft7Validator
import fireworks_schema

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')


class JSONSchemaTest(unittest.TestCase):
    """ validate the FireWorks JSON schema """

    def test_validate_schema(self):
        """ validate the schema against the metaschema """
        schemas = [
            'addfilestask.json',
            'archivedirtask.json',
            'backgroundtask.json',
            'commandlinetask.json',
            'commonadapter.json',
            'compressdirtask.json',
            'deletefilestask.json',
            'dupefinder.json',
            'filedeletetask.json',
            'filetransfertask.json',
            'filewritetask.json',
            'firetask.json',
            'firework.json',
            'foreachtask.json',
            'fwaction.json',
            'fwconfig.json',
            'fworker.json',
            'generic.json',
            'getfilestask.json',
            'importdatatask.json',
            'joindicttask.json',
            'joinlisttask.json',
            'launch.json',
            'launchpad.json',
            'links.json',
            'pytask.json',
            'scripttask.json',
            'spec.json',
            'templatewritertask.json',
            'tracker.json',
            'workflow.json'
        ]
        for schema in schemas:
            schema_file = os.path.join(fireworks_schema.SCHEMA_DIR, schema)
            with open(schema_file, 'r') as fileh:
                schema_dict = json.load(fileh)
            try:
                Draft7Validator.check_schema(schema_dict)
            except SchemaError as err:
                self.fail('Schema validation error: '+err.message)


class JSONSchemaValidatorTest(unittest.TestCase):
    """ test the FireWorks schema validator using sample documents """

    def test_validate(self):
        """ validate a set of samples against the schema directly """
        schemas = ['Firetask', 'Firework', 'Workflow', 'LaunchPad', 'FWorker',
                   'CommonAdapter']
        for schema in schemas:
            path = os.path.join(SAMPLES_DIR, schema.lower())
            for wf_file in os.listdir(path):
                with open(os.path.join(path, wf_file), 'r') as fileh:
                    try:
                        fireworks_schema.validate(json.load(fileh), schema)
                    except ValidationError as err:
                        self.fail('Validation error: '+err.message)

    def test_validate_invalid(self):
        """ validate a set of invalid workflow samples against the schema """
        path = os.path.join(SAMPLES_DIR, 'workflow-invalid')
        for wf_file in os.listdir(path):
            with open(os.path.join(path, wf_file), 'r') as fileh:
                inst = json.load(fileh)
                with self.assertRaises(ValidationError):
                    fireworks_schema.validate(inst, 'Workflow')


if __name__ == '__main__':
    unittest.main()
