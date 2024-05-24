```bash
dpkg -l | grep ssh

sudo apt install openssh-client
sudo apt install openssh-server

ps -e | grep ssh
#    PID TTY          TIME CMD
# 954512 ?        00:00:00 sshd
```