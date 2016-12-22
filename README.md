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
* First, start with an embedded system that runs Debian Linux such as the Beaglebone Black
* Second, follow sections 9-11 of this [tutorial](https://s3.amazonaws.com/snort-org-site/production/document_files/files/000/000/090/original/Snort_2.9.8.x_on_Ubuntu_12-14-15.pdf) from Snort.org
* next, run the TODO ansible deployment script to install our needed code into the guardian node

* Request our Google document with setup procedure
* TODO maybe we will set up an ansible deployment or otherwise make this more user friendly.