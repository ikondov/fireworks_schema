"""JSON schema validator for FireWorks working with relative paths"""

__author__ = 'Ivan Kondov'
__copyright__ = 'Copyright 2020-2025, Karlsruhe Institute of Technology'
__email__ = 'ivan.kondov@kit.edu'
__maintainer__ = 'Ivan Kondov'

import os
import json
from pathlib import Path
from importlib.metadata import version
import jsonschema
import semantic_version

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(ROOT_DIR, 'schema')

jsonschema_version = semantic_version.Version(version('jsonschema'))
if jsonschema_version >= semantic_version.Version('4.18.0'):
    from referencing import Registry, Resource

    def validate_with_referencing(instance, schema_name):
        """JSON schema validator working with relative paths: use referencing"""
        schema_file = schema_name.lower() + '.json'
        schema_path = os.path.join(SCHEMA_DIR, schema_file)
        with open(schema_path, 'r', encoding='utf-8') as fileh:
            schema_dict = json.load(fileh)
        files = os.listdir(SCHEMA_DIR)
        resources = []
        for file_ in files:
            with open(os.path.join(SCHEMA_DIR, file_), 'r', encoding='utf-8') as fp:
                res = (file_, Resource.from_contents(json.load(fp)))
            resources.append(res)
        registry = Registry().with_resources(resources)
        jsonschema.validate(instance, schema_dict, registry=registry,
                            format_checker=jsonschema.FormatChecker())
    validate = validate_with_referencing
else:
    def validate_with_refresolver(instance, schema_name):
        """JSON schema validator working with relative paths: use RefResolver"""
        schema_file = schema_name.lower() + '.json'
        schema_path = os.path.join(SCHEMA_DIR, schema_file)
        with open(schema_path, 'r', encoding='utf-8') as fileh:
            schema_dict = json.load(fileh)
        base_uri = Path(os.path.abspath(schema_path)).as_uri()
        custom_res = jsonschema.RefResolver(base_uri, schema_dict)
        jsonschema.validate(instance, schema_dict, resolver=custom_res,
                            format_checker=jsonschema.FormatChecker())
    validate = validate_with_refresolver
