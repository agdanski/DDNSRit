# DDNSRit
Dynamic DNS/Hostname Updater for RIT

Script to update the /etc/hosts file for linux - made specifically for RIT
Basically when setting up my server on RIT, came across the issue that the IP Address isnt constant.

Usage: python dhcpfix.py <INTERFACE NAME> <HOSTNAME>

On my server this was setup as a cronjob that runs every 10 minutes and on every reboot, hasnt caused any performance issues
but there is code in here to allow dynamic updating based specifically off when the dns lease file changes
