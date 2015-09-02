import os
import re
import sys
import datetime
import urllib, urllib2
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
        total_active_7_count = '0'  #ta7c
        total_active_7_more_count = '0'   #ta7mc
        total_active_24_count = '0'       #ta24c
        total_active_24_7_count = '0'     #ta247c

        #procedure to calculate current date and time
        i = datetime.datetime.now()
        current_timestamp = i.strftime('%Y-%m-%d %H:%M:%S')
        #print (current_timestamp)

        #re-formatting string - url link to have in complete/proper format to open github repo
        url_link = "https://github.com/"+url_link + "/pulse#new-issues"


        #procedure to open url and read response from the server which contains source code of the page
        req = urllib2.Request(url_link)
        r = urllib2.urlopen(req)

        htmlstr = r.read()


        #find the pattern for total number of active issues if any
        total_active_match = re.search(r'(\d+)</span>\sActive\sIssues</p>', htmlstr)

        #if no such pattern exists then throw message
        if not total_active_match:
            # We didn't find a active issue pattern, so throw an error message.
            return render_template('display.html', tac=total_active_count, ta7mc=total_active_7_more_count, ta24c=total_active_24_count, ta247c=total_active_24_7_count)
            #sys.stderr.write('Couldn\'t find the Active issues! - pattern\n')
        else:
	        #assign total value found from pattern
	        total_active_count = total_active_match.group(1)
	        #print (total_active_count)


        #if any active issue exists then previously any other issue may be active. Or else none of issue could be active.
        if total_active_count == '0':
	        total_active_24_count = '0'
	        total_active_24_7_count = '0'
	        total_active_7_count = '0'
	        total_active_7_more_count = '0'
        else:
	        total_active_7_match = re.search(r'(\d+)</span>\sIssues(\W+)created', htmlstr)
	        if not total_active_7_match:
		        # We didn't find pattern for last 7 days active issue, so we'll throw an error message.
		        return render_template('display.html', tac=total_active_count, ta7mc=total_active_7_more_count, ta24c=total_active_24_count, ta247c=total_active_24_7_count)
		        #sys.stderr.write('Couldn\'t find the Active issues in last seven days! - pattern\n')
	        else:
		        total_active_7_count = total_active_7_match.group(1)

	        #if any active issue exists within last 7 days then we can further drill down to get posted in last 24 hrs or more than 24 hrs but less than 7 days. Or else none of issue could be active.
	        if total_active_7_count == '0':
		        total_active_24_count = '0'
		        total_active_24_7_count = '0'
	        else:
		        #total_active_24_7_match = re.findall(r'<span\sclass="state\sstate-open">Opened</span>.*?<time\sdatetime="(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z', htmlstr, re.S)
		        total_active_24_7_match = re.findall(r'<span\sclass="state\sstate-open">Opened</span>.*?<time\sdatetime="(\d\d\d\d-\d\d-\d\d)T(\d\d\:\d\d:\d\d)Z', htmlstr, re.S)
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
			        else:
				        total_active_24_7_count = int(total_active_24_7_count) + 1


			        total_active_7_more_count = int(total_active_7_count) - int(total_active_24_7_count) - int(total_active_24_count)

        return render_template('display.html', tac=total_active_count, ta7mc=total_active_7_more_count, ta24c=total_active_24_count, ta247c=total_active_24_7_count)
        #return redirect(url_for('show_index'))

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug="true")
