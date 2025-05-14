# -*- coding: utf-8 -*-

import sys
import os
import re
import subprocess

"""
Python Nagios extensions
"""

class daemon:
	"""
	Control the nagios daemon through python
	"""

	def __init__(self, nagios_bin = "/usr/bin/nagios", nagios_cfg = "/etc/nagios/nagios.cfg", nagios_init = "/etc/init.d/nagios"):

		if not os.path.isfile(nagios_bin):
			sys.stderr.write("Missing Nagios Binary (%s)\n" % nagios_bin)
			return None

		if not os.path.isfile(nagios_cfg):
			sys.stderr.write("Missing Nagios Configuration (%s)\n" % nagios_cfg)
			return None

		if not os.path.isfile(nagios_init):
			sys.stderr.write("Missing Nagios Init File (%s)\n" % nagios_init)
			return None

		self.nagios_bin = nagios_bin
		self.nagios_cfg = nagios_cfg
		self.nagios_init = nagios_init

	def verify_config(self):
		"""
		Run nagios -v config_file to verify that the conf is working
		"""
		# Use subprocess.run instead of os.system for security
		try:
			result = subprocess.run(
				[self.nagios_bin, "-v", self.nagios_cfg],
				check=False,
				capture_output=True,
				text=True
			)
			return result.returncode == 0
		except Exception as e:
			sys.stderr.write(f"Error verifying config: {e}\n")
			return False

	def restart(self):
		# Use subprocess.run instead of os.system for security
		try:
			result = subprocess.run(
				[self.nagios_init, "restart"],
				check=False,
				capture_output=True,
				text=True
			)
			return result.returncode == 0
		except Exception as e:
			sys.stderr.write(f"Error restarting Nagios: {e}\n")
			return False
	def reload(self):
		# Use subprocess.run instead of os.system for security
		try:
			result = subprocess.run(
				[self.nagios_init, "reload"],
				check=False,
				capture_output=True,
				text=True
			)
			return result.returncode == 0
		except Exception as e:
			sys.stderr.write(f"Error reloading Nagios: {e}\n")
			return False