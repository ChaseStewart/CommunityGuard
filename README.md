# README #

CU Boulder ECEN 5023
Adv NetSys Final Project

Chase E Stewart, Anne Vasu, and Professor Eric Keller

### What is this repository for? ###

* This repository holds SQL, Python, Snort, BBB, and DHCP configuration code for the Avant-Guard project, as well as the final workshop paper and the LaTEX for the system.
* For more information, read the paper within the latex/ folder

### How do I get set up? ###
In order to get the whole system working, you will need to create one or more Guardian Node(s) as well as one or a few Community Outposts.

#### Guardian Node ####
* Start with an embedded system (or one day router) that runs Debian Linux such as the Beaglebone Black
* Follow sections 9-11 of this [tutorial](https://s3.amazonaws.com/snort-org-site/production/document_files/files/000/000/090/original/Snort_2.9.8.x_on_Ubuntu_12-14-15.pdf) from Snort.org
* From this instance install git and ansible by calling `sudo apt-get install git ansible`
* Clone the .git repo here by calling `git clone https://bitbucket.org/ChaseEStewart/advnetsysfinal` from the device
* Finally, run the TODO Guardian ansible deployment script to install our needed code into the guardian node (code will resemble `ansible-playbook guardian/deploy/main.yml`)

#### Community Outpost ####
* Get an account with a cloud services provider (we used Amazon Web Services )
* Create an instance with a Linux OS (we support RHEL or CentOS)
* From this instance install git and ansible by calling `sudo yum install git ansible`
* Clone the .git repository here by calling `git clone https://bitbucket.org/ChaseEStewart/advnetsysfinal` from the instance
* run the TODO Outpost ansible deployment script (code will resemble `ansible-playbook outpost/deploy/main.yml`)