import ConfigParser
import os

# this class handles pull and push to the server
class malicious_ip_class:

	# initialize with default settings	
	def __init__(self):
		self.blacklist_path=""
		self.emerging_ips=""
		self.log_location=""
		self.ip_list=[]



	# push data to server
	def run_merge(self):
		self.get_config_data()
		self.merge_emerging_ip_list()
		self.merge_log_ip_list()
		self.write_out()


	# load ips from blacklist.txt file
	def get_config_data(self):
		config = ConfigParser.RawConfigParser()
		config.read('bbb_cron_conf.cfg')
		self.blacklist_path = config.get("pycron","blacklist-path")	
		self.emerging_ips   = config.get("pycron","emerging-ip-path")	
		self.log_location   = config.get("pycron","log-location")	
		self.private_key = config.get("pycron","private-key-path")	
		with open(self.blacklist_path, "r") as f:
			for line in f:
				self.ip_list.append(line)


	# now merge the emerging list with this one
	def merge_emerging_ip_list(self):
		with open(self.emerging_ips, "r") as f:
			for line in f:
				if line not in self.ip_list:
					self.ip_list.append(line)



		os.remove(self.emerging_ips)
		print(self.emerging_ips+" merged and removed")
		return


	
	# now merge the emerging list with this one
	def merge_log_ip_list(self):
		with open(self.log_location, "r") as f:
			for line in f:
				if len(line.split(",")) > 3:
					new_ip = line.split(",")[3]
					if new_ip+"\n" not in self.ip_list:
						self.ip_list.append(new_ip+"\n")


		#os.remove(self.log_location)
		#print(self.log_location+" merged and removed")
		return


	# write ip_list to file
	def write_out(self):

		with open(self.blacklist_path, "w") as f:
			for ip in self.ip_list:
				f.write(ip)


if __name__ == '__main__':
	push_object = malicious_ip_class()
	push_object.run_merge()

			

