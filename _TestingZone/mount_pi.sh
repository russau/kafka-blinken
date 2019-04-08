#!/bin/bash
ssh pi@redpi mkdir /home/pi/experiment
sudo sshfs -o allow_other,defer_permissions,StrictHostKeyChecking=no pi@redpi:/home/pi/experiment $(pwd)/redpi
