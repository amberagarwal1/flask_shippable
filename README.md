# flask_shippable
This project is built on Flask - Python microframework.
This is an outcome of the assignment as stated below:

Problem Description 

Create a repository on GitHub and write a program in any programming language (PYTHON here) that will do the following: 

Input : User can input a link to any public GitHub repository

Output :

Your UI should display a table with the following information -

- Total number of open issues

- Number of open issues that were opened in the last 24 hours

- Number of open issues that were opened more than 24 hours ago but less than 7 days ago

- Number of open issues that were opened more than 7 days ago 


So, flask_shippable.py is the main python file which carries out the processing of the mentioned list.

index.html is the homepage which asks the user to input Github repository name. It is placed at templates/index.html
index.html layout is defined in HTML and designing is defined in style sheet placed at static/style.css.
Homepage have some headings and a textbox with a submit button. It's a form and the input field can't be left blank. Javascript function is created to check it. And if user tries to submit without entring any value, then it will pop a window or alert for the same. Also, placeholder is placed to suggest user the format in which repository need to entered.

As soon as the submit is pressed, function getUrl in python file (flask_shipppable.py) is called up. It is the function that carries out all the processing. so, we got the values posted by user through the form. 

variables - we initialised 5  variables that hold the count of issues as asked:
total_active_count = '0'    #count of all open issues
total_active_7_more_count = '0'   #count of all open issues which are old than 7 days
total_active_24_count = '0'       #count of all open issues which at max 24 hrs old
total_active_24_7_count = '0'     #count of all open issues which are older than 24 hrs but less than 7 days

current timestamp - Now, we need to have date and time. comparng the current date/time and time of submission of issue, we can find the ageing of the issues. So, we initiially calculate the current date and time.

url - since, we have the repository name submitted by user. We need to frame a complete url that is valid and where the requied data can be found. so, after bit of workaround, I found that active issues data is available over page :
https://github.com/repo_full_name/issues (repo_full_name is the name of valid repo like for our reppository it is: amberagarwal1/flask_shipppable)

so, we have the page that need to be parsed. All the data lies wityhin this page but need to extracted carefully.
I searched for the pattern for each required count into the page and formulated regular expression.
So, now I have partterns and conditions that need to be applied to have asked counts.

So, at the end we did some manipulations to have count for each asked paramter.
And it all inlcuded pattern macthing and classifying the correct category based on timestamp.

So, results are displayed at templates/display.html which is called from the python function itslef to have count as arguments and page format is descrribed using HTML and CSS.


Please have a look at it  and download it and run it.

Any commments/suggestion.changes are welcome


Have A Good Day!!!
