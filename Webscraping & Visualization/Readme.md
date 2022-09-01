
### Authors: Chris Bæk and Alexander Høier as part of our programming course

## The exam of the programming course - webscrape every article from www.thelocal.com and create some visual insights like usage of tags and wordclouds. Further, create way to get recommendations of new articles, based on the currently selected one. 

# While the code chunks are delegated and written mostly individually, we have done a significant amount of cross-reviewing of each others' code, some of which we also edited together afterwards. Therefore, the coding cannot be attributed to each person as sharply as the overview suggests.


Step 0 (Before opening Spyder, assuming using a Windows machine):

	* Open Regedit.msc 
	* Change key "Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled to '1'"
	* Restart the computer when the file has been changed

# This is done to avoid errors due to long filenames, as we use the filename of each article to store its tags, some of which can be long.



Step 1 (Running Dash the first time):

	* Open 'main.py' 
	* Either run each block individually using CTRL+ENTER or simply run the whole file normally.
	* If SSL-certificate problems occur when running the first block, uncomment line 103 and 148 and comment line 102 and 147 in DS831lib.py.
		# This will disable SSL authentication, which gets around the issue of Spyder having an outdated Certificate repository.

# This will run all necessary functions in the respective libraries to perform all tasks given in the assignment.
 
# 'DS831lib.py' scrapes Thelocal.dk for articles.

	# It has a runtime of approx. 2 hours. if set to scrape from 2014-2021
	# The article titles are named with the date of release, article title, and tags.
	# They will be stored in your working directory in the folder; articles.

	# For every date you scrape, the date is added to the file "scraping_history", 
	# and the program will recognize the date as already been scraped. Further, the file
	# 'list_history' also has the date and includes an errorcode, if no articles are found
	# on the given date.

	# In the overview folder, there will be a tag counter for every year, and article overview
	# file containing an overview of all the articles that has been scraped, and a file containing
	# all the dates of which an error has occured, as well as the error code.

	# if the connection keeps getting repeatedly closed by the remote server, please allow a couple of
	# hours to pass, before trying again. If the kernel freezes, delete the last scraped date
	# from the article_overview file, from the scraping_history file and all the articles included
	# in that date from the article folder.
	# Known server-side errors: 2020-08-25 contains 4 NoneType server response errors.

	# The function scraper.call_scrapes() takes three arguments; year, month, date respectively. 
	# for single digits in month and date, don't add 0's before the actual digit. 
	# Thelocal's archive starts 2008/01/01, but no articles are present before May 2014. 


# 'backend_article_analysis_lib.py' performs the preliminary preparation of the scraped data for further use.

	# analysis.create_json_tag_files() converts the .txt tag files for each year to .json files.
		# It will throw an error if it hits a year between 2014 and 2021 with no articles scraped.
		# This will happen if you stop the scraper before 2021.
		# Prior years will be handled correctly, so no functionality is lost for the Dash app.
	# analysis.make_complete_tag_list() creates a CSV list to be used in Dash later to choose tags from.
		# It will throw an error if it hits a year between 2014 and 2021 with no articles scraped.
		# This will happen if you stop the scraper before 2021.
		# Prior years will be handled correctly, so no functionality is lost for the Dash app.
	# analysis.analyze_articles() creates a comprehensive csv-file with multiple parameters of interest
	# which is later used real-time in Dash. It contains colums for: [FILENAME|TAGS|TITLE|WORDS|FREQUENCY].


# 'Dash_app' runs the web application.
	
	# Almost all app callbacks refers to functions stored in 'function_lib.py', which provides the information
	# needed in realtime to show data as requested.
	
	# The first time Dash_app is run, there is a longer pre-load time than for subsequent runs, as explained below.

# 'function_lib.py'  provides real-time data whenever called on by Dash_app. It is thus never run directly.

	# get_search_term_dict is split into two functions; the first checks if a search term dictionary file has
	# already been created, and if yes, simply feeds that to Dash. Otherwise, it calls find_search_terms, which
	# creates a search term dictionary file, saves it, then returns it. This causes the longer load on first run.



Step 2 (Subsequent runs):
	
	# Only run the Dash_app block using CTRL+ENTER.



Step 3 (Scrape newer articles):
	
	* In order to scrape articles published since last run, first delete the .JSON and .txt file for the current
	  year in the overview folder ("overview\year.[txt,json]) as well as search_term_dict.json from the same folder.
	* Run all three blocks again, and articles from the new dates are added and properly analyzed before running Dash.


