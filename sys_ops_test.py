#!/usr/bin/python
import commands, re, urllib, datetime, time, smtplib
from smtplib import SMTP

def apache_Running():
	output_Command = str(commands.getstatusoutput('service httpd status | grep active'))
	service_Running = re.search('running', output_Command)

	if service_Running:
		return True
	else:
		return False

def apache_Port_Listening():
	
	listening_Port = str(commands.getstatusoutput('netstat -ln | grep -E \':80\''))
	port = re.search('80', listening_Port)

	if port:
		return True
	else:
		return False


def url_Status_Code():
	link = "http://localhost/phpinfo.php"
	address = urllib.urlopen(link)
	response = address.getcode()
	return response

def word_Count_Check():
	words = ['Testing 123..', 'If you can read this page it means that this site is working properly']
	link = "http://localhost/"

	site = urllib.urlopen(link)
	site_Content = site.read().decode("utf-8")
	
	missing_words = False
	for word in words:
    		if word not in site_Content:
      			missing_words = True
    	
	if missing_words:
		return False
	else:
		return True

def perform_Check():
	if 	apache_Running() and\
		apache_Port_Listening() and\
		(url_Status_Code() == 200) and\
		word_Count_Check():
		return True
	else:
		return False

def send_Email():
	try:
    		sender = 'neaguali@gmail.com'
    		receivers = 'alexandru.c.neagu@gmail.com'

		if not apache_Running():
			message_part1 = "Apache service is not running"
		else:
			message_part1 = "Apache service is running"
		
		if not apache_Port_Listening():
			message_part2 = "Apache not listening to port 80"
		else:
			message_part2 = "Apache listening to port 80"

		message_part3 = "Url status is: " + str(url_Status_Code())

		if not word_Count_Check():
			message_part4 = "Webpage is not accessible"
		else:
			message_part4 = "Webpage is accessible"



    		message = """ 
			From: Admin <neaguali@gmail.com>
			To: <alexandru.c.neagu@gmail.com>
			Subject: Apache server is down
			
			Apache server is down!

			Report
				1. %s
				2. %s
				3. %s
				4. %s
			""" % (message_part1, message_part2, message_part3, message_part4)


	

    		smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
    		smtpObj.ehlo()
    		smtpObj.starttls()
    		smtpObj.ehlo()
    		smtpObj.login('neaguali@gmail.com','Urdnaxela1985')
    		smtpObj.sendmail(sender, receivers, message)
    		smtpObj.quit()
    		print "Successfully sent email"
	except smtplib.SMTPException,error:
    		print str(error)
   		print "Error: unable to send email"		


def main():


	start = datetime.time(8)
	end = datetime.time(17)
	current_time = datetime.datetime.now().time()
	
	#send_Email()
	while (current_time >= start) and (current_time <= end):
		if perform_Check():
			print("Server is up")
			time.sleep(5)
		else:
			consecutive_Downtime = 0
			for i in range(5):
				if perform_Check():
					print("Server was down but now it's up again")
					break
				else:
					consecutive_Downtime += 1
					time.sleep(5)
			if consecutive_Downtime == 5:
				print("Server is Down!!!")


if __name__ == '__main__':
	main()
