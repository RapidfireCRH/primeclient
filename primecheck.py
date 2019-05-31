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
	mylist = db.query("select prime from primes where prime <= {0}".format(sqrt_of_num))
	for prime in mylist:
		if(isdiv(prime[0],int_to_check)):
			return False
	return True

def checkout(lastendnum):
	def delcheckout():
		db.delete("delete from Checkout where hostname = \"{0}\"".format(hostname))
	
	check_begin = 0
	check_end = 0
	#check that hostname does not already have a checkout
	if(lastendnum == 0):# If it is the first time run, read from db and see if it is restarting
		q = db.query("select hostname from Checkout where hostname = \"{0}\"".format(hostname))
		if(len(q) != 0):
			if(q[0][0] == hostname):
				#if hostname does exist, populate begin and end with appropriately checked out values
				check_begin, check_end = db.query("select start, end from Checkout where hostname = \"{0}\"".format(hostname))[0]
				return (check_begin, check_end)
	else:
		delcheckout()
		if(
		end = db.query("select end from Checkout")
		#If nothing checked out, check that table is not empty first
		if(len(end)==0):
			check_begin = db.query("select max(prime) from primes")[0][0] + 1
		else:
			for s in end:
				if(s[0] > check_begin):
					check_begin = s[0] + 1
		check_end = check_begin + db.checkoutnum
		db.insert("insert into Checkout (start, end, hostname) values (%s, %s, %s)",(check_begin, check_end, hostname))
		#insert hostname and biggest output +1
		return (check_begin, check_end)



def __main__():
	check_begin = 0
	check_end = 0
	currentnum = 0
	while True:
		currentnum = currentnum + 1
		if(currentnum >= check_end + 1):
			if(currentnum != 1):
			check_begin, check_end = checkout(check_end)
		if(checknum(currentnum)):
			db.insert("insert into primes (prime, added_by) values (%s, %s)",(currentnum, hostname))
			print("{0}: prime".format(currentnum))

__main__()
