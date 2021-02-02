#import pysftp
import pysftp
from datetime import datetime
import os
import scp as SCPClient
import time
import requests
import json
from paramiko.client import SSHClient
from paramiko import AutoAddPolicy
import paramiko
from soracom_interface import Soracom

class PullerRemote:

	def __init__(self):
		#Void SSH/FTP security settings
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None

		#Create Soracom Instance
		self.soracom = Soracom()
		self.soracom.initialize_soracom_link()

		#Variables
		self.last_path = None
		self.s3_path = None

	def pull_one(self, unit, imsi):

		#Open Soracom tunnel (120 seconds)
		self.soracom.tunnel(imsi, 60)

		ip = self.soracom.get_ip()
		portnumber = self.soracom.get_port()

		#Open FTP
		print("Connecting to " + str(unit) + " at " + ip + " on port " + str(portnumber))
		client = SSHClient()
		client.set_missing_host_key_policy(AutoAddPolicy())
		client.connect(hostname=ip, port=portnumber, username='admin', password='Metro123!', timeout=60)
		sftp = client.open_sftp()

		print("FTP Connected")

		#Timestamp
		now = datetime.now()

		#Create directory for new service logfile
		destination = 'logs/' + str(unit) + '/' + now.strftime('%Y') + '/' + now.strftime('%m') + '/' + now.strftime('%d') + '/' + now.strftime('%H') + "/lvm-service-log-01.txt"

		self.last_path = 'logs/' + str(unit) + '/' + now.strftime('%Y') + '/' + now.strftime('%m') + '/' + now.strftime('%d') + '/' + now.strftime('%H') + '/'

		self.s3_path = str(unit) + '/' + now.strftime('%Y') + '/' + now.strftime('%m') + '/' + now.strftime('%d') + '/' + now.strftime('%H') + '/lvm-service-log-01.txt'

		os.makedirs(self.last_path)

		#Transfer logfile
		sftp.get('mnt/data/lvm/logs/lvm-service-log-01.txt', destination)
		print("One file downloaded")

		#Close FTP connection
		sftp.close()
		print("Connection to " + str(unit) + " closed")

	def pull_all(self, unit, imsi):
		self.soracom.tunnel(imsi, 60)

		ip = self.soracom.get_ip()
		portnumber = self.soracom.get_port()

		print("Connecting to " + str(unit) + " at " + ip + " on port " + str(portnumber))
		client = SSHClient()
		client.set_missing_host_key_policy(AutoAddPolicy())
		client.connect(hostname=ip, port=portnumber, username='admin', password='Metro123!', timeout=60)
		sftp = client.open_sftp()

		print("FTP Connected")

		now = datetime.now()

		os.makedirs('logs/' + str(unit))
		direc = 'logs/' + str(unit) + '/'

		for log in range(10):
			print(str(log))
			if log == 0:
				destination = direc + 'lvm-service-log.txt'
				file = 'mnt/data/lvm/logs/lvm-service-log.txt'
			elif log == 10:
				destination = direc + 'lvm-service-log-10.txt'
				file = 'mnt/data/lvm/logs/lvm-service-log-10.txt'
			else:
				destination = direc + 'lvm-service-log-0' + str(log) + '.txt'
				file = 'mnt/data/lvm/logs/lvm-service-log-0' + str(log) + '.txt'

			print(file)
			sftp.get(file, destination)
			print(file + " file downloaded")

		sftp.close()
		print("connection to " + str(unit) + " closed")

	def get_s3_path(self):
		return self.s3_path

	def get_path(self):
		return self.last_path
