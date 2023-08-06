import copy
import abc


class Config(metaclass=abc.ABCMeta):

    type = abc.abstractproperty()
    fields = abc.abstractproperty()

    def to_dict(self):
        d = copy.deepcopy(self.__dict__)
        d["type"] = self.type
        return {k: v for k, v in d.items() if v is not None}

    @classmethod
    def make_config_from_dict(cls, conf):
        d = copy.deepcopy(conf)
        del d["type"]
        return cls(**d)

    @classmethod
    def is_valid_dict(cls, conf):
        error = None
        if conf is None:
            error = "empty config"
            return (False, error)
        if not isinstance(conf, dict):
            error = "config must be a dictionary"
            return (False, error)
        if "type" not in conf or conf["type"] != cls.type:
            error = f"field 'type' must exist and be equal to '{cls.type}''"
            return (False, error)
        for key in cls.fields:
            if key not in conf:
                error = f"field '{key}' not present"
                return (False, error)
        return (True, error)


class GlobalConfig(Config):

    fields = ["user_name", "email", "token"]
    type = "global"

    def __init__(
        self, user_name="", email="", token="", spell_admin_token="", owner=None, include_uncommitted=True, **kwargs
    ):
        self.user_name = user_name
        self.email = email
        self.token = token
        self.spell_admin_token = spell_admin_token
        self.owner = owner
        self.include_uncommitted = include_uncommitted
