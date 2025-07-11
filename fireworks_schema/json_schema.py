"""JSON schema validator for FireWorks working with relative paths"""

__author__ = 'Ivan Kondov'
__copyright__ = 'Copyright 2020-2025, Karlsruhe Institute of Technology'
__email__ = 'ivan.kondov@kit.edu'
__maintainer__ = 'Ivan Kondov'

import os
import json
from pathlib import Path
from importlib import metadata, import_module
from fireworks import fw_config
import jsonschema
import semantic_version

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(ROOT_DIR, 'schema')
JSONSCHEMA_VERSION = semantic_version.Version(metadata.version('jsonschema'))
USE_REFERENCING = JSONSCHEMA_VERSION >= semantic_version.Version('4.18.0')


class RegistryError(Exception):
    """exception to raise with using the registry"""


class _SchemaRegistry:
    """a schema registry class to be instantiated only in this module"""
    path_registry = {f: os.path.join(SCHEMA_DIR, f) for f in os.listdir(SCHEMA_DIR)}
    reg = None

    def __init__(self):
        if USE_REFERENCING:
            self.reg = self._get_registry()

    def get_schema(self, schema_name):
        """get schema dictionary and absolute path"""
        schema_file = schema_name.lower() + '.json'
        if schema_file not in self.path_registry:
            raise RegistryError(f'schema file {schema_file} not found in registry')
        with open(self.path_registry[schema_file], 'r', encoding='utf-8') as fileh:
            schema_dict = json.load(fileh)
        return schema_dict

    def _get_registry(self):
        """construct a registry object"""
        referencing = import_module('referencing')
        res_class = getattr(referencing, 'Resource')
        resources = []
        for file_, path in self.path_registry.items():
            with open(path, 'r', encoding='utf-8') as fp:
                resources.append((file_, res_class.from_contents(json.load(fp))))
        return getattr(referencing, 'Registry')().with_resources(resources)

    def get_resolver(self, schema_name):
        """get reference resolver for a given schema"""
        schema_file = schema_name.lower() + '.json'
        schema_path = self.path_registry[schema_file]
        schema_dict = self.get_schema(schema_name)
        return jsonschema.RefResolver(Path(schema_path).as_uri(), schema_dict)

    def add(self, schema_path):
        """register a schema for a custom class outside of fireworks"""
        schema_file = os.path.basename(schema_path)
        if schema_file in self.path_registry:
            raise RegistryError(f'schema file {schema_file} already in registry')
        with open(schema_path, 'r', encoding='utf-8') as fileh:
            try:
                jsonschema.Draft7Validator.check_schema(json.load(fileh))
            except (json.decoder.JSONDecodeError,
                    jsonschema.exceptions.ValidationError) as err:
                msg = f'schema in file {schema_file} not valid:\n{err}'
                raise RegistryError(msg) from err
        self.path_registry[schema_file] = os.path.abspath(schema_path)
        if USE_REFERENCING:
            self.reg = self._get_registry()


_schema_registry = _SchemaRegistry()
_format_checker = jsonschema.FormatChecker()


def register_schema(schema_path):
    """register a schema for a custom class outside of fireworks"""
    return _schema_registry.add(schema_path)


def validate(instance, schema_name, debug=False):
    """JSON schema validator using the referencing package"""
    schema_dict = _schema_registry.get_schema(schema_name)
    try:
        if USE_REFERENCING:
            jsonschema.validate(instance, schema_dict, registry=_schema_registry.reg,
                                format_checker=_format_checker)
        else:
            custom_res = _schema_registry.get_resolver(schema_name)
            jsonschema.validate(instance, schema_dict, resolver=custom_res,
                                format_checker=_format_checker)
    except jsonschema.exceptions.ValidationError as err:
        msg = f'{err}'
        if debug:
            msg = (f'{msg}\n\nValidation started with schema {schema_name}'
                   f' with instance:\n{instance}')
        raise jsonschema.exceptions.ValidationError(msg)


def fw_schema_deserialize(func=None, debug=False):
    """decorator function to activate validation in from_dict() methods"""
    def decorator(func):
        def wrapper_validator(cls, dct):
            if fw_config.JSON_SCHEMA_VALIDATE:
                validate(dct, cls.__name__, debug=debug)
            return func(cls, dct)
        return wrapper_validator
    if func:
        return decorator(func)
    return decorator


def fw_schema_serialize(func=None, debug=False):
    """decorator function to activate validation in to_dict() methods"""
    def decorator(func):
        def wrapper_validator(*args):
            dct = func(*args)
            if fw_config.JSON_SCHEMA_VALIDATE:
                validate(dct, args[0].__class__.__name__, debug=debug)
            return dct
        return wrapper_validator
    if func:
        return decorator(func)
    return decorator
