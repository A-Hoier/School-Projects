# -*- coding: utf-8 -*-

import time


def Primes_until(n):
    start = time.time()
    prime_list = list(range(2, n+1))
    
    for i in range(2,int(n**0.5+1)):
        for number in prime_list:
            if number != 0:
                if number%i == 0 and number != i:
                    prime_list[number-2] = 0
    end = time.time()
    

    print(list(filter(lambda a: a != 0, prime_list)))
    
    print("time used: ", end-start, " seconds")



Primes_until(10000)