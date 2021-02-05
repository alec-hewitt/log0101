import os
import time

from uploader import Uploader
from puller_remote import PullerRemote

#Edge device information

#edge_devices = [1042, 1078, 1030, 1032, 1046, 1049, 1050, 1051, 1052, 1061, 1067, 1073, 1079, 1080, 1082, 1083, 1084, 1085]
#imsi_list = ['295050911071565', '295050911071598', '295050911071554','295050911071553','295050911071568','295050911071572','295050911071573','295050911071575', '295050911071571', '295050911071589', '295050911071595', '295050911071593', '295050911071583', '295050911071588' , '295050911071587', '295050911071596', '295050911071597', '295050911066743']

edge_devices = [1078, 1050]
imsi_list = ['295050911071598','295050911071573']



#edge_devices = [1030, 1032, 1046, 1049, 1051, 1052, 1061, 1067, 1073, 1079, 1080, 1082, 1083, 1084, 1085]
#imsi_list = ['295050911071554','295050911071553','295050911071568','295050911071572','295050911071575', '295050911071571', '295050911071589', '295050911071595', '295050911071593', '295050911071583', '295050911071588' , '295050911071587', '295050911071596', '295050911071597', '295050911066743']

#edge_devices = [1079, 1080, 1082, 1083, 1084, 1085]
#imsi_list = ['295050911071583', '295050911071588' , '295050911071587', '295050911071596', '295050911071597', '295050911066743']


#edge_devices = [1049]
#imsi_list = ['295050911071572']

#Settings
#period = 21600 #pull frequency (seconds)

puller = PullerRemote()
uploader = Uploader()

#t_0 = time.time()

#count = 0

#time.sleep(21600)

#For each edge device, pull and upload
for index in range(len(edge_devices)):

	edge = edge_devices[index]
	imsi = imsi_list[index]

	check = "logs/" + str(edge)
	if os.path.isfile(check):
		print(str(edge) + " already done, skipping")
		continue

	#Pull service log to local directory
	#puller.pull_one(edge, imsi)

	print("pulling from edge " + str(edge))

	puller.pull_all(edge, imsi)

	#Get path for AWS upload
	#path = puller.get_path()
	#s3_path = puller.get_s3_path()

	#Upload to AWS
	#print("Uploading files to S3")
	#uploader.upload_logs(path, edge, s3_path)
	#print("Done")

	#Delete local files
	#print("Deleting Local Logfiles")
	#os.system('rm -r logs/*')

	print("Complete")

	#print("All files uploaded. Waiting " + str(period) + " seconds")

	#Reset timer
	#t_0 = time.time()

	#count = count + 1

	#cycle
	#while time.time() - t_0 < period:
	#time.sleep(1)
	#remaining = period - (time.time() - t_0)
	#print("%.0f" % remaining + " seconds remaining")
