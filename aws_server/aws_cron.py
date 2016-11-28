#from sshtunnel import SSHTunnelForwarder
import MySQLdb
import socket
import struct
import ConfigParser
import io
import sys
import hashlib

# this class handles pull and push to the server
class aws_cron_class:

	# initialize with default settings	
	def __init__(self):
		self.blacklist_path=""
		self.port=3306
		self.user='newdbadmin'
		self.password='I!AmTheFly'
		self.db='adv_netsys_final'
		self.in_list=[]
		self.valid_mac_list=[]
		
	# convert input table to output table
	def run_in_to_out(self):
		print("getting config")
		self.get_config()
		print("getting mac list")
		self.get_mac_list()
		print("mac list was "+str(self.valid_mac_list))
		print("reading input")
		self.read_input()
		print("pushing to output")
		self.check_and_output()

	# load ips from blacklist.txt file
	def get_config(self):
		config = ConfigParser.RawConfigParser()
		config.read('aws_cron.cfg')

	# get mac list
	def get_mac_list(self):
		con = None
		con = MySQLdb.connect(user=self.user,passwd=self.password,db=self.db,host='127.0.0.1',port=self.port)
		cur = con.cursor()
		cur.execute("""SELECT DISTINCT mac_addr FROM mac_addr_registry;""")
		for macaddr in cur:
			self.valid_mac_list.append(macaddr[0]);


	# read input from that table 
	def read_input(self):
		con = None
		con = MySQLdb.connect(user=self.user,passwd=self.password,db=self.db,host='127.0.0.1',port=self.port)
		cur = con.cursor()
		cur.execute("""SELECT DISTINCT ip_addr, mac_addr FROM bad_ipv4_input;""")
		
		for item in cur:
			mac = item[1]
			ip = item[0]
			if mac in self.valid_mac_list:
				print str(ip)
				self.in_list.append((ip,mac))
		print("in list is"+str(self.in_list))	
		#cur.execute(""" TRUNCATE bad_ipv4_input""");
		con.commit()
		print("in list is "+str(self.in_list))


	# check if all ips in list need to be pushed 
	def check_and_output(self):
		con = None
		con = MySQLdb.connect(user=self.user,passwd=self.password,db=self.db,host='127.0.0.1',port=self.port)
		cur = con.cursor()

		cur.execute("""SELECT DISTINCT ip_addr, mac_addr from bad_ipv4_input;""")

		for item in self.in_list:
			mac_ip_hash = hashlib.md5()
			mac_ip_hash.update(str(item[0]))
			mac_ip_hash.update(str(item[1]))
			hash_val = mac_ip_hash.digest()

			cur.execute(""" SELECT COUNT(1) FROM bad_ipv4_master_list where hash =%s """, hash_val)
			if (cur.fetchone()[0]):
				print("Already have this!")
				continue

			cur.execute("""INSERT INTO bad_ipv4_master_list (hash) VALUES (%s);""",(hash_val))
			cur.execute("""INSERT INTO bad_ipv4_output (ip_addr, flag_count) VALUES (%s,%s) ON DUPLICATE KEY UPDATE flag_count = flag_count+1;""",(item[0],1))
		con.commit()


if __name__ == '__main__':
	push_object = aws_cron_class()
	push_object.run_in_to_out()

