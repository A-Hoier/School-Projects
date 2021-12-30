# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:50:55 2021

@author: alexa


Write a function that takes the dictionary in persons.py, which maps names to
ages, and prints the names of all persons that are aged in a given range from
minAge to maxAge, e.g., from 20 to 40.
"""

persons = {'Alice': 2, 'Bob': 31, 'Chloe': 56, 'Mozelle': 17, 'Margery': 31, 'Kasha': 15, 'Jacki': 75, 'Katheryn': 87, 'Robert': 41, 'Collin': 16, 'Marya': 23, 'Jeffery': 15, 'Maritza': 74, 'Sigrid': 56, 'Opal': 59, 'Kristie': 83, 'Kristofer': 34, 'Leonarda': 63, 'Nicholas': 38, 'Edgardo': 78, 'Dawna': 4, 'Nidia': 27, 'Rutha': 2, 'Salena': 18, 'Isis': 67, 'Ralph': 24, 'Penny': 85, 'Laurette': 83, 'Heather': 74, 'Shasta': 4, 'Rosita': 49, 'Debi': 2, 'Yvette': 33, 'Milo': 43, 'Lynette': 27, 'Lavone': 76, 'Lissa': 61, 'Patti': 30, 'Keva': 87, 'Marquitta': 23, 'Kristyn': 53, 'Gillian': 83, 'Audria': 82, 'Natacha': 53, 'Frederica': 59, 'Herman': 5, 'Laurence': 11, 'Queenie': 68, 'Nida': 9, 'Randal': 51, 'Valene': 36, 'Shira': 80}



import operator
personssorted = sorted(persons.items(), key=operator.itemgetter(1))
ps = {}

def age_find(min_age, max_age):
    for k, v in persons.items():
        if min_age > v < max_age:
            print(k)


age_find(20, 40)