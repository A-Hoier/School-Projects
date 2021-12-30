# -*- coding: utf-8 -*-

"""
taking the avg of tuples and returning it.

note that it's the avg of the first number of every tuple, follow by the second
number of each tuple etc.
"""

t1 = ((10, 10, 10, 12), (30, 45, 56, 45), (81, 80, 39, 32), (1, 2, 3, 4))

for i in zip(*t1):
    print([sum(i)/len(i)])
    
    

print([sum(i)/len(i) for i in zip(*t1)])