from functools import partial
import logging
import os
import warnings

import yaml
import click

from spell.cli.exceptions import ExitException
from spell.configs.config_classes import GlobalConfig


class ConfigHandler:
    def __init__(self, spell_dir, logger=None):
        self.spell_dir = os.path.expanduser(spell_dir)
        self.config_file_path = os.path.join(self.spell_dir, "config")
        self.config = None
        self.logger = logger

    def load_default_config(self, type):
        self._log(f"loading default {type} config")
        class_ = self.get_config_class(type)
        if class_ is None:
            raise ConfigException(f"Invalid type specified: {type}")
        self.config = class_()

    def load_config(self, loader=yaml.safe_load):
        try:
            self.load_config_from_file(loader=loader)
        except ConfigException:
            self.load_default_config("global")
        if "SPELL_TOKEN" in os.environ:
            self.config.token = os.environ["SPELL_TOKEN"]
            if "SPELL_OWNER" not in os.environ:
                raise ExitException("The SPELL_TOKEN environment variable is set, but SPELL_OWNER is not.")
        if "SPELL_OWNER" in os.environ:
            self.config.owner = os.environ["SPELL_OWNER"]

    def load_config_from_file(self, loader=yaml.safe_load):
        if not os.path.isfile(self.config_file_path):
            raise ConfigException(f"config file {self.config_file_path} does not exist")
        try:
            self._log(f"reading config file {self.config_file_path} from disk")
            with open(self.config_file_path, "r") as f:
                conf = loader(f)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigException(f"error reading config file {self.config_file_path}: {e}")
        if not isinstance(conf, dict) or "type" not in conf:
            raise ConfigException(f"error reading config file {self.config_file_path}: could not identify a 'type'")
        class_ = self.get_config_class(conf["type"])
        if class_ is None:
            raise ConfigException(
                f"error reading config file {self.config_file_path}: invalid value for type: '{conf['type']}'"
            )

        valid, error = class_.is_valid_dict(conf)
        if not valid:
            raise ConfigException(f"{conf['type']} config file {self.config_file_path} not valid: {error}.")

        self.config = class_.make_config_from_dict(conf)

    def remove_config_file(self):
        try:
            os.remove(self.config_file_path)
        except FileNotFoundError:
            pass

    def write(self, writer=partial(yaml.safe_dump, default_flow_style=False)):
        # create directory if necessary
        dir_ = os.path.dirname(self.config_file_path)
        if not os.path.isdir(dir_):
            self._log(f"creating directory to write {self.config.type} config file: {dir_}")
            try:
                os.makedirs(dir_)
            except OSError as e:
                raise ConfigException(
                    "Could not create directories "
                    "for {} when attempting to write {} config file: {}".format(dir_, self.config.type, e)
                )
        # write file
        try:
            with open(self.config_file_path, "w") as f:
                self._log(f"writing {self.config.type} config file to disk at {self.config_file_path}")
                writer(self.config.to_dict(), f)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigException(
                f"Could not write {self.config.type} config file to disk at {self.config_file_path}: {e}"
            )

    @staticmethod
    def get_config_class(type):
        if type == "global":
            return GlobalConfig
        return None

    def _log(self, msg, level=logging.INFO):
        if self.logger:
            self.logger.log(level, msg)


class ConfigException(Exception):
    def __init__(self, message):
        self.message = message
        super(ConfigException, self).__init__(message)


def default_config_dir():
    return os.path.join(click.get_app_dir("spell", force_posix=True))


def warn_if_spell_client_in_local():
    if (
        os.getenv("SPELL_RUN", False)
        and os.getenv("SPELL_API_URL") is not None
        and os.getenv("SPELL_API_URL").endswith(".spell:5000")
    ):
        warnings.warn(
            "You are attempting to use the Spell CLI within a local run or workspace to talk to "
            "your local API instance. This will fail because run environments in local are not "
            "connected to the Spell VPN, and therefore cannot resolve the API service URL. As a "
            "workaround, try setting the SPELL_API_URL and SPELL_TOKEN environment variables to "
            "point to dev or prod instead."
        )
