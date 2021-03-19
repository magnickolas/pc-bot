from functools import wraps
from pathlib import Path
from subprocess import run

from loguru import logger
from paramiko import AutoAddPolicy
from paramiko.client import SSHClient
from paramiko.config import SSHConfig

from .config import TG_ID, MAC, SSH_INSTANCE


def authcmd(cmd):
    @wraps(cmd)
    def wrapper(update, context):
        user_id = update.effective_chat.id
        if str(user_id) == TG_ID:
            reply = cmd()
            context.bot.send_message(chat_id=user_id, text=reply)
    return wrapper

@authcmd
def power_on() -> str:
    run(["wakeonlan", MAC])
    return "Turned on!"

@authcmd
def power_off() -> str:
    try:
        cfg = SSHConfig.from_path(Path.home() / ".ssh" / "config")\
                       .lookup(SSH_INSTANCE)
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(**{
            "hostname":     cfg.get("hostname"),
            "port":         cfg.get("port") or 22,
            "username":     cfg.get("user"),
            "password":     cfg.get("password"),
            "key_filename": cfg.get("identityfile"),
        })
        ssh.exec_command("sudo poweroff")
        return "Turned off!"
    except Exception:
        logger.exception("Failed to power off")
        return "Failed to turn off..."
