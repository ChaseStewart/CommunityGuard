
/* the DB is called malicious IPs */

-- start over fresh with database
DROP DATABASE IF EXISTS adv_netsys_final;
-- create db
CREATE DATABASE adv_netsys_final;
-- use db
USE adv_netsys_final;



/* Create all necessary tables*/

-- Input table that all users can post to but nobody can read from
CREATE TABLE bad_ipv4_input( ip_addr INT UNSIGNED NOT NULL, mac_addr BIGINT UNSIGNED NOT NULL, primary key (mac_addr) );

-- Output table that all users can read from but nobody can post to
CREATE TABLE bad_ipv4_output( ip_addr INT UNSIGNED NOT NULL, flag_count BIGINT UNSIGNED NOT NULL, primary key (ip_addr) );

-- Intermediate table that holds unique mac_addrs users that are allowed to post
CREATE TABLE mac_addr_registry (id INT AUTO_INCREMENT, mac_addr BIGINT UNSIGNED, primary key (id) );

-- Intermediate table that holds number of valid flags needed to blacklist a page
CREATE TABLE flag_count (valid_flag_count BIGINT UNSIGNED, num_reg_users BIGINT UNSIGNED, primary key (num_reg_users) );

-- Intermediate table that keeps all matches of valid MACADDR and IP
CREATE TABLE bad_ipv4_master_list ( ip_addr INT UNSIGNED NOT NULL, mac_addr BIGINT UNSIGNED NOT NULL, primary key (mac_addr) );



/* Create necessary users */

-- DBWriter is used to read the bad_ipv4_output table

GRANT USAGE ON adv_netsys_final.* TO 'dbwriter'@'localhost';
DROP USER 'dbwriter'@'localhost';
CREATE USER 'dbwriter'@'localhost' IDENTIFIED BY 'I!AmTheFly';
GRANT INSERT ON adv_netsys_final.bad_ipv4_input TO 'dbwriter'@'localhost';

-- DBWriter is used to write to the bad_ipv4_input table
GRANT USAGE ON adv_netsys_final.* TO 'dbreader'@'localhost';
DROP USER 'dbreader'@'localhost';
CREATE USER 'dbreader'@'localhost' IDENTIFIED BY 'I!AmTheFly';
GRANT SELECT ON adv_netsys_final.bad_ipv4_output TO 'dbreader'@'localhost';

-- DBAdmin is not accessible by users and is used to run the intermediate cron commands that turn input into output
GRANT USAGE ON adv_netsys_final.* TO 'newdbadmin'@'localhost';
DROP USER 'newdbadmin'@'localhost';
CREATE USER 'newdbadmin'@'localhost' IDENTIFIED BY 'I!AmTheFly';
GRANT ALL ON adv_netsys_final.* TO 'dbadmin'@'localhost';

