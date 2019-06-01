import sys
import math
from os import system
import db
import datetime
import socket

hostname = socket.gethostname()

def checknum(int_to_check):# false is not prime
    def isdiv(x, y):# false is not divisable
        if(y%x==0):
            return True
        else:
            return False
    sqrt_of_num = math.ceil(math.sqrt(int_to_check[0]))
    mylist = db.query("select prime from primes where prime <= {0} and DoubleCheck = 1".format(sqrt_of_num))
    for prime in mylist:
        if(isdiv(prime[0],int_to_check[0])):
            return False
    return True

def __main__():
    
    print("Loading DB...")
    maxnum = db.query("select max(num) from primes")
    rangenum = math.ceil(maxnum[0][0]/10000)
    for x in range(int(rangenum)):
        cor = 0
        notcor = 0
        database = db.query("select prime from primes where num between {0} and {1} and DoubleCheck = 0".format((x*10000),((x+1)*10000)))
        curtime = datetime.datetime.now()
        print("{3}|{1} - {2}: DB Loading Complete, {0} lines loaded".format(len(database),(x*10000),((x+1)*10000),curtime.strftime("%X")))
        for primecheck in database:
                if(checknum(primecheck)):
                    cor = cor + 1
                    if(cor%1000 == 0):
                        print("Correct So Far: {0}".format(cor))   
                    db.update("update primes set DoubleCheck = 1 where prime = {0}".format(primecheck[0]))
                    curtime = datetime.datetime.now()
                    db.update("update primes set DC_TimeStamp = \'{0}\' where prime = {1}".format(curtime.strftime("%s"), primecheck[0]))
                else:
                    print("{0} not prime".format(primecheck))
                    notcor = notcor + 1
        print("{0} correct, {1} not correct".format(cor, notcor))

__main__()
