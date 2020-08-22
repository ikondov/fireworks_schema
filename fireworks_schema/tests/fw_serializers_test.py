""" fw_serialisers tests with JSON schema validation """

__author__ = 'Ivan Kondov'
__copyright__ = 'Copyright 2020, Karlsruhe Institute of Technology'
__email__ = 'ivan.kondov@kit.edu'
__maintainer__ = 'Ivan Kondov'

import os
import unittest
from jsonschema.exceptions import ValidationError
import fw_config_path
from fireworks.fw_config import JSON_SCHEMA_VALIDATE
from fireworks.utilities.fw_serializers import load_object_from_file

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')


class JSONSchemaFWserialisersTest(unittest.TestCase):
    """ test validators in fw_serializers.py, requires JSON_SCHEMA_VALIDATE """

    # skip due to runtime errors after validation (with status Error)
    skip_list = [
        'customtask.json',
        'lambda_task.json',
        'launchpad_ssl_x509.json',
        'launchpad_ssl.json',
        'file_transfer_task_2.json',
        'file_transfer_task.json',
        'filetransfertask1.json'
    ]

    def setUp(self):
        if not JSON_SCHEMA_VALIDATE:
            raise unittest.SkipTest('Skipping because JSON_SCHEMA_VALIDATE=False')

    def test_validate_load_object_from_file(self):
        """ validate Firetask, CommonAdapter schemas via load_object_from_file() """
        schemas = ['Firetask', 'CommonAdapter']
        for schema in schemas:
            path = os.path.join(SAMPLES_DIR, schema.lower())
            for sfile in os.listdir(path):
                if sfile in self.skip_list:
                    continue
                try:
                    load_object_from_file(os.path.join(path, sfile))
                except ValidationError as err:
                    self.fail('Validation error: '+err.message)

    def _validate_from_file(self, module, classname):
        """ validate a set of samples against the schema via from_file() """
        namespace = __import__(module.split('.')[0])
        for subpackage in module.split('.')[1:]:
            namespace = getattr(namespace, subpackage)
        cls = getattr(namespace, classname)
        path = os.path.join(SAMPLES_DIR, classname.lower())
        for sfile in os.listdir(path):
            if sfile in self.skip_list:
                continue
            try:
                cls.from_file(os.path.join(path, sfile))
            except ValidationError as err:
                self.fail('Validation error: '+err.message)

    def test_workflow_from_file(self):
        """ validate Workflow schema via FWSerializable.from_file() """
        self._validate_from_file('fireworks', 'Workflow')

    def test_firework_from_file(self):
        """ validate Firework schema via FWSerializable.from_file() """
        self._validate_from_file('fireworks', 'Firework')

    def test_fworker_from_file(self):
        """ validate FWorker schema via FWSerializable.from_file() """
        self._validate_from_file('fireworks', 'FWorker')

    def test_qadapter_from_file(self):
        """ validate CommonAdapter schema via FWSerializable.from_file() """
        modulename = 'fireworks.user_objects.queue_adapters.common_adapter'
        self._validate_from_file(modulename, 'CommonAdapter')

    def test_lpad_from_file(self):
        """ validate LaunchPad schema via FWSerializable.from_file() """
        self._validate_from_file('fireworks', 'LaunchPad')


if __name__ == '__main__':
    unittest.main()
