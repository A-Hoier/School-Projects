# -*- coding: utf-8 -*-
"""
Creates a fun diamond shape
"""

useri = int(input("enter the number of rows of half of the diamond: "))



for i in range(1, useri*2, 2):
    print(int(useri-i/2) * " ", i * "*", int(useri-i/2) * " ")

for j in range(useri*2-3, 0, -2):
    print(int(useri-j/2) * " ", j * "*", int(useri-j/2) * " ")


