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
PATH_REGISTRY = {f: os.path.join(SCHEMA_DIR, f) for f in os.listdir(SCHEMA_DIR)}


def get_schema(schema_name):
    """get schema dictionary and absolute path"""
    schema_file = schema_name.lower() + '.json'
    with open(PATH_REGISTRY[schema_file], 'r', encoding='utf-8') as fileh:
        schema_dict = json.load(fileh)
    return schema_dict, PATH_REGISTRY[schema_file]


jsonschema_version = semantic_version.Version(version('jsonschema'))
if jsonschema_version >= semantic_version.Version('4.18.0'):
    from referencing import Registry, Resource

    resources = []
    for file_, path in PATH_REGISTRY.items():
        with open(path, 'r', encoding='utf-8') as fp:
            resources.append((file_, Resource.from_contents(json.load(fp))))
    registry = Registry().with_resources(resources)

    def register_schema(schema_path):
        """register a schema for a custom class outside of fireworks"""
        schema_file = os.path.basename(schema_path)
        if schema_file in PATH_REGISTRY:
            raise ValueError('schema file name already in registry')
        PATH_REGISTRY[schema_file] = os.path.abspath(schema_path)
        with open(schema_path, 'r', encoding='utf-8') as fileh:
            schema_dict = json.load(fileh)
        registry.with_resource(schema_file, schema_dict)

    def validate_with_referencing(instance, schema_name):
        """JSON schema validator using the referencing package"""
        schema_dict, _ = get_schema(schema_name)
        jsonschema.validate(instance, schema_dict, registry=registry,
                            format_checker=jsonschema.FormatChecker())
    validate = validate_with_referencing
else:
    def register_schema(schema_path):
        """register a schema for a custom class outside of fireworks"""
        schema_file = os.path.basename(schema_path)
        if schema_file in PATH_REGISTRY:
            raise ValueError('schema file name already in registry')
        PATH_REGISTRY[schema_file] = os.path.abspath(schema_path)

    def validate_with_refresolver(instance, schema_name):
        """JSON schema validator using RefResolver"""
        schema_dict, schema_path = get_schema(schema_name)
        custom_res = jsonschema.RefResolver(Path(schema_path).as_uri(), schema_dict)
        jsonschema.validate(instance, schema_dict, resolver=custom_res,
                            format_checker=jsonschema.FormatChecker())
    validate = validate_with_refresolver
