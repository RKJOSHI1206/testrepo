import paramiko
from paramiko import SSHClient
import sys
import os
import subprocess
import socket
import argparse

parser=argparse.ArgumentParser(
    description='''This python script will take backup of all the DB2 databases for TPH and GW. ''',
    epilog="""All is well that ends well.""")
parser.add_argument('OS_TYPE TPH_RELEASE ENVIRONMENT_TYPE', nargs='*', default=[1, 2, 3], help='OS_TYPE RELEASE_VERSION ENVIONMENT_TYPE!')
parser.add_argument('windows 2.5.10 e2e', nargs='*', default=[1, 2, 3], help='All E2E environment database backup for WINDOWS OS!')
parser.add_argument('linux 2.5.10 e2e', nargs='*', default=[1, 2, 3], help='All E2E environment database backup for Linux OS!')
args=parser.parse_args()


os_type = sys.argv[1]
release_version = sys.argv[2]
env_type = sys.argv[3]

if os_type == 'windows' :
    backup_location = 'D:\\DB2_backup\\all_bfr_' + release_version
    u_name = 'winadmin'
    u_pwd = '15Asennu51'
    print(backup_location)
if os_type == 'linux' :
    backup_location = '/db2home/db2inst1/backups/all_bfr_' + release_version
    u_name = 'db2inst1'
    u_pwd = 'db2inst1'
    print(backup_location)

# Host id for e2e and fat environment
host_ip = {
            "e2e" :{ "windows" : ['51.20.113.61','13.48.163.145','16.171.223.168'],
                     "linux" : ['13.50.140.154', '13.53.119.168','16.171.78.103' ]
                   },
            "fat" :{ "windows" : ['13.50.120.110','13.48.163.145','51.21.0.11'],
                     "linux" : ['13.50.140.154','16.171.244.49','16.171.78.103']
                   }  
           }
    
# Connect
client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.load_system_host_keys()
for x in (host_ip[env_type][os_type]) :
    print('Host Ip is :' + x + 'User Name is::' + u_name + ' ' + u_pwd)
    # Run a command (Execute DB2 commands)
    if os_type == 'windows' :
        client.connect(x, username= u_name, password=u_pwd)
        if x == '13.48.163.145' and env_type == 'e2e' :
            backup_location = 'D:\\DB2_backup\\all_E2E_bfr_' + release_version
            stdin, stdout, stderr = client.exec_command ('mkdir ' + backup_location)
            stdin, stdout, stderr = client.exec_command ('C:\\Users\\winadmin\\backupE2EDb.bat ' + backup_location)
        if x == '13.48.163.145' and env_type == 'fat' :
            backup_location = 'D:\\DB2_backup\\all_fat_bfr_' + release_version
            stdin, stdout, stderr = client.exec_command ('mkdir ' + backup_location)
            stdin, stdout, stderr = client.exec_command ('C:\\Users\\winadmin\\backupFATDb.bat ' + backup_location)
        
        stdin, stdout, stderr = client.exec_command ('mkdir ' + backup_location)
        stdin, stdout, stderr = client.exec_command ('C:\\Users\\winadmin\\backupDb.bat ' + backup_location)
        print(f'STDOUT 1: {stdout.read().decode("utf8")}')
        print(f'STDERR 1: {stderr.read().decode("utf8")}')
    if os_type == 'linux' :
        if x == '16.171.78.103' and env_type == 'e2e' :
            u_name = 'db2inst2' 
            u_pwd = 'db2inst2'
            backup_location =  '/db2home/db2inst2/backups/all_bfr_' + release_version
            print('Exception::' + u_name + ' ' + u_pwd)
        if x == '16.171.78.103' and env_type == 'fat' :
            u_name = 'db2inst3' 
            u_pwd = 'db2inst3' 
            backup_location =  '/db2home/db2inst3/backups/all_bfr_' + release_version   
            print('Exception::' + u_name + ' ' + u_pwd)    
        print('Out::' + u_name + ' ' + u_pwd)
        client.connect(x, username= u_name, password=u_pwd)
        stdin, stdout, stderr = client.exec_command ('mkdir ' + backup_location)
        stdin, stdout, stderr = client.exec_command('db2 list db directory | grep -i alias|cut -d "=" -f2')
        d_name = stdout.read().decode("utf8")
        db_name = d_name.split('\n')
        for i in range(len(db_name)) :
            #print('Database Name:' + db_name[i])
            cmd = 'db2 backup database ' + db_name[i] + ' to ' + backup_location + ' compress'
            print (cmd) 
            #stdin, stdout, stderr = client.exec_command(cmd)
            print(f'STDOUT 1: {stdout.read().decode("utf8")}')
            print(f'STDERR 1: {stderr.read().decode("utf8")}')
# Get return code from command (0 is default for success)
        print(f'Return code: {stdout.channel.recv_exit_status()}')

# Because they are file objects, they need to be closed
    stdin.close()
    stdout.close()
    stderr.close()

# Close the client itself
    client.close()