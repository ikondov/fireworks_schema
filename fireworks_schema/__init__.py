"""fireworks_schema module"""
import sys
import os
from .json_schema import validate, register_schema
from .json_schema import ROOT_DIR, SCHEMA_DIR
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
