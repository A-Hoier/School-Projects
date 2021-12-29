# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 10:09:11 2021

@author: baeks
"""

import pandas as pd
import re
import os
import json



#Takes list of tag(s) as input, and counts all the words in articles with the same tag(s), returns two lists:
# 1) all the words that has been used in the articles. 2) a list of the sum of how many times the word has been used
def find_article_words_from_tag(input_tag=0,Frequency=2): #Chris
    with open("overview/analyse_opened_article.csv", encoding = 'utf-16') as dataset:
            dataset = pd.read_csv(dataset,sep='|',error_bad_lines=False)
            df = pd.DataFrame(dataset)
                
            output_dict = {}
            sorted_output_list = [[],[]]
            index = 0
            
            # Iterating through every element of the df, and the tag list input from the drop down in dash
            while index<len(df):
                for tag in input_tag: 
                    
                    #Adding words and frequency of a article that has the same tags as we're searching for.
                    if tag.upper() in str(df['TAGS'][index]).upper():
                        pairs = [str(df['WORDS'][index]).split(';'),str(df['FREQUENCY'][index]).split(';')]
 
                        # Adding words and frequency as key value pairs to a dict and counting them, if 
                        # frequency of the word is > 2(can be changed as the function is called)
                        pair_index = 0
                        while pair_index < len(pairs[0])-1:
                           if int(pairs[1][pair_index])>=Frequency:
                               if pairs[0][pair_index] not in output_dict:
                                   output_dict[pairs[0][pair_index]] = 1
                               else:
                                   output_dict[pairs[0][pair_index]] += 1
                           pair_index += 1
                index += 1
            
            # Converts the dictionary to two lists within a list.
            tuple_output_list = sorted(output_dict.items(), key = lambda x: x[1],reverse=True)
            index = 0
            while index < len(tuple_output_list):
                sorted_output_list[0].append(tuple_output_list[index][0])
                sorted_output_list[1].append(tuple_output_list[index][1])
                index+=1
                
            return sorted_output_list

     

# Assigns scores to all articles in the folder, then returns the 5 highest-ranked articles.
def recommend_similar_articles(file_name): #Chris
    with open("overview/analyse_opened_article.csv", encoding = 'utf-16') as dataset:
        df = pd.read_csv(dataset,sep='|',index_col=0)

    # Sanitizes input from dataframe with different delimiters for each column.    
    search_tags = str(str(df.loc[file_name]['TAGS'].split(';')).split(','))
    search_words = str(df.loc[file_name]['WORDS'].split(';'))
    search_title = str(str(df.loc[file_name]['TITLE'].split(';')).split(' '))
    df.drop(file_name,inplace=True) #Doesn't count the currently shown article while scoring
     
    score_report = {}      
    for i, _ in df.iterrows():
        score_report[i] = 0
        
    index = 0
    while index<len(df):
        search_row = df.iloc[index]
        for tag in str(str(search_row['TAGS']).split(';')).split(','):
            if tag in search_tags:
                score_report[df.index[index]] += 20 # Tag matches count the most
    
        search_pairs = [str(df['WORDS'][index]).split(';'),str(df['FREQUENCY'][index]).split(';')]
        pair_index = 0
        while pair_index < len(search_pairs[0])-1:
            if search_pairs[0][pair_index] in search_words:
                score_report[df.index[index]] += min(int(search_pairs[1][pair_index]),8) # Word match scores depend on how often they are used.
            pair_index += 1
        
        for title_word in str(str(search_row['TITLE']).split(';')).split(' '):
            if title_word in search_title:
                score_report[df.index[index]] += 4 # Title word matches count some per match
                    
        index += 1
    
    best_articles_tuple_list = sorted(score_report.items(), key = lambda x: x[1],reverse=True)[0:5] # Sort the report and pass on the 5 best
    
    best_articles_list = [i[0] for i in best_articles_tuple_list] # Convert list of tuples to list
    
    best_articles_dict = [{'label':df.loc[article]['TITLE'],'value':article} for article in best_articles_list] # Convert list to list of dicts, attach their filename.

    return best_articles_dict


# Creates a dictionary of all possible search words in articles when called.
def find_search_terms(): #Chris
    with open("overview/analyse_opened_article.csv", encoding = 'utf-16') as dataset:
        df = pd.read_csv(dataset,sep='|',index_col=0)
        
    term_list=[]
    index = 0
    
    while index<len(df):
        search_row = df.iloc[index]
        for tag in re.split(';| |,',str(search_row['TAGS'])[:-1]):
            tag = tag.lower().replace('.','').replace('’',"'").replace('‘',"'")
            if tag[:1] == "'":
                tag = tag[1:]
            if tag[-1:] == "'":
                tag = tag[:-2]               
            if str(tag) not in term_list:
                print(tag)
                term_list.append(str(tag))
        
        for word in re.split(';| |,',str(search_row['WORDS'])[:-1]):
            word = word.lower().replace('.','').replace('’',"'").replace('‘',"'")
            if word[:1] == "'":
                word = word[1:]
            if word[-1:] == "'":
                word = word[:-2]
            if str(word) not in term_list:
                print(word)
                term_list.append(str(word))
        
        for title_word in re.split(';| |,',str(search_row['TITLE'])[:-1]):
            title_word = title_word.lower().replace('.','').replace('’',"'").replace('‘',"'")
            if title_word[:1] == "'":
                title_word = title_word[1:]
            if title_word[-1:] == "'":
                title_word = title_word[:-2]
            if str(title_word) not in term_list:
                print(title_word)
                term_list.append(str(title_word))
        index +=1

# Handles the exception where an empty entry is made from the split funtions. 
# If 'Voteman' is not the first scraped article, it might hit a wrong index as it is fixed.
        term_list.pop(2) 
        
    return term_list


# Lifts search term to return if file is present; otherwise requests it to be made, then dumps it as file before passing.
def get_search_term_dict(): #Chris
    if os.path.isfile("overview/search_term_dict.json"):
        with open("overview/search_term_dict.json", "r", encoding='utf-8') as file:
            term_dict = json.load(file)
    else:
        term_dict = [{'label' : phrase, 'value': phrase} for phrase in find_search_terms()]
        with open("overview/search_term_dict.json", "w", encoding='utf-8') as file:
            json.dump(term_dict, file)

    return term_dict


# Compares the given search term(s) with the article library, returns articles that match all given terms.
def return_searched_article_list(search_tag_list,article_list=None): #Chris
    if article_list is None: # For the first term, the article library is loaded as dataframe to search through.
        with open("overview/analyse_opened_article.csv", encoding = 'utf-16') as dataset:
            df = pd.read_csv(dataset,sep='|')
    else: # For second term onwards, converts the dict of articles matching previous terms to dataframe.
        df = pd.DataFrame.from_dict(article_list, orient='index', columns=['FILENAME','TAGS','TITLE','WORDS','FREQUENCY'])

    matching_article_dict = {} 
    search_tag = search_tag_list[0] 
    
    index = 0
    while index<len(df): # Returns all articles that match the current search term to dict.
        search_row = df.iloc[index]
        if (search_tag.upper() in str(search_row['TAGS']).upper()
         or search_tag.upper() in str(search_row['WORDS']).upper() 
         or search_tag.upper() in str(search_row['TITLE']).upper()):
            matching_article_dict[index] = search_row[0:5]
              
        index += 1    
    
    if len(search_tag_list)>1: # Calls the search function again to sieve the remaining articles if more terms are given.
        return return_searched_article_list(search_tag_list[1:],article_list=matching_article_dict)
    
    # If last term is handled, passes the dictionary to a Dash-compatible format with title and filename.
    return [{'label':matching_article_dict[key][2],'value': matching_article_dict[key][0]} for key in matching_article_dict.keys()]


# Reads requested filename, returns the text contents from it.
def open_requested_article(FILENAME): #Chris
    with open('articles/'+str(FILENAME), "r", encoding='utf-8') as article:
        text = article.read()

    return text
