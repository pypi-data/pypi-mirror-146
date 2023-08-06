===============================
motor_apt
===============================

Application for controlling motors from Thorlabs

By: juraj <korcek.juraj@gmail.com>
Date: April 17, 2015
Copyright Alpes Lasers SA, Neuchatel, Switzerland

Add rules: /etc/udev/rules.d/99-fix-ftdi-thorlabs.rules
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="faf0", RUN+="/bin/sh -c 'echo $kernel > /sys/bus/usb/drivers/ftdi_sio/unbind'"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="faf0", GROUP="dialout", MODE="0660"
