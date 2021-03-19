# pc-bot

Telegram bot that lets you remotely turn on/off your PC from another hosted device.

## Prerequisites

- Configure Wake-on-LAN on PC that you want to turn on/off
- Add the following line `/etc/sudoers` to let the bot turn off PC without sudo password:
    ```
    <username> ALL=(ALL) NOPASSWD:/sbin/poweroff
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
export SSH_INSTANCE=<instance name from ssh config file>
python3 -m pc-bot
```

### Features

| Command | Action    |
|:-------:| --------- |
|   /on   | Power on  |
|  /off   | Power off |



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
Environment="SSH_INSTANCE=<instance name from ssh config file>"

[Install]
WantedBy=default.target
```

```
systemctl --user daemon-reload
systemctl --user enable pc-bot.service
systemctl --user start pc-bot.service
```
