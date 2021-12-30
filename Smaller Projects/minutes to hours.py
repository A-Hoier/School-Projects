# -*- coding: utf-8 -*-
"""
Converts minutes in to hours and minutes
"""

min = int(input("Type any number of minutes, and get a return of total hours and minutes: "))

hour = min/60
rounded_hour = int(hour)
min_left = min % 60

print(str(min) + " is equal to " + str(rounded_hour) + " hour(s) and " + str(min_left) + " minute(s)")
