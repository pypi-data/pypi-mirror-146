import os

import yaml

from .logger import logger
from ..bn2vec_exceptions import ConfigFileValidationFailed


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def convert_into(org: dict, dst):
        for k in org.keys():
            if isinstance(org[k], dict):
                dst[k] = AttrDict(org[k])
            else:
                dst[k] = org[k]


class ConfigParser:

    default_config_path = os.path.join(os.getcwd(), 'config.yaml')
    configs: AttrDict = AttrDict()

    @classmethod
    def parse(cls, config_path) -> None:
        cls.__load_accepted_format()
        if config_path is None:
            cls.config_path = cls.default_config_path
        else:
            cls.config_path = config_path

        with open(cls.config_path, "r", encoding='utf8') as stream:
            try:
                AttrDict.convert_into(yaml.safe_load(stream), cls.configs)
            except yaml.YAMLError as yaml_error:
                logger.error(yaml_error)
            else:
                cls._validate()

    @classmethod
    def _validate(cls) -> None:
        if not isinstance(cls.configs, AttrDict):
            raise ConfigFileValidationFailed(
                cls.config_path,
                "file is empty."
            )
        for section in cls.meta.keys():
            if not cls._has_section(section):
                raise ConfigFileValidationFailed(
                    cls.config_path,
                    f"section {section} isn't specified."
                )
            if section != 'Embeddings':
                for option in cls.meta[section].keys():
                    if not cls._has_option(section, option):
                        raise ConfigFileValidationFailed(
                            cls.config_path,
                            f"option {option} under section {section} isn't specified."
                        )
                    if section != 'Memory':
                        cls._is_accepted_list(section, option)
                    else:
                        cls._is_accepted_attribute(section, option)
            else:
                cls._is_accepted_list(section)

    @classmethod
    def _is_accepted_attribute(
        cls,
        section: str,
        option: str
    ) -> None:
        config_val = cls.configs[section][option]

        if 'hard_memory_loc' != option:
            if not isinstance(config_val, bool):
                raise ConfigFileValidationFailed(
                    cls.config_path,
                    f"option {option} under {section} should be a boolean."
                )
        else:
            if not isinstance(config_val, str):
                raise ConfigFileValidationFailed(
                    cls.config_path,
                    f"option {option} under {section} should be a string."
                )

    @classmethod
    def _is_accepted_list(
        cls,
        section: str,
        option: str = None
    ) -> None:
        if option is not None:
            meta_list = cls.meta[section][option]
            config_list = cls.configs[section][option]
            if 'all' == config_list:
                cls.configs[section][option] = meta_list
                return
        else:
            meta_list = cls.meta[section]
            config_list = cls.configs[section]
            if 'all' == config_list:
                cls.configs[section] = meta_list
                return

        if not isinstance(config_list, list):
            raise ConfigFileValidationFailed(
                cls.config_path,
                f"option {option} under {section} should be a list."
            )
        if set(meta_list).union(set(config_list)) != set(meta_list):
            raise ConfigFileValidationFailed(
                cls.config_path,
                f"values {set(config_list) - set(meta_list)} in option {option} under {section} are not acceptable."
            )

    @classmethod
    def _has_section(cls, section: str) -> bool:
        return section in cls.configs.keys()

    @classmethod
    def _has_option(cls, section: str, option: str) -> bool:
        return option in cls.configs[section].keys()

    @classmethod
    def __load_accepted_format(cls) -> None:
        cls.meta = {
            'Memory': {
                'memorize_dnf_graphs': False,
                'memorize_dnf_sequences': False,
                'memorize_bn_graphs': False,
                'memorize_bn_sequences': False,
                'hard_memory': False,
                'hard_memory_loc': None
            },
            'Embeddings': [
                'rsf', 'lsf', 'ptrns', 'igf'
            ],
            'Graphs': {
                'dnf_graphs': ['vcp', 'vcn', 'vgp', 'vgn', 'vgos', 'cgp', 'cgn'],
                'bn_graphs': [
                    'compdnfp', 'compdnfn', 'compgp', 'compgn', 'compgos', 'dnfgp', 'dnfgn', 'dnfgos'
                ],
            },
            'Sequences': {
                'dnf_sequences': ['degrees', 'weights', 'cc', 'cdegrees', 'vdegrees'],
                'bn_sequences': ['degrees', 'weights', 'cc', 'cdegrees', 'vdegrees']
            },
            'Stats': {
                'rsf_stats': [
                    'min', 'max', '2nd-order-stat',
                    'range', 'entropy', 'std',
                    'mode', '25%', '50%',
                    '75%', 'IQ-range', 'moment1',
                    'moment2', 'moment3'
                ],
                'lsf_stats': [
                    'min', 'max', '2nd-order-stat',
                    'range', 'entropy', 'std',
                    'mode', '25%', '50%',
                    '75%', 'IQ-range', 'moment1',
                    'moment2', 'moment3'
                ],
                'bn_stats': [
                    'min', 'max', '2nd-order-stat',
                    'range', 'entropy', 'std',
                    'mode', '25%', '50%',
                    '75%', 'IQ-range', 'moment1',
                    'moment2', 'moment3'
                ]
            }
        }


Config = ConfigParser.configs