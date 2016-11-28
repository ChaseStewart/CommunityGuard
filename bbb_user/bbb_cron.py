#from sshtunnel import SSHTunnelForwarder
import MySQLdb
import socket
import struct
import ConfigParser
import io
from uuid import getnode as get_mac

# this class handles pull and push to the server
class malicious_ip_class:

	# initialize with default settings	
	def __init__(self):
		self.blacklist_path=""
		self.port=3306
		self.pushuser='dbwriter'
		self.pulluser='dbreader'
		self.password='I!AmTheFly'
		self.db='adv_netsys_final'
		self.my_mac= get_mac()
		self.ip_list=[]

	# load ips from blacklist.txt file
	def get_ips_from_file(self):
		config = ConfigParser.RawConfigParser()
		config.read('bbb_cron_conf.cfg')
		self.blacklist_path = config.get("pycron","blacklist-path")	
		with open(self.blacklist_path, "r") as f:
			for line in f:
				self.ip_list.append(line)

	# push data to server
	def run_push(self):
		self.get_ips_from_file()
		self.blacklist_push()

	# pull data from server
	def run_pull(self):
		self.blacklist_pull()

	def blacklist_pull(self):
	#    try:
	#        with SSHTunnelForwarder(
	#                 ('35.160.253.104', 22),
	#               #  ssh_password="password",
	#                 ssh_private_key="/home/osboxes/project_private_key.pem",
	#                 ssh_username="ec2-user",
	#                 remote_bind_address=('127.0.0.1', 3306)) as server:

		
		self.ip_list = []
		con = None
		con = MySQLdb.connect(user=self.pulluser,passwd=self.password,db=self.db,host='127.0.0.1',port=self.port)
		cur = con.cursor()
		cur.execute("""SELECT ip_addr FROM bad_ipv4_output WHERE flag_count > 0;""")

		for (ip) in cur:
			ip_num = socket.inet_ntoa(struct.pack("!I",ip[0]))
			print (str(ip[0])+" is the num and ascii is "+ip_num)
			self.ip_list.append(ip_num)	

		with open(self.blacklist_path, "r") as f:
			current_ip_list = f.readlines()

		for i in range(len(current_ip_list)):
			current_ip_list[i]= current_ip_list[i].replace("\n","")
		print(str(current_ip_list))

		with open(self.blacklist_path, "a+") as f:
			for ip in self.ip_list:
				if ip not in current_ip_list:
					f.write(ip+"\n")
		return


	def blacklist_push(self):
	#    try:
	#        with SSHTunnelForwarder(
	#                 ('35.160.253.104', 22),
	#               #  ssh_password="password",
	#                 ssh_private_key="/home/osboxes/project_private_key.pem",
	#                 ssh_username="ec2-user",
	#                 remote_bind_address=('127.0.0.1', 3306)) as server:

		con = None
		con = MySQLdb.connect(user=self.pushuser,passwd=self.password,db=self.db,host='127.0.0.1',port=self.port)
		cur = con.cursor()
		print("ADDING THESE IPS"+str(self.ip_list))
		for ip in self.ip_list:
			ip_num = struct.unpack("!I",socket.inet_aton(ip))[0]
			print (ip_num)
			cur.execute("""INSERT INTO bad_ipv4_input (ip_addr, mac_addr) VALUES (%s,%s);""",(ip_num,self.my_mac))
		con.commit()

if __name__ == '__main__':
	push_object = malicious_ip_class()
	push_object.run_push()
	push_object.run_pull()

			

# TODO ON AWS CRON, USE THIS ON DUPLICATE KEY UPDATE
#cur.execute("""INSERT INTO bad_ipv4_cache (ip_addr, mac_adr) VALUES (%s,%s) ON DUPLICATE KEY UPDATE flag_count = flag_count+1;""",(ip_num,self.my_mac))
