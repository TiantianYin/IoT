import random
import time
import thread
import sys

num = 0

f = open("static/temp.txt", "w+")
f.write("0 0 0 0 0 0 0 0 0 0")
f.close()

while (True):
	f = open("static/temp.txt", "r+")
	TEMP = str(random.randint(10,30)) 

	line = f.readline()

	print line
	sys.stdout.flush()

	arr = line.split( )

	del arr[0]
	arr.append(TEMP)
	s = ''
	for x in arr:
		s = s + x + " "
	s = s.strip()
	f.seek(0)
	f.write(s)
	print s
	sys.stdout.flush()

	f.close()
	time.sleep(3)
