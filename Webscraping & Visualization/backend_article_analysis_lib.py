# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 00:52:10 2021

@author: alexa
"""

import json
import os
import csv
import re

# Counts the tags, and adding them to a json as a dictionary
def create_json_tag_files(): #Alexander
    for year in range(2014, 2022, 1): # loops over the years
        if os.path.isfile("overview/"+str(year)+".json") == False: # checks if the json file exists 
            with open("overview/"+str(year)+".txt", "r", encoding='utf-8') as f: # loads the txt file
                f = f.read().split(', ') # reads the txt file, and separates the string and puts it into a list
                tag_dict = {}
                
                # Counts the occurrence of each word.
                for word in f:
                    if word != '':
                        if word not in tag_dict.keys():
                            tag_dict[word] = 1
                        else:
                            tag_dict[word] += 1
            # Dumps the content into a json file
            with open("overview/"+str(year)+".json", "w", encoding='utf-8') as j:
                json.dump(tag_dict, j, ensure_ascii=False)
                j.close()

# Reads all the tag files created above, and creates a single tag file, that contains the occurrences of each tag per year.
def make_complete_tag_list(): #Alexander
    # loads every json file
    for year in range(2014, 2022): 
        with open("overview/"+str(year)+".json", encoding='utf-8') as file:
            json_dict = json.load(file)
            file.close()
        # if the "complete_tag_list.py" file doesn't exists, the file is created and headers are made
        if os.path.isfile("overview/"+"complete_tag_list.csv") == False:
            with open("overview/"+"complete_tag_list.csv", "w", encoding='utf-16', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(["Year,"+"Tag,"+"Counter"])
                file.close()
        # the year, tags and counter is put into a list, and is appended to the "complete_tag_list.py" file
        with open("overview/"+"complete_tag_list.csv", "a+", encoding='utf-16', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for key, value in json_dict.items():
                print(key, value)
                writer.writerow([str(year)+","+key+","+str(value)])


# Adds filename of a given article to: "is in world cloud.txt" when it has been 
# added to the file: analyse_opened_article.csv. 
def add_to_word_cloud(article): #Alexander
    with open('overview/is in word cloud.txt', 'a+', encoding='utf-8') as file:
        file.write(str(article)+"\n")
    
        
# Checks if the filename already exists in the file: analyse_opened_article.csv.
# Makes it possible for the analyse_opened_article.csv to be updated, without having
# to go through files that have already been added to the file.
def is_in_word_cloud(article): #Alexander
    try:
        with open('overview/is in word cloud.txt', 'r', encoding='utf-8') as file:
            if article in file.read():
                return True
            return False
    except:
        return False
    
    
# Creates the file: "analyse_opened_article.csv" and creating headers.
# Inserts the exact file name, for reference when making the article recommendation system.
# inserts every tag that is represented in the article. 
# The words and frequency columns are linked, so for any given article, index 0 of frequency,
# represents index 0 of words.
def analyze_articles(): #Alexander 
    complete_article_list = os.listdir('articles')
    if os.path.isfile('overview/analyse_opened_article.csv') == False:
        with open('overview/analyse_opened_article.csv', 'w', encoding='utf-16',newline='') as file:
            writer = csv.writer(file, delimiter='|',quoting=csv.QUOTE_NONE)
            writer.writerow(['FILENAME','TAGS','TITLE','WORDS','FREQUENCY'])
            
    
    with open('overview/analyse_opened_article.csv', 'a', encoding='utf-16', newline='') as file:
        stopwords = open('stopwords.txt', 'r').read()
        
        for article in complete_article_list:
            writer = csv.writer(file, delimiter ='|',quoting=csv.QUOTE_NONE) # Using | as delimiter to avoid trouble with commas in the filename.
            index = article.index('tag; ') # creates an index of where the tags start, since they are subtracted from the filename
            if is_in_word_cloud(article) == False: # if the is present in the file: "is in word cloud.txt": skip next section 
                tags = article[index+5:-4] # Removes the first part "tags; " and the last part: ".txt
                count = 11 #Creates a index for the length of the date
                title = article[count:index] # subtracts the title from the filename
                
                #Removes all blank spaces in front of the title of the article
                while title[0] == ' ':
                    count+=1
                    title = article[count:index]
                    
                    
                with open('articles/'+str(article),'r', encoding='utf-8') as article_file:
                    dictionary = {}
                    for line in article_file.readlines(): # turns the file into str lines, and iterates over them
                        line = line.lower()
                        line = re.sub('[^a-z]', ' ', line) 
                        words = line.split(' ') # creates a list of all the words in the line
                        for word in words: #iterates over every element of the words list
                        
                            # Adds word to dictionary as key, and adding 1 to the value, if its not blank and not in stopwords.txt
                            if word != '' and word not in stopwords:
                                if word not in dictionary.keys():
                                    dictionary[word] = 1
                                else:
                                    dictionary[word] += 1
                    
                    #Reads the dictionary, iterates over the items, if value is two or higher, adds word and value to seperate strings.
                    word_str = ""
                    word_count_str = ""
                    for word, count in dictionary.items():
                        if count > 1:
                            word_str += word +";"
                            word_count_str += str(count) +";"
                            
                    #writes all the variables created above, to the "analyse_opened_article.csv" file.
                    writer.writerow([article,tags,title,word_str,word_count_str])
                    add_to_word_cloud(article)
                    print(article+" has been added to the word cloud history")

