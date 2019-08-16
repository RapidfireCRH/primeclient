import sys
import math
import mysql.connector
import socket
import db

checkoutnum = 1000
hostname = socket.gethostname()

def checknum(int_to_check):# false is not prime
    def isdiv(x, y):# false is not divisable
        if(y%x==0):
            return True
        else:
            return False
    
    sqrt_of_num = math.ceil(math.sqrt(int_to_check))
    mylist = db.query("select prime from onemillion where prime <= {0}".format(sqrt_of_num))
    for prime in mylist:
        if(isdiv(prime[0],int_to_check)):
            return False
    return True

def checkout(lastendnum):
    def checkoutwrite(low, high):
        if(db.query("select name from Checkout where name = \"{0}\"".format(hostname))):
            db.update("update Checkout set low={0}, high={1} where name = \"{2}\"".format(low, high, hostname))
        else:
            db.insert("insert into Checkout (low, high, name) values (%s, %s, %s)",(low, high, hostname))

    cb = 0#check_begin
    ce = 0#check_end
     #Check if already checked out when lastendnum == 0
        #true -> return checkout data
        #false -> next code
    if lastendnum == 0:
        q = db.query("select name from Checkout where name = \"{0}\"".format(hostname))
        if(q is not None and len(q) != 0):
            if(q[0][0] == hostname):
                cb , ce = db.query("select low, high from Checkout where name = \"{0}\"".format(hostname))[0]
                if(cb != 0):
                    return cb, ce

    #Check for highest in checkouttable
    #Val > 0 -> True -> return Val, val + checkoutnum
    #Val == 0 -> False -> next code
    checkoutwrite(0,0)
    end = db.query("select max(high) from Checkout")
    end2 = db.query("select max(prime) from onemillion")[0][0]
    if(end is not None and end[0][0] != 0):
        if(end2 < end[0][0]):
            cb = end[0][0]+1
            ce = cb + checkoutnum
            checkoutwrite(cb,ce)
            return cb, ce

    #check for highest completed in primes
    #return val, val + checkoutnum
    cb = end2 + 1
    ce = cb + checkoutnum
    checkoutwrite(cb,ce)
    return cb, ce



def __main__():
    check_begin, check_end = checkout(0)
    currentnum = check_begin - 1
    hostnamenum = db.query("select id from checkout where name = \"{0}\"".format(hostname))[0][0]
    while True:
        if(db.query("select count(prime) from onemillion")[0][0] == 1200000):
            exit()
        currentnum = currentnum + 1
        if(currentnum >= check_end + 1):
            check_begin, check_end = checkout(check_end)
            currentnum = check_begin
            print("{0}".format(currentnum))
        if(checknum(currentnum)):
            db.insert("insert into onemillion (prime, hostname) values (%s, %s)",(currentnum, hostnamenum))

__main__()
