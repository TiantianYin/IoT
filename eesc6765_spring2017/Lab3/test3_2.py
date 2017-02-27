import threading

with open('key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()

def task1():
	newUpdate = mtaUpdates(APIKEY)
	tr = newUpdate.tripUpdates
	v = newUpdate.vehicles
	#add to AWS
	return


def task2():
	#View all data from
	#check and delete
	return


def worker(num):
    """thread worker function"""
    print 'Worker: %s' % num
    try:
    	while (1):
    		if num == 0:
    			task1()
    		else:
    			task2();
    		sleep(30)

    except KeyboardInterrupt:
    		exit
    return

threads = []
for i in range(2):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
