# README #

# CommunityGuard #

CU Boulder ECEN 5023
Adv NetSys Final Project

Chase E Stewart, Anne Vasu, and Professor Eric Keller

### What is this repository for? ###

* This repository holds SQL, Python, Snort, BBB, and DHCP configuration code for the CommunityGuard project, as well as the final workshop paper and the LaTEX for the system.
* For more information, read the paper within the latex/ folder

### How do I get set up? ###
In order to get the whole system working, you will need to create one or more Guardian Node(s) as well as one or a few Community Outposts.

#### Guardian Node ####
* Start with an embedded system (or one day, a router) that runs Debian Linux such as the Beaglebone Black
* Follow sections 9-11 of this [tutorial](https://s3.amazonaws.com/snort-org-site/production/document_files/files/000/000/090/original/Snort_2.9.8.x_on_Ubuntu_12-14-15.pdf) from Snort.org
* From this instance install git and ansible by calling `sudo apt-get install git` and then following [this link](http://docs.ansible.com/ansible/intro_installation.html) for ansible installation
* Clone the .git repo here by calling `git clone https://bitbucket.org/ChaseEStewart/advnetsysfinal` from the device
* Run the TODO Guardian ansible deployment script to install our needed code into the guardian node (code will resemble `ansible-playbook guardian/deploy/main.yml`)
* You will need to configure the device before you are able to use it- right now this happens by editing /bbb_user/bbb_cron_conf.cfg, one day it will be a webserver that you will be able to navigate to.

#### Community Outpost ####
* Get an account with a cloud services provider (we used Amazon Web Services )
* Create an instance with a Linux OS (we support CentOS7 right now)
* Install EPEL packages- in case of CentOS7, follow [these instructions](http://www.tecmint.com/how-to-enable-epel-repository-for-rhel-centos-6-5/)
* From this instance install git and ansible by calling `sudo yum install git ansible`
* Set up your user on the server temporarily to have passwordless sudo by calling `sudo visudo`- there are many resources online if you get stuck. 
* Clone the git repository here by calling `git clone https://bitbucket.org/ChaseEStewart/advnetsysfinal` from the instance
* run the Outpost ansible deployment script by typing `cd advnetsysfinal/deploy` and then typing `ansible-playbook aws_main.yml -i hosts -e "user_name=<your username> extra_password=<your MySQL password>" `
* TODO ansible script still needs to setup cron jobs- will implement soon.
* You will need to configure the outpost before you are able to use it- right now this happens by editing  aws_server/aws_cron.cfg, one day it will also be a webserver that you will be able to navigate to.