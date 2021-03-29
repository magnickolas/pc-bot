from functools import wraps
from pathlib import Path
from subprocess import CalledProcessError, check_call, DEVNULL

from loguru import logger
from paramiko import AutoAddPolicy
from paramiko.client import SSHClient
from paramiko.config import SSHConfig

from .config import TG_ID, MAC, SSH_INSTANCE, RPC_PASSWORD, RPC_SERVER, RPC_USER


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
    try:
        check_call(["wakeonlan", MAC], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
        return "Turned on!"
    except CalledProcessError:
        logger.exception("Failed to turn on")
        return "Failed to turn on..."

@authcmd
def power_off() -> str:
    try:
        if __is_windows():
            __power_off_windows()
        elif SSH_INSTANCE is not None:
            __power_off_linux()
        return "Turned off!"
    except Exception:
        logger.exception("Failed to turn off")
        return "Failed to turn off..."

def __is_windows() -> bool:
    if RPC_SERVER is None:
        return False
    try:
        check_call(["net", "rpc", "user", "info", RPC_USER, "-S", RPC_SERVER, "-U", f"{RPC_USER}%{RPC_PASSWORD}"])
        return True
    except CalledProcessError:
        return False

def __power_off_windows():
    check_call(["net", "rpc", "-S", RPC_SERVER, "-U", f"{RPC_USER}%{RPC_PASSWORD}", "shutdown", "-t", "0", "-f"])

def __power_off_linux():
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
