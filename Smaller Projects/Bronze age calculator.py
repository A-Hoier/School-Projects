# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 08:31:32 2021

@author: alexa
"""
input("Welcome to the Bronze Age Calculator!\nPress enter to continue...")
num1 = input("Enter the first number: ")
num2 = input("Enter the second number: ")

Operation = input("Choose one of the following operations: \n1 - Addition \n2 - Subtraction \n3 - Multiplication \n4 - Division \n_________________\n")
if int(Operation) == 1:
    print("Doing addition")
    result = int(num1) + int(num2)
    print(num1 + "+" + num2 + "=" + str(result))
if int(Operation) == 2:
    print("Doing subtraction")
    result = int(num1) - int(num2)
    print(num1 + "-" + num2 + "=" + str(result))
elif int(Operation) == 3:
    print("Doing multiplication")
    result = int(num1) * int(num2)
    print(num1 + "*" + num2 + "=" + str(result))
elif int(Operation) == 4 and int(num2) == 0:
    print("Unable to divide by zero")
elif int(Operation) == 4:
    print("Doing division")
    result = int(num1) / int(num2)
    print(num1 + "/" + num2 + "=" + str(result))
print("Thanks for using the Bronze age calculator")




