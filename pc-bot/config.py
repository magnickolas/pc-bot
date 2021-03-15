import os

class ConfigError(Exception):
    def __init__(self, name):
        super().__init__(f"Argument {name} is not specified")

def throw_exception(name):
    raise ConfigError(name)

def get_or_throw(name):
    return os.environ.get(name) or throw_exception(name)

BOT_TOKEN = get_or_throw("BOT_TOKEN")
TG_ID = get_or_throw("TG_ID")
MAC = get_or_throw("MAC")
