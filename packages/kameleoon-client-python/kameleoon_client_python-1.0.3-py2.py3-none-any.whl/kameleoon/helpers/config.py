import os
from typing import Optional, Dict

import yaml


def config(configuration_path) -> Dict[str, str]:
    from kameleoon.exceptions import ConfigurationNotFoundException

    """ This function reads the configuration file. """
    if not os.path.exists(configuration_path):
        raise ConfigurationNotFoundException("No config file {}".format(configuration_path))
    config_ = {}
    with open(configuration_path, 'r') as yml_file:
        config_ = yaml.load(yml_file, Loader=yaml.SafeLoader)
    return config_
