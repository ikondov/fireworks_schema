""" set the path to a custom FW config file """

__author__ = 'Ivan Kondov'
__copyright__ = 'Copyright 2020, Karlsruhe Institute of Technology'
__email__ = 'ivan.kondov@kit.edu'
__maintainer__ = 'Ivan Kondov'

import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["FW_CONFIG_FILE"] = os.path.join(curr_dir, 'fw_config.yaml')
