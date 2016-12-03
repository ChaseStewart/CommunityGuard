#!/bin/sh



cd /home/debian



echo "removing old emerging.rules.zip"
echo
rm -rf emerging.rules.zip



echo "getting new emerging.rules.zip" 
echo
wget -q http://rules.emergingthreatspro.com/open/snort-2.9.0/emerging.rules.zip
unzip -q /home/debian/emerging.rules.zip



echo "Copying configuration files to ~/deploy"
echo
mkdir /home/debian/deploy
cd /



cp /etc/snort/snort.conf                     /home/debian/deploy
cp /etc/snort/rules/emerging.conf            /home/debian/deploy
cp /etc/snort/rules/local.rules              /home/debian/deploy
cp /etc/snort/rules/ddos_ips.txt             /home/debian/deploy
cp /etc/snort/rules/iplists/black_list.rules /home/debian/deploy
cp /etc/snort/rules/iplists/white_list.rules /home/debian/deploy
cp /etc/snort/rules/avant_guard_ddos.rules   /home/debian/deploy



echo "~/deploy has the following:"
ls /home/debian/deploy 
echo


echo "clobbering snort rules folder"
echo
rm -rf /etc/snort/rules
mv /home/debian/rules /etc/snort/rules



echo "replacing configuration rules"
echo
cp /home/debian/deploy/snort.conf             /etc/snort/snort.conf            
cp /home/debian/deploy/emerging.conf          /etc/snort/rules/emerging.conf   
cp /home/debian/deploy/local.rules            /etc/snort/rules/local.rules     
cp /home/debian/deploy/avant_guard_ddos.rules /etc/snort/rules/avant_guard_ddos.rules
cp /home/debian/deploy/ddos_ips.txt           /etc/snort/rules/ddos_ips.txt



echo "Now making blacklist files!"
echo
cd /etc/snort/rules
mkdir iplists    
cp /home/debian/deploy/black_list.rules       /etc/snort/rules/iplists/black_list.rules 
cp /home/debian/deploy/white_list.rules       /etc/snort/rules/iplists/white_list.rules 



echo "removing deploy folder"
echo
rm -rf /home/debian/deploy



echo "running BBB Cron python script"
echo 
cd /home/debian/advnetsysfinal/bbb_user
/usr/bin/python bbb_cron.py
/usr/bin/python merge_ips.py


