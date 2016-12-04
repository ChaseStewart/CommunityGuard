from sshtunnel import SSHTunnelForwarder
import MySQLdb
import socket
import struct
import ConfigParser
import io
from uuid import getnode as get_mac


ddos_block_rule_tcp = "drop tcp $HOME_NET any -> [] any (msg \"Home device attempting to send to currently DDOSed server\")"
ddos_block_rule_udp = "drop udp $HOME_NET any -> [] any (msg \"Home device attempting to send to currently DDOSed server\")"
ddos_block_rule_icmp = "drop icmp $HOME_NET any -> [] any (msg \"Home device attempting to send to currently DDOSed server\")"
ddos_block_rule_ip = "drop ip $HOME_NET any -> [] any (msg \"Home device attempting to send to currently DDOSed server\")"



# this class handles pull and push to the server
class ddos_cron_class:

	# initialize with default settings	
	def __init__(self):
		self.ddos_path=""
		self.port=3306
		self.pulluser='dbreader'
		self.password='I!AmTheFly'
		self.db='adv_netsys_final'
		self.received_ip_list=[]
		self.ip_dict = {}
		self.ddos_ip_path=""
		self.ddos_rule_path=""



	# push data to server
	def run_ddos_cron(self):
		self.get_ddos_ips()
		self.ddos_pull()



	# load ips from blacklist.txt file
	def get_ddos_ips(self):
		config = ConfigParser.RawConfigParser()
		config.read('bbb_cron_conf.cfg')
		self.ddos_ip_path = config.get("ddos","ddos-ip-path")	
		self.ddos_rule_path = config.get("ddos","ddos-rule-path")	
		with open(self.ddos_ip_path, "r") as f:
			for line in f:
				line = line.strip("\n")
				if line not in self.ip_dict.keys():
					print("line is <"+line+">")
					print("FILE: adding "+line)
					self.ip_dict[line]=(True,False)


	def ddos_pull(self):
		with SSHTunnelForwarder(
			('35.160.253.104', 22),
			#  ssh_password="password",
			ssh_private_key="/home/debian/project_private_key.pem",
			ssh_username="ec2-user",
			remote_bind_address=('127.0.0.1', 3306)) as server:

				self.ip_list = []
				con = None
				con = MySQLdb.connect(user=self.pulluser,passwd=self.password,db=self.db,host='127.0.0.1',port=server.local_bind_port)
				cur = con.cursor()
				cur.execute("""SELECT ip_addr FROM ddos_watch_list;""")

				# first get and process IPs from server
				for (ip) in cur:
					ip_num = socket.inet_ntoa(struct.pack("!I",ip[0]))
					self.received_ip_list.append(ip_num)
					print("line is <"+ip_num+">")
					if ip_num not in self.ip_dict.keys():
						self.ip_dict[ip_num]=(False,True)
						print("AWS: adding "+ip_num)
					else:
						self.ip_dict[ip_num] = (True,True);
						print("AWS: list already has "+ip_num)
				# now process received data
				for ip in self.ip_dict.keys():
					print 
					
					# remove from list
					if self.ip_dict[ip][0] == True and self.ip_dict[ip][1] == False:
						print("REMOVING OLD COMMANDS")
						remove_file = ""
						with open(self.ddos_rule_path,"w+") as f:

							# keep all lines that do not feature given IP
							for line in f.readlines():
								print("line is <"+line+"> and new ip is <"+ip+">")
								if ip not in line:
									remove_file=remove_file+line+"\n"

							# write back all lines except ones featuring ip addr 
							f.write(remove_file)

					
									
					# added to list
					elif self.ip_dict[ip][0] == False and self.ip_dict[ip][1] == True:
						print("ADDING NEW COMMANDS")
						new_command=""
						with open(self.ddos_rule_path,"a") as f:

							# write IP addr into new command and append it
							process_command = ddos_block_rule_ip.split("[")
							new_command = new_command+process_command[0]+"["+ip+process_command[1]+"\n"
							process_command = ddos_block_rule_icmp.split("[")
							new_command = new_command+process_command[0]+"["+ip+process_command[1]+"\n"
							process_command = ddos_block_rule_udp.split("[")
							new_command = new_command+process_command[0]+"["+ip+process_command[1]+"\n"
							process_command = ddos_block_rule_tcp.split("[")
							new_command = new_command+process_command[0]+"["+ip+process_command[1]+"\n"
							f.write(new_command+"\n")

		# now that whole list is processed, replace ddos_path
		with open(self.ddos_ip_path, "w") as f:
			for ip in self.received_ip_list:
				f.write(ip+"\n")

		return



# start the job when this is called
if __name__ == '__main__':
	push_object = ddos_cron_class()
	push_object.run_ddos_cron()

			

