import os
from typing import Optional

def __throw_exception(name):
    raise ConfigError(name)

def __get(name) -> Optional[str]:
    return os.environ.get(name)

def __get_nonempty(name) -> str:
    res = __get(name)
    if res is None:
        raise ValueError(f"Argument {name} is not specified")
    if not res:
        raise ValueError(f"Argument {name} is empty")
    return res

BOT_TOKEN: str = __get_nonempty("BOT_TOKEN")
TG_ID: str = __get_nonempty("TG_ID")
MAC: str = __get_nonempty("MAC")
SSH_INSTANCE: str = __get_nonempty("SSH_INSTANCE")
RPC_SERVER: Optional[str] =  __get("RPC_SERVER")
RPC_USER: Optional[str] = __get("RPC_USER")
RPC_PASSWORD: Optional[str] = __get("RPC_PASSWORD")