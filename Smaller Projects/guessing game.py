# -*- coding: utf-8 -*-
"""
A Guessing game made during the second week of programming.

Have fun
"""
import random
num = random.randrange(1,1001)

wrong_count = 1


name = input("Hello, what is your name? ")
intro = input("Hello " + name + " would you like to play a game? yes (y) or no (n): ")
if intro.lower() == "y":
    print("welcome")
elif intro.lower() == "n":
    exit()

if intro.lower() == "y":
    print("In this game, you'll have to guess a number between 1 and 1000")
    guess = input("Take your first guess: ")
while int(guess) != num:
    wrong_count = wrong_count +1
    if int(guess) > num:
        guess = input("WRONG! too high: ")
    if int(guess) < num:
        guess = input("WRONG! too low: ")
print("Very nice! Well done on guessing the secret number")
print("It only took you ", wrong_count, " tries to guess the number!")
input("thank you for playing " + name + ", press enter to exit... ")