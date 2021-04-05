# pc-bot

Telegram bot that lets you remotely turn on/off your PC from another hosted device.

## Prerequisites

- Configure Wake-on-LAN on PC that you want to turn on/off
- Powering off *nix:
    - Add the following line `/etc/sudoers` to let the bot turn off PC without sudo password:
        ```
        <username> ALL=(ALL) NOPASSWD:/sbin/poweroff
        ```
- Powering off Windows:
    - Install samba package on the host.
    - Execute the following commands with administrator's privileges on the target:
        ```
        sc config RemoteRegistry start= auto
        sc start RemoteRegistry
        reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
        ```
- Install `wakeonlan` on the host, check out if it works with PC's mac address

## Install

```
python3 setup.py install --user
```

## Run

```
export BOT_TOKEN=<token from @BotFather>
export TG_ID=<your telegram id (to prevent someone controlling your PC)>
export MAC=<mac address of PC>
# Variables to turn off with SSH
export SSH_INSTANCE=<instance name from ssh config file> # optional
# Variables to turn off Windows with RPC
export RPC_SERVER=<target IP>                            # optional
export RPC_USER=<Windows login>                          # optional
export RPC_PASSWORD=<Windows password>                   # optional
python3 -m pc-bot
```

### Features

| Command   | Action                                                                   |
| :-------: | ------------------------------------------------------------------------ |
| /on       | Power on                                                                 |
| /off      | Power off                                                                |
| /ip       | Get target's IP address (actually host's, but assuming they're the same) |



## Example of systemd unit

**~/.config/systemd/user/pc-bot.service**
```
[Unit]
Description=PC-Bot
After=network.target network-online.target
Wants=network-online.target

[Service]
Restart=on-abort
ExecStart=python3 -m pc-bot
StartLimitInterval=60
StartLimitBurst=10
Environment="BOT_TOKEN=<token from @BotFather>"
Environment="TG_ID=<your telegram id (to prevent someone controlling your PC)>"
Environment="MAC=<mac address of PC>"
Environment="SSH_INSTANCE=<instance name from ssh config file>" # optional
Environment="RPC_SERVER=<target IP>"                            # optional
Environment="RPC_USER=<Windows login>"                          # optional
Environment="RPC_PASSWORD=<Windows password>"                   # optional

[Install]
WantedBy=default.target
```

```
systemctl --user daemon-reload
systemctl --user enable pc-bot.service
systemctl --user start pc-bot.service
```
