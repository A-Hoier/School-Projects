# -*- coding: utf-8 -*-



import csv 
import os
import json
from urllib.request import urlopen, Request
import urllib
from bs4 import BeautifulSoup
import datetime
import time


"""
This file will start scraping articels from thelocal.dk's webpage.
In the bottom, the line, call_scrapes() will begin the scraping of the content.

The article titles are named with the date of release, article title, and tags.
They will be stored in your working directory in the folder; articles.

For every date you scrape, the date is added to the file "scraping_history", 
and the program will recognize the date as already been scraped. Further, the file
'list_history' also has the date and includes an errorcode, if no articles are found
on the given date.

In the overview folder, there will be a tag counter for every year, and article overview
file containing an overview of all the articles that has been scraped, and a file containing
all the dates of which an error has occured, as well as the error code.

if the connection keeps getting close by the remote server, please allow a couple of
hours to pass, before trying again. If the kernel freezes, delete the last scraped date
from the article_overview file, from the scraping_history file, all the articles included
in that date from the article folder, as well as all the tags from the articles from the
tag_counter from the given year.

The below code will execute scraping of articles from thelocal.dk. THe function
takes three arguments; year, month, date respectively. for single digits in month and date,
don't add 0's before the actual digit. Thelocal's archive starts 2008/01/01, but no articles
are present before May 2014.

By the end of the year, I will add some code which will provice a nice visual 
overview of the content of the files, as well as some other nice features.

Happy scraping
"""


print(os.getcwd())
# When called, adds the input date to the list of dates to be scraped and adds any errorcode returned with it, as is the case with some excepts later.
def add_to_list_history(date,errorcode=None):
    with open("overview/list_history.txt", "a+") as f_a:
        f_a.write(str(date)+str(errorcode)+"\n")

# When called, adds the input date to the list of completely scraped dates.
def add_to_scraping_history(date):
    with open("overview/scraping_history.txt", "a+") as f_a:
        f_a.write(str(date)+"\n")
 
# When called, writes the input arguments to the overview file as CSV.        
def add_to_overview(date, title, tag_string):
    if os.path.isfile("overview/Article_overview.csv")==False: #Checks if the file exists; if it doesn't, it is created first with columns in row 1.
        #As the file is used in a "with" indentation in the following two sections, it is automatically closed when un-indenting.
        with open("overview/Article_overview.csv", "a+", encoding='utf-16', newline='') as f:
            columns='date,title,tags'
            temp=csv.writer(f)
            temp.writerow([columns])
    overview = date + ", " + title + "," + tag_string.replace(',',';')
    with open("overview/Article_overview.csv", "a+", encoding='utf-16', newline='') as f:
        temp = csv.writer(f)
        temp.writerow([overview])

# When called, adds the date and current article to a list of errors to be checked and retried after running the scrape.
def add_to_error_dates(date,article):   
    with open("overview/error_date_list.csv", "a+", encoding='utf-16', newline='') as f:
        temp = csv.writer(f)
        temp.writerow([str(date.replace("-",""))+','+str(article)])

# This is the main function to be activated from the outside and calls the rest of the file.
# It creates the subfolders used in the file and takes the desired starting date, 
# then crawls through each date, calling the other functions as relevant if scraping has not already been done for that date.
def call_scrapes(yyyy=2008,mm=1,dd=1):
    if not os.path.isdir("articles"):
        os.mkdir("articles/")
    if not os.path.isdir("overview"):
        os.mkdir("overview/")
    time.sleep(1)
    news_date = datetime.date(yyyy, mm, dd)
    end_date = datetime.date.today()
    delta = datetime.timedelta(+1)
    n=0
    article_list=[]
    while news_date<end_date:
        news_date_optimized = news_date.strftime('%Y/%m/%d ') #Creates a date format to be used for scraping URL
        news_date_filetype=news_date_optimized.replace("/", "-") #Creates a date format to be used for scraping the archive
        header=headers(n) #Cycles through each header for that date
        n=(n+1)%5 #Cycles through each header for that date
        #Checks if the current date has been scraped, then calls the relevant functions and feeds them the required arguments if not.
        if check_scraping_history(news_date) == True:
            pass
        else:
            article_list=(scraping_thelocal_archive(news_date_optimized,news_date_filetype,header))
            scraping_thelocal_article(article_list, news_date_filetype,header)
        news_date+=delta

# When called, checks if the input date has already been scraped, otherwise returns False.
def check_scraping_history(date):
    if os.path.isfile("overview/scraping_history.txt") == True:
        with open("overview/scraping_history.txt", "r") as f_r:
            if str(date) in f_r.read():
                return True
            return False
    return False

# Creates a list of headers to cycle through and returns whichever header the index asks for when called.
# We are adding headers in this way to get around Thelocal's script blocker.
def headers(index):
    Header1 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    Header2 = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/74.0.3729.169 Safari/537.36"
               "referer"}
    
    Header3 = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0)' 
               'AppleWebKit/537.36 (KHTML, like Gecko)' 
               'Chrome/96.0.4664.45 Safari/537.36'}
    
    Header4 = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X)'
               'AppleWebKit/605.1.15 (KHTML, like Gecko)'
               'CriOS/96.0.4664.53 Mobile/15E148 Safari/604.1'}
    
    Header5 = {'user-agent': 'Mozilla/5.0 (Linux; Android 10)' 
               'AppleWebKit/537.36 (KHTML, like Gecko)' 
               'Chrome/96.0.4664.45 Mobile Safari/537.36'}
    
    Headers_list = [Header1, Header2, Header3, Header4, Header5]    
    return Headers_list[index]
     

# This function does the bulk of the actual article scraping and calls other functions as needed to do individual processes.
def scraping_thelocal_article(article_list, date, header):
    if isinstance(article_list, list) == True: #Checking if article list is a list, if it's not a list, there are no article on the given date.    
        for article in article_list: #Looping over every article present on the date
            try: # In order to catch unforseen errors, the scraping process is in a try:except
                req = Request(url=article, headers=header) #Requesting the url with headers
                html = urlopen(req).read() # using urlopen and the read function to 
                doc = BeautifulSoup(html, 'html.parser') #Using beautifulsoup to parse the html-code
                title = str(doc.find("title").string) #Finding the title of the article by searching the html code
                title = title.replace(":", ";").replace("?", ".").replace("/", "-").replace("\\", "-").replace("*", ".").replace(">", "{").replace("<", "}").replace("|", ".").replace("\"", "\'").replace("ć", "´c")
                while title[0]==" ": #Most articles have excess spaces before their name. This loop removes all spaces at the start of a string,
                    title=title[1:] #so that the file names are standardized.
                #The title.replace is done to remove all characters unusable for filenames in Windows 
                     
                # Getting all the tags from the article, appending them to a list as well as putting them in a string.
                tag = doc.find_all(class_="entry-meta-tag")
                tag_list = []
                for line in tag:
                    tag_list.append(line.string)
                tag_string = ', '.join(tag_list)
                
                                                
                intro = str(doc.find(id='article-intro').string) # saving the intro of the article to a variable
                
                # Removing all hyperlinks, recommendations and scripts
                junk = doc('ul') + doc('strong') + doc('script')
                for x in junk:
                    x.decompose
                
                #Creating the file name variable with the date, title and tags, and opening a file with that name
                file_name = date + " " + title + " tag; " + tag_string
                temp_var = open("articles/"+file_name+".txt", 'w', encoding='UTF-8')
                
                #Writing the intro and the body from the article
                temp_var.write(intro)
                temp_var.write(doc.section.text)
                

                tag_counter(str(date), tag_string)#Calling the function for counting the tags for each year
                add_to_overview(str(date), title, tag_string) #Calling the function that will add the date, article and tags to an overview csv file

                temp_var.close() # Closing the file
                print('Article "',title,'" has been successfully scraped.',sep='') #Keeps the user updated
            except Exception as e: #Informs the user if an exception occurs and awaits further input.
                print('The article has encountered an error during scraping and is added to the list of error dates.')
                print('To amend this, delete the date from the scraping history and any articles from the overview file with that date and run again.')
                print('Encountered error:\n'+str(e)) #Prints the exception for the user to study.y
                add_to_error_dates(date,article) #Calls the error function.
                response=input('Vil du fortsætte med scraping? [y/n]') #Terminates the program if user doesn't confirm continuing.
                if response.lower() =="y":
                    pass
                else:
                    raise SystemExit
    add_to_scraping_history(date) # Calls function to add to scraped history after successfully completing the article list for the given date. 
            

def scraping_thelocal_archive(news_date,news_date_filetype,header): 
    """
    This part is scraping thelocal.dk, and uses the date input, to navigate to a specific date.
    For each date, it returns a list of all the article urls.  
    """
    #Creates the url based on the base url and the date from the input
    url_req = "https://www.thelocal.dk/" + news_date
    
    # Request the url using urllib library. The header used is specified in the headers function. 
    req = Request(url=url_req, headers=header) 
    
    # Using a try except. When the date has no articles, the Request returns an error, 
    # Which is handled by the except
    try:
        # using urlopen with the read function to create readable html code
        html = urlopen(req).read()
        
        #Using beautiful soup to parse the html code
        doc = BeautifulSoup(html, 'html.parser')
        # Puts all the articles in the div variable, ready for further processing
        div = doc.find(class_="article-list-container")
        
        #Creates two empty lists. the first for loop searches for all a's in the div variable, and appends 
        # all hyperlinks found to the "links" list. The div variable contain all links to articles twice,
        # therefore, the second for loop appends the hyperlink from the "links" list to the "article_list",
        # if it doesnt already exist.
        links = []
        article_list = []
        for article in div.find_all('a'):
            links.append(article.get('href'))
        for link in links:
            if link not in article_list:
                article_list.append(link)
                add_to_list_history(news_date_filetype) 
                
               
        print('\n'+"Downloading from date: "+str(news_date_filetype)[:-1]+': '+str(len(article_list))+' articles.',sep='')
        # Returns the article list
        return article_list
    
    # This exception handles all the dates containing no articles, and adds the date to the history of scraped dates with.
    except urllib.error.HTTPError as err:
        add_to_list_history(news_date_filetype,err)
        print('\n'+'No articles found for '+str(news_date_filetype)[:-1]+'.',sep='')
        pass


def tag_counter(date, tag_string):
    
    """
    This function creates a new json file for every year, and counts
    how many times each tag is used.
    """
    # Changes the date to a string object, and creates a year variable
    date = str(date)
    year = date[0:4]
    
    # This part checks if tag counter exists as a txt file. If it doesn't exist(happens only january first), it
    # creates the files, and writes the tag to the text file, seperated with a comma and a space.
    if os.path.isfile("overview/"+year+".txt") == False:
        with open("overview/"+year+".txt", "w+") as temp_txt:
            temp_txt.write(tag_string)
            temp_txt.write(", ")
            
    # This part appends the tag to the csv file. To celebrate the end of the year, a dictionary is created,
    # counting how man times a tag has been used. This dictionary is passed to a csv file
    elif date[5:10] == "12-31":
        tag_dict = {}
        with open("overview/"+year+".txt", "a+") as temp_txt:
            temp_txt.write(tag_string)
        
       # temp_txt.close()
        
        with open("overview/"+year+".txt") as file:
            lines = file.read().split(', ')
            for word in lines:
                if word != "":
                    if word not in tag_dict.keys():
                        tag_dict[word] = 1
                    else:
                        tag_dict[word] += 1
             
        with open("overview/"+year+".json", "w+", encoding='utf-8') as f_w:
            json.dump(tag_dict, f_w, ensure_ascii=False)
    
    #This is the codeblock that is running most of the time, every day, except 1/1 and 31/12 this part is
    # appending the tags to the txt file
    else:
        with open("overview/"+year+".txt", "a+", encoding='utf-8') as temp_txt:
            temp_txt.write(tag_string)
            temp_txt.write(", ")


with open("__init__.py", "w") as f:
    f.close()
    
call_scrapes() 
