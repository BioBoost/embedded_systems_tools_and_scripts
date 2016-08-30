#!/usr/bin/env python
import sys
import sys, os, time, atexit
from signal import SIGTERM 
import socket
import subprocess
import time
import re
import json

class Daemon:
	"""
	A generic daemon class.
	
	Usage: subclass the Daemon class and override the run() method
	"""
	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
	
	def daemonize(self):
		"""
		do the UNIX double-fork magic, see Stevens' "Advanced 
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
		"""
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
	
		# decouple from parent environment
		os.chdir("/") 
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit from second parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1) 
	
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("%s\n" % pid)
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if pid:
			message = "pidfile %s already exist. Daemon already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)
		
		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if not pid:
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stderr.write(message % self.pidfile)
			return # not an error in a restart

		# Try killing the daemon process	
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()

	def run(self):
		"""
		You should override this method when you subclass Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""



SLEEP_TIME = 60
BROADCAST_PORT = 1337

def get_ifconfig_output():
	return subprocess.check_output("ifconfig eth0", shell=True)

def get_local_ip_address():
	ifconfig_output = get_ifconfig_output()
	inet_address_match = re.match(r'^.*?inet\saddr:(.*?)\s+.*', ifconfig_output, re.M|re.DOTALL)
	if inet_address_match:
		return inet_address_match.group(1)
	else:
		return "127.0.0.1"

def get_local_mac_address():
	ifconfig_output = get_ifconfig_output()
	mac_address_match = re.match(r'.*?HWaddr\s(.*?)\s+$', ifconfig_output, re.M|re.DOTALL)
	if mac_address_match:
		return mac_address_match.group(1)
	else:
		return "XX:XX:XX:XX:XX:XX"

def build_message(local_ip_address, local_mac_address, identifier):
	return json.dumps({ "device": "Raspberry Pi 2",
		"identifier": identifier,
		"ip address": local_ip_address,
		"mac address": local_mac_address })

def get_identifier(file):
	identifier = "maurice"
	try:
		with open(file, 'r') as f:
			identifier = f.readline().strip()
	except Exception: 
	  pass

	return identifier

def broadcast_message (port, message):
	destination = ('<broadcast>', port)
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	udp_socket.sendto(message, destination)
	udp_socket.close()

class MyDaemon(Daemon):
	def run(self):
		# For some reason this only works in combination with the systemd service (probable because working dir is set via service)
		identifierLocation = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'identifier')
		while True:
			try:
				local_ip_address = get_local_ip_address()
				local_mac_address = get_local_mac_address()
				identifier = get_identifier(identifierLocation)
				message = build_message(local_ip_address, local_mac_address, identifier)
				broadcast_message(BROADCAST_PORT, message)
			except Exception: 
			  pass
			time.sleep(SLEEP_TIME)
 
if __name__ == "__main__":
	daemon = MyDaemon('/var/run/rpi-hello.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
				daemon.start()
		elif 'stop' == sys.argv[1]:
				daemon.stop()
		elif 'restart' == sys.argv[1]:
				daemon.restart()
		else:
				print "Unknown command"
				sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)