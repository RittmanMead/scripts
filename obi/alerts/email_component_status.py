'''

The MIT License (MIT)
Copyright (c) 2016 Rittman Mead America Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import smtplib
import re
from subprocess import PIPE, Popen
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender= "username"
recipient = "recipient"
username="username"
password="passsword"
smtp_server = "smtp.gmail.com"
smtp_port = 587
status_command = "command"
render_html=True

def main():
	component_output = run_command(status_command)
	message = build_message(sender, recipient, component_output)
	send_email(sender, recipient, message, username, password)
	print("Done")	

def send_email(sender, recipient, message, username, password):
	try:
		smtp = smtplib.SMTP(smtp_server, smtp_port)
		smtp.starttls()
		smtp.login(username, password)
		smtp.sendmail(sender, recipient, message.as_string())
		smtp.quit()
	except Exception as e:
		print("Failed to send email. Cause:\n" + str(e))
		exit()


def build_message(sender, recipient, body):
	message_from = "From: OBIEE Component Status <"+str(sender)+">\n"	
	message_to = "To: <"+str(recipient)+">\n"
	message_subject = "Subject: OBIEE Component Status\n"
	message_blank = "\n"
	message_body = str(body)

	message_mime="MIME-Version: 1.0"
	message_content_type = "Content-type: text/html"
	
	msg = MIMEMultipart('alternative')
	msg["Subject"] = message_subject
	msg["From"] = message_from
	msg["To"] = message_to
	if render_html:
		part = MIMEText(message_body, "html")
	else:
		part = MIMEText(message_body+"\nProvided by Rittman Mead\nInterested in more services like this email? Sign up for Rittman Mead's Performance Analytics", "plain")
	msg.attach(part)

	return(msg)


def run_command(command):
	try:
		output = Popen(command.split(" "), stdout=PIPE).communicate()[0]
		if render_html is True:
			output = organize_output(output)
		return(output)

	except Exception as e:
		print("Status command failed. Cause:\n" + str(e))
		exit()


def organize_output(output):
	original_output = output
	try:
		new_output = output
		begin_index = output.find("\n\nStatus")+2
        	if begin_index < 0:
               		raise Exception("New lines not found")
                
		new_output = re.sub(' +', ' ',re.sub('\n+', '\n',new_output[begin_index:].strip("\t")))
		temp_output = new_output.split("\n")
		new_output="</table></td></tr>"

		#normal table rows
		header = False
		for row in reversed(temp_output):
			if "---" in row:
				header=True
				continue
			elements = row.rstrip().split(" ")
			if not header:
				#table rows
				row_html="<tr>"
				for element in range(0, len(elements)):
					if len(elements[element]) < 1:
						continue
					if element == 0:
						row_html+="<td width='150' height='40' valign='middle' align='left' style='font-family:Arial, Helvetica, sans-serif;font-size:13px;color:#333333;font-weight:normal;line-height:15px;-webkit-text-size-adjust:none;padding-left:10px;background-color:#f9f9f9;border-bottom:1px #ffffff solid;'>"+str(elements[element])+"</td>"
					else:
						row_html+="<td width='150' height='40' valign='middle' align='left' style='font-family:Arial, Helvetica, sans-serif;font-size:13px;color:#333333;font-weight:normal;line-height:15px;-webkit-text-size-adjust:none;padding-left:10px;'>"+str(elements[element])+"</td>"
			else:
				#table header
				row_html="<tr>"
				for element in elements:
					row_html+="<td width='150' height='30' valign='middle' align='left' style='font-family:Arial, Helvetica, sans-serif;font-size:13px;color:#ffffff;font-weight:bold;line-height:15px;-webkit-text-size-adjust:none;padding-left:10px;background:#5b6470;'>"+str(element)+"</td>"			

			row_html+="</tr>"
			new_output = row_html + new_output
			if header:
				break

		new_output = "<tr><td valign='top' align='left' style='border:#5b6470 1px solid;'><table width='100%' border='0' cellspacing='0' cellpadding='0'>" + new_output
		
		#top lines
		for i in reversed(range(0,2)):
			new_output = "<tr><td valign='middle' align='left' height='40' style='background:#f9f9f9;'><table width='100%' border='0' cellspacing='0' cellpadding='0'><tr><td valign='middle' align='left' style='font-family:Arial, Helvetica, sans-serif;font-size:13px;color#333333;font-weight:normal;line-height:15px;-webkit-text-size-adjust:none;padding-left:15px;'><span style='font-weight:bold;'>" + str(temp_output[i]) + "</span></td></tr></table></td></tr>" + new_output + '<tr><td height="10" style="border-collapse:collapse;mso-table-lspace:0pt; mso-table-rspace:0pt; mso-line-height-rule:exactly;line-height:10px;"><!--[if gte mso 15]>&nbsp;<![endif]--></td></tr>'
	
		header_html='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"> <head> <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"> <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0;"> <title>Rittman Mead</title> <link type="text/css" rel="stylesheet" href="http://www.michaelpeacock.co/responsive.css"> <style type="text/css"> * {padding: 0px;margin: 0px;} html {-webkit-text-size-adjust: none;-webkit-font-smoothing: antialiased;} a {outline: 0;} img {display: block;} td {mso-line-height-rule: exactly;} .outlookFix {text-decoration: underline;} </style> </head> <body class="fullWidth" style="background-color:#ffffff;"> <table border="0" cellspacing="0" cellpadding="0" width="100%" align="center" style="table-layout:fixed;"> <tr> <td valign="top" align="center" bgcolor="#FFFFFF"> <table border="0" cellspacing="0" cellpadding="0" width="636" align="center" class="minMaxOuter"> <!-- NAV --> <tr> <td valign="top" align="left" bgcolor="#f3f5f6"> <table border="0" cellspacing="0" cellpadding="0" width="636" class="fullWidth"> <tr> <td align="left" valign="top" width="25"></td> <td valign="top" align="left"> <table width="100%" border="0" cellspacing="0" cellpadding="0"> <tr> <td height="25" style="border-collapse:collapse;mso-table-lspace:0pt; mso-table-rspace:0pt; mso-line-height-rule:exactly;line-height:25px;"><!--[if gte mso 15]>&nbsp;<![endif]--></td> </tr> <tr> <td valign="top" align="left"> <table width="194" border="0" cellspacing="0" cellpadding="0"> <tr> <td valign="top" align="left"><a href="http://www.rittmanmead.com/" target="_blank" style="font-family:Helvetica;text-decoration:none;font-size:22px;"><span style="color:#ee3124;text-decoration:none;">rittman</span><span style="color:#425968;font-weight:bold;text-decoration:none;">mead</span></a></td> </tr> </table> </td> </tr> <tr> <td height="25" style="border-collapse:collapse;mso-table-lspace:0pt; mso-table-rspace:0pt; mso-line-height-rule:exactly;line-height:25px;"><!--[if gte mso 15]>&nbsp;<![endif]--></td> </tr> </table> </td> </tr> </table> </td> </tr> <!-- END NAV --> <!--Body Content--> <tr> <td height="10" style="border-collapse:collapse;mso-table-lspace:0pt; mso-table-rspace:0pt; mso-line-height-rule:exactly;line-height:10px;"><!--[if gte mso 15]>&nbsp;<![endif]--></td> </tr>'
	
		footer_html='<tr> <td height="10" style="border-collapse:collapse;mso-table-lspace:0pt; mso-table-rspace:0pt; mso-line-height-rule:exactly;line-height:10px;"><!--[if gte mso 15]>&nbsp;<![endif]--></td> </tr> <tr> <td valign="middle" align="left" style="background:#f9f9f9;padding-top:10px;padding-bottom:10px;\"> <table width="100%" border="0" cellspacing="0" cellpadding="0"> <tr> <td valign="middle" align="left" width="25">&nbsp;</td> <td valign="middle" align="center" style="font-family:Arial, Helvetica, sans-serif;font-size:13px;color:#333333;font-weight:normal;line-height:15px;-webkit-text-size-adjust:none;"><span style="font-weight:bold;">Interested in more services like this email?</span><br/><br/>Read about Rittman Mead&apos;s Performance Analytics service <a href="http://www.rittmanmead.com/performance-analytics" target="_blank" style="color:#425958;font-weight:bold;text-decoration:underline;"><span style="color:#425958;font-weight:bold;text-decoration:underline;">here</span></a></td> </tr> </table> </td> </tr> </table> </td> </tr> </table> </body> </html>' 
		
		new_output = header_html + new_output + footer_html

		return(new_output)

	except Exception as e:
		print("HTML styling failed, returning normal output. Cause:\n" + str(e))
		render_html=False
		return(original_output)


if __name__=="__main__":
	main()
