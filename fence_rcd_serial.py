#!/usr/bin/python -tt

# Copyright 2015 Infoxchange, Danielle Madeley, Sam McLeod-Jones

# Controls an RCD serial device
# Ported from stonith/rcd_serial.c

# The Following Agent Has Been Tested On:
# CentOS Linux release 7.1.1503

# Resource example:
# primitive stonith_node_1 ocf:rcd_serial_py params port="/dev/ttyS0" time=1000 hostlist=stonith_node_1 stonith-timeout=5s

import sys
import atexit
import os
import struct
import logging
from fcntl import ioctl
from termios import TIOCMBIC, TIOCMBIS, TIOCM_RTS, TIOCM_DTR
from time import sleep

sys.path.append("@FENCEAGENTSLIBDIR@")
from fencing import *

#BEGIN_VERSION_GENERATION
RELEASE_VERSION="rcd_serial (serial reset) fence agent"
REDHAT_COPYRIGHT=""
BUILD_DATE="22 Jul 2015"
#END_VERSION_GENERATION


class RCDSerial(object):
	"""Control class for serial device"""

	def __init__(self, port='/dev/ttyS0'):
		self.fd = fd = os.open(port, os.O_RDONLY | os.O_NDELAY)
		logging.debug("Opened %s on fd %i", port, fd)
		ioctl(fd, TIOCMBIC, struct.pack('I', TIOCM_RTS | TIOCM_DTR))

	def close(self):
		"""Close the serial device"""
		logging.debug("Closing serial device")
		ret = os.close(self.fd)

		return ret

	def toggle_pin(self, pin=TIOCM_DTR, time=1000):
		"""Toggle the pin high for the time specified"""

		logging.debug("Set pin high")
		ioctl(self.fd, TIOCMBIS, struct.pack('I', pin))

		sleep(float(time) / 1000.)

		logging.debug("Set pin low")
		ioctl(self.fd, TIOCMBIC, struct.pack('I', pin))

def reboot_device(conn, options):
	conn.toggle_pin(time=options["--power-wait"])
	return True

def main():
	device_opt = ["serial_port", "no_status", "no_password", "no_login", "method", "no_on", "no_off"]

	atexit.register(atexit_handler)

	all_opt["serial_port"] = {
		"getopt" : ":",
		"longopt" : "serial-port",
		"help":"--serial-port=[port]           Port of the serial device (e.g. /dev/ttyS0)",
		"required" : "1",
		"shortdesc" : "Port of the serial device",
		"default" : "/dev/ttyS0",
		"order": 1
	}

	all_opt["method"]["default"] = "cycle"
	all_opt["power_wait"]["default"] = "2"

	options = check_input(device_opt, process_input(device_opt))

	docs = {}
	docs["shortdesc"] = "rcd_serial fence agent"
	docs["longdesc"] = "fence_rcd_serial"
	docs["vendorurl"] = "http://www.scl.co.uk/rcd_serial/"
	show_docs(options, docs)

	## Operate the fencing device
	conn = RCDSerial(port=options["--serial-port"])
	result = fence_action(conn, options, None, None, reboot_cycle_fn=reboot_device)
	conn.close()

	sys.exit(result)

if __name__ == "__main__":
	main()

