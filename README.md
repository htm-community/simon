# htm-simon
"Simon" game for Raspberry Pi, reversed so user sets pattern and NuPIC replays

Assumes the following GPIO pin assignments:

```
19: Red LED
17: Green LED
27: Blue LED
22: Yellow LED
10: Reset Switch
09: Red Button
11: Green Button
05: Blue Button
06: Yellow Button
13: Speaker
```

To have the game start automatically on reboot, clone repository to path /home/pi/simon.

Then create /etc/systemd/system/simon.service
```
[Unit]
Description=Simon
After=docker.service
Requires=docker.service

[Service]
KillSignal=SIGINT
ExecStart=/usr/bin/docker run --rm --device /dev/gpiomem:/dev/gpiomem -v /sys:/sys -v /home/pi/simon:/home/pi/simon paulscode/nupic:pizero /home/pi/simon/start.sh
WorkingDirectory=/home/pi/simon
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Then:
```
sudo systemctl enable simon.service
```
Upon reboot, game will start automatically
