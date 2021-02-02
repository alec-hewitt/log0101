import json
import boto3
import os

from datetime import datetime

class Uploader:

	def __init__(self):
		try:
			with open('config.json', 'r') as f:
				config = json.load(f)

				self.serial_no = config['serial_no']
				self.bucket_name = config['bucket_name']

		except:
			print("\n\nWARNING: config.json with serial_no, bucket_name fields must be present\n")
			raise

		self.s3_client = boto3.client('s3')


	def upload_logs(self, path, unit, upload_path):

		if os.path.exists(path):
			#local filename
			filename = os.listdir(path)[0]

			s3_path = upload_path

			#print("uploading: ", os.path.join(path, filename))
			filetograb = path + filename

			self.s3_client.upload_file( filetograb, self.bucket_name, s3_path)

			print("File uploaded to S3")

		else:
			print("No directory specified")


