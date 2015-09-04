import os
import re
import sys
import datetime
import urllib, urllib2, httplib
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def show_index():
	return render_template('index.html')


@app.route('/getUrlDetail/', methods=['GET', 'POST'])
def getUrl():
	if request.method == 'POST':
		url_link=request.form['url_link']

		#initialising and assigning default values
		total_active_count = '0'   #tac
		total_active_7_more_count = '0'   #ta7mc
		total_active_24_count = '0'       #ta24c
		total_active_24_7_count = '0'     #ta247c

		#procedure to calculate current date and time
		i = datetime.datetime.now()
		current_timestamp = i.strftime('%Y-%m-%d %H:%M:%S')
		#print (current_timestamp)

		#re-formatting string - url link to have in complete/proper format to open github repo
		url_link1 = "https://github.com/"+url_link + "/issues"


		#procedure to open url and read response from the server which contains source code of the page
		req = urllib2.Request(url_link1)
		try:
			r = urllib2.urlopen(req)
		except urllib2.URLError as e:
			message = 'URLError = ' + str(e.reason)
			return render_template('message.html', message= message)
		except urllib2.HTTPError, e:
			message = 'HTTPError = ' + str(e.code)
			return render_template('message.html', message= message)
		except httplib.HTTPException, e:
			message = 'HTTPException'
			return render_template('message.html', message= message)

		htmlstr = r.read()


		#find the pattern for total number of active issues if any
		total_active_match = re.search(r'<span class="octicon octicon-issue-opened"></span>(\W+)(\d+)\sOpen', htmlstr)

		#if no such pattern exists then throw message
		if not total_active_match:
			# We didn't find a active issue pattern, so throw an error message.
			return render_template('display.html', tac=total_active_count, ta7mc=total_active_7_more_count, ta24c=total_active_24_count, ta247c=total_active_24_7_count)
			#sys.stderr.write('Couldn\'t find Open issues! - pattern\nNo Issues')
		else:
			#assign total value found from pattern
			total_active_count = total_active_match.group(2)
			#print (total_active_count)


		#if any active issue exists then previously any other issue may be active. Or else none of issue could be active.
		if total_active_count == '0':
			total_active_24_count = '0'
			total_active_24_7_count = '0'
			total_active_7_more_count = '0'
		else:
			pagination_active_page_match = re.search(r'<div class="pagination">', htmlstr)
			if not pagination_active_page_match:
				# We didn't find a active issue pattern, so throw an error message.
				sys.stderr.write('Couldn\'t find Pagination pattern\n Only 1 page')
				first_active_page_count = '1'
				last_active_page_count = '1'
				#print ("Only 1 page found!!")
			else:
				first_active_page_count = '1'
				#print (first_active_page_count)
				last_active_page_match = re.search(r'<div class="pagination">.*>(\d+)</a> <a class="next_page" rel="next"', htmlstr, re.S)
				if not last_active_page_match:
					# We didn't find a active issue pattern, so throw an error message.
					sys.stderr.write('Couldn\'t find the last page! - pattern\n')
				else:
					#assign total value found from pattern
					last_active_page_count = last_active_page_match.group(1)
					#print (last_active_page_count)
					#print ("matched")

			url_formator = []

			for page_number in range(int(first_active_page_count), int(last_active_page_count)+1 ):
				url_formator.append("https://github.com/"+url_link+"/issues?page="+str(page_number)+"&amp;q=is%3Aissue+is%3Aopen")


			for link in url_formator:
				print (link)

				request_link = urllib2.Request(link)
				response_link = urllib2.urlopen(request_link)
				link_htmlstr = response_link.read()

				#total_active_24_7_match = re.findall(r'<span\sclass="state\sstate-open">Opened</span>.*?<time\sdatetime="(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z', htmlstr, re.S)
				total_active_24_7_match = re.findall(r'<span class="octicon octicon-issue-opened open"></span>.*?<time\sdatetime="(\d\d\d\d-\d\d-\d\d)T(\d\d\:\d\d:\d\d)Z', link_htmlstr, re.S)
				if not total_active_24_7_match:
					# We didn't find a pattern for it, so we'll throw an error message.
					return render_template('display.html', tac=total_active_count, ta7mc=total_active_7_more_count, ta24c=total_active_24_count, ta247c=total_active_24_7_count)
					#sys.stderr.write('Couldn\'t find the pattern for timestamp for active issues within last 7 days! - pattern\n')

				for timestamp_tuple in total_active_24_7_match:
					#(year, month, day, hr, min, sec) = timestamp_tuple

					#from the pattern, we will get two keys for tuple and will assign values to them
					(date, time) = timestamp_tuple

					#re-formatting the string to have a string in timely manner pattern
					entry_timestamp = date + " " + time
					#print (entry_timestamp)

					#converting the string to date time object in the defined format
					start_dt = datetime.datetime.strptime(entry_timestamp, '%Y-%m-%d %H:%M:%S')
					end_dt = datetime.datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S')

					#calculate difference between the active issue posted time and the current time
					diff_time = (end_dt - start_dt)
					#print (diff_time)


					if diff_time.days <= 0:
						total_active_24_count = int(total_active_24_count) + 1
					elif diff_time.days >=1 and diff_time.days <7:
						total_active_24_7_count = int(total_active_24_7_count) + 1
					else:
						total_active_7_more_count = int(total_active_7_more_count) + 1


				response_link.close()

		return render_template('display.html', tac=total_active_count, ta7mc=total_active_7_more_count, ta24c=total_active_24_count, ta247c=total_active_24_7_count)
		#return redirect(url_for('show_index')
	else:
		return render_template('index.html')


if __name__ == '__main__':
	app.run(debug="true")
