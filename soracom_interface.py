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

class Soracom:

	def __init__(self):
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None
		self.http_response = None
		self.auth_dict = None
		self.napter_dict = None


		self.authKeyId = 'keyId-hYuSNmbpQxVNNJAYKpdhdnrCCENwcYwo'
		self.authKey = 'secret-q5kLkxJJTkRNwZ70mglXRVks4tznBNJgiLszIUMlVBJw69jaZ5N1mHrpp3ndKyTT'
		self.api_endpoint = 'https://g.api.soracom.io/v1/'
		self.tlsBool = False
		print("Soracom Link Object Created")

	def authenticate(self, authKeyId, authKey, api_endpoint):
			headerString = {'Content-Type': 'application/json', 'Accept': 'application/json'}
			bodyDict = {'authKeyId': authKeyId, 'authKey': authKey}

			self.http_response = requests.post(api_endpoint+'auth', headers = headerString, data = json.dumps(bodyDict))

	def unpack_authentication_response(self, http_response):
		json_response = json.loads(http_response.text)
		self.auth_dict = {
			'apiKey': json_response['apiKey'],
			'apiToken':json_response['token'],
			'apiOperatorId': json_response['operatorId'],
			'apiUsername': json_response['userName']
		}

	def create_napter_tunnel(self, auth_dict, imsi_target, port_target, duration, tls_bool, *args):
		headerString = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'X-Soracom-API-Key': auth_dict['apiKey'],
			'X-Soracom-Token': auth_dict['apiToken']
			}
		bodyDict = {
			'destination': {
				'imsi': imsi_target,
				'port': port_target
			},
			'duration': duration,
			'tlsRequired': tls_bool
		  }
		self.http_response = requests.post(self.api_endpoint+'port_mappings', headers = headerString, data = json.dumps(bodyDict))
		self.napter_dict = json.loads(self.http_response.text)

	def initialize_soracom_link(self):
		self.authenticate(self.authKeyId, self.authKey, self.api_endpoint)
		self.unpack_authentication_response(self.http_response)

	#Use auth_dict to create new Soracom tunnel to defined device
	#Returns tunnel connection details
	def tunnel(self, imsi, duration):
		self.create_napter_tunnel(self.auth_dict, imsi, 22, duration, self.tlsBool)

	def get_ip(self):
		#find in napter_dict
		ip = self.napter_dict['ipAddress']
		return ip

	def get_port(self):
		port = self.napter_dict['port']
		return(port)
