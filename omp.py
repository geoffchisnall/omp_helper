#!/usr/bin/python
#Author: Geoffrey Chisnall 2016
#Description
#Menu system for the OMP command to do some functions.

from xml.dom import minidom
from subprocess import Popen, PIPE, STDOUT
import sys,os,time,subprocess,getpass

os.system('clear')

#Username and Password checking
print ("Login details for the OpenVAS Management Console\n")
username = []
password = []
username=raw_input("Please enter your OMP username: ")
password = getpass.getpass(prompt='Please enter your OMP password: ')
if (not username) or (not password):
	print "Incorrect username/password"
	sys.exit()
else: 
	try:
		test  = ("omp -u %s -w %s --get-omp-version" % (username,password))
		test2 = subprocess.check_output(test, shell=True, stdin=PIPE, stderr=STDOUT)
	except subprocess.CalledProcessError as e:
		print "Incorrect username/password"
		sys.exit()

os.system('clear')

ans=True
while ans:
    print("""
    OpenVAS Management Console
    Author: Geoffrey Chisnall
    Version 1.0


    MENU:
    ------------
    1.List the TARGETS
    2.List the TASKS
    3.List the CONFIGS
    4.List the Report Formats
    5.List the Portlist
    6.Create a new TARGET
    7.Create a new TASK
    8.Create a new PORTLIST
    9.Delete a TASK
    10.Delete a TARGET
    11.Delete a PORTLIST
    12.Start a TASK
    13.Stop a TASK
    14.Start all TASKS (NOTE: this can effect performance on the computer)
    15.Get latest report of TASK
    16.Get latest report of all TASKS
    17.List status of a TASK
    18.Modify TARGET's PORTLIST (NOTE: the target has to be removed from a TASK)
    0.Exit/Quit
    """)
    ans=input("What would you like to do? ")

#List the targets that are configured
    if ans==1:
      os.system("omp -u %s -w %s -T" % (username,password)) 

#List the taks that are configured
    elif ans==2:
      os.system("omp -u %s -w %s -G" % (username,password))

#List the configs that are configured
    elif ans==3:
      os.system("omp -u %s -w %s -g" % (username,password))

#List the report format that are configured
    elif ans==4:
      os.system("omp -u %s -w %s -F" % (username,password))

#List the portlists that are configured
    elif ans==5:
      os.system("echo \"<xml>\" > portlist.xml")
      os.system("omp -u %s -w %s --xml='<get_port_lists/>' >> portlist.xml" % (username,password))
      os.system("echo \"</xml>\" >> portlist.xml")
      xmldoc = minidom.parse("portlist.xml")
      xml = xmldoc.getElementsByTagName("xml")[0]
      ports = xml.getElementsByTagName("port_list")
      print "PORTID", ' '*30, "PORTAME"
      for portlist in ports:
	portname = portlist.getElementsByTagName("name")[1].firstChild.data
	portid = portlist.getAttribute("id")
	print portid, portname
      os.system("rm portlist.xml")

#Create a new target
    elif ans==6:
      newtarget=raw_input("Name of the new TARGET: ")
      iptarget=raw_input("IP of the new TARGET: ")
      os.system("echo \"<xml>\" > portlist.xml")
      os.system("omp -u %s -w %s --xml='<get_port_lists/>' >> portlist.xml" % (username,password))
      os.system("echo \"</xml>\" >> portlist.xml")
      xmldoc = minidom.parse("portlist.xml")
      xml = xmldoc.getElementsByTagName("xml")[0]
      ports = xml.getElementsByTagName("port_list")
      print "PORTID", ' '*30, "PORTAME"
      for portlist in ports:
        portname = portlist.getElementsByTagName("name")[1].firstChild.data
        portid = portlist.getAttribute("id")
        print portid, portname
      portlisttarget=raw_input("ID of the portlist for new TARGET: ")
      os.system("omp -u %s -w %s --xml='<create_target><name>%s</name><hosts>%s</hosts><port_list id=\"%s\"></port_list></create_target>'" % (username,password,newtarget,iptarget,portlisttarget))
      os.system("rm portlist.xml")

#Create a new task
    elif ans==7:
     nametask=raw_input("Name of the TASK: ")
     commenttask=raw_input("IP Address of the TASK: ")
     os.system("omp -u %s -w %s -g" % (username,password))
     configtask=raw_input("ID of config to use: ")
     os.system("omp -u %s -w %s -T" % (username,password))
     idtarget=raw_input("ID of the TARGET to use: ")
     os.system("omp -u %s -w %s --xml='<create_task><name>%s</name><comment>%s</comment><config id=\"%s\"/><target id=\"%s\"/></create_task>'" % (username,password,nametask,commenttask,configtask,idtarget))

#Create a new Portlist
    elif ans==8:
     nameportlist=raw_input("Name of the Portlist: ")
     commentportlist=raw_input("Comment of the Portlist: ")
     print ("Usage: T:1-65535 or T:22,25,8080 or T:1-100,U:1-100 - T=TCP;U=UDP")
     rangeportlist=raw_input("Ports to add: ")
     os.system("omp -u %s -w %s --xml='<create_port_list><name>%s</name><comment>%s</comment><port_range>%s</port_range></create_port_list>'" % (username,password,nameportlist,commentportlist,rangeportlist))

#Delete a task
    elif ans==9:
     os.system("omp -u %s -w %s -G" % (username,password))
     idtask=raw_input("ID of the TASK: ")
     os.system("omp -u %s -w %s -D %s" % (username,password,idtask))

#Delete a target
    elif ans==10:
     os.system("omp -u %s -w %s -T" % (username,password))
     idtarget=raw_input("ID of the TARGET: ")
     os.system("omp -u %s -w %s --xml='<delete_target target_id=\"%s\" />'" % (username,password,idtarget))

#Delete a portlist
    elif ans==11:
      os.system("echo \"<xml>\" > portlist.xml")
      os.system("omp -u %s -w %s --xml='<get_port_lists/>' >> portlist.xml" % (username,password))
      os.system("echo \"</xml>\" >> portlist.xml")
      xmldoc = minidom.parse("portlist.xml")
      xml = xmldoc.getElementsByTagName("xml")[0]
      ports = xml.getElementsByTagName("port_list")
      print "PORTID", ' '*30, "PORTAME"
      for portlist in ports:
        portname = portlist.getElementsByTagName("name")[1].firstChild.data
        portid = portlist.getAttribute("id")
        print portid, portname
      deleteportlist=raw_input("Portlist to delete: ")
      os.system("omp -u %s -w %s --xml='<delete_port_list port_list_id=\"%s\" />>'" % (username,password,deleteportlist))
     

#Start a task
    elif ans==12:
      os.system("omp -u %s -w %s -G" % (username,password))
      taskid=raw_input("ID of the TASK: ").strip()
      os.system("omp -u %s -w %s -S %s" % (username,password,taskid))

#Stop a task
    elif ans==13:
     os.system("omp -u %s -w %s -G" % (username,password))
     taskid=raw_input("ID of the TASK: ").strip()
     os.system("omp -u %s -w %s -iX '<stop_task task_id=\"%s\"/>'" % (username, password, taskid))

#Start all tasks
    elif ans==14:
        os.system("echo \"<xml>\" > tasks.xml")
        os.system("omp -u %s -w %s --xml='<get_tasks/>' >> tasks.xml" % (username,password))
        os.system("echo \"</xml>\" >> tasks.xml")

        xmldoc = minidom.parse("tasks.xml")
        xml = xmldoc.getElementsByTagName("xml")[0]
        tasks = xml.getElementsByTagName("task")

        f = open('tasks.xml', 'rb')
        f.readlines()
        f.close()
        for task in tasks:
                taskid = task.getAttribute("id")
 		os.system("omp -u %s -w %s -S %s" % (username,password,taskid))
        os.system("rm tasks.xml")

#get the lastest report on a task
    elif ans==15: 
     os.system("omp -u %s -w %s -G" % (username,password))
     taskid=raw_input("ID of TASK: ")
     taskname=("omp -u %s -w %s -iX '<get_tasks task_id=\"%s\" />' | sed -n '/<name/,/name>/p' | grep \"<name>\"  | sed -e 's/.<name>//' | sed -e 's/<.*//' | awk 'NR==2' | sed \"s/       //\"" %  (username,password,taskid))
     resultname = subprocess.check_output(taskname, shell=True)
     resultname2 = resultname.strip()
     taskreport="omp -u %s -w %s -iX '<get_tasks task_id=\"%s\" />' | sed -n '/<last_report/,/last_report>/p' | grep \"report id\"  | sed -e 's/<report id=\"//' | sed -e 's/\">.*//' | sed \"s/          //\"" % (username,password,taskid)
     result = subprocess.check_output(taskreport, shell=True)
     result2 = result.strip()
     os.system("omp -u %s -w %s --get-report %s --format c402cc3e-b531-11e1-9163-406186ea4fc5 > \"%s\".pdf" % (username,password,result2,resultname2))

#get the latest report on all tasks
    elif ans==16:
	os.system("echo \"<xml>\" > tasks.xml")
	os.system("omp -u %s -w %s --xml='<get_tasks/>' >> tasks.xml" % (username,password))
	os.system("echo \"</xml>\" >> tasks.xml")

	xmldoc = minidom.parse("tasks.xml")
	xml = xmldoc.getElementsByTagName("xml")[0]
	tasks = xml.getElementsByTagName("task")

	f = open('tasks.xml', 'rb')
	f.readlines()
	f.close()
	for task in tasks:
      	 	taskid = task.getAttribute("id")
		taskstatus=("omp -u %s -w %s -iX '<get_tasks task_id=\"%s\" />' | grep \"<status>\" | sed -e 's/.<status>//' | sed -e 's/<.*//'" %  (username,password,taskid))
		status = subprocess.check_output(taskstatus, shell=True)
		taskname=("omp -u %s -w %s -iX '<get_tasks task_id=\"%s\" />' | sed -n '/<name/,/name>/p' | grep \"<name>\"  | sed -e 's/.<name>//' | sed -e 's/<.*//' | awk 'NR==2' | sed \"s/       //\"" %  (username,password,taskid))
     		resultname = subprocess.check_output(taskname, shell=True)
	        resultname2 = resultname.strip()
		if "New" in status:
			print ("%s report has not been generated" % (resultname2))
		else:
		        taskreport="omp -u %s -w %s -iX '<get_tasks task_id=\"%s\" />' | sed -n '/<last_report/,/last_report>/p' | grep \"report id\"  | sed -e 's/<report id=\"//' | sed -e 's/\">.*//' | sed \"s/          //\"" % (username,password,taskid)
        		result = subprocess.check_output(taskreport, shell=True)
	        	result2 = result.strip()
		        os.system("omp -u %s -w %s --get-report %s --format c402cc3e-b531-11e1-9163-406186ea4fc5 > \"%s\".pdf" % (username,password,result2,resultname2))
		        print ("%s report has been generated" % (resultname2))
	os.system("rm tasks.xml")


#Get the status on a task
    elif ans==17:
     os.system("omp -u %s -w %s -G" % (username,password))
     taskid=raw_input("ID of TASK: ")
     taskstatus="omp -u %s -w %s -G | grep %s | awk '{print $2}'" % (username,password,taskid)
     result = subprocess.check_output(taskstatus, shell=True)
     result2 = result.strip()
     print "The status of task %s is %s" % (taskid,result)

#Modify TARGETS's PORTLIST
    elif ans==18:
	os.system("omp -u %s -w %s -T" % (username,password))
	modifytarget=raw_input("ID of TARGET: ")
	os.system("echo \"<xml>\" > portlist.xml")
	os.system("omp -u %s -w %s --xml='<get_port_lists/>' >> portlist.xml" % (username,password))
	os.system("echo \"</xml>\" >> portlist.xml")
	xmldoc = minidom.parse("portlist.xml")
	xml = xmldoc.getElementsByTagName("xml")[0]
	ports = xml.getElementsByTagName("port_list")
	print "PORTID", ' '*30, "PORTAME"
	for portlist in ports:
		portname = portlist.getElementsByTagName("name")[1].firstChild.data
		portid = portlist.getAttribute("id")
		print portid, portname
	modifytargetportlist=raw_input("ID of PORTLIST: ")
	os.system("omp -u %s -w %s --xml='<modify_target target_id=\"%s\"><port_list>%s</port_list></modify_target>'" % (username,password,modifytarget,modifytargetportlist))
     
     

#Exit the menu
    elif ans==0:
      print("\nGoodbye") 
      ans = None
    else:
      print("\nNot Valid Choice Try again")
      os.system('clear')
      ans = True
