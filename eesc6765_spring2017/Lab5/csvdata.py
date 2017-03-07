import csv
import operator

f = open( './Lab5.csv', 'rb')

w = open('./middle2.csv', 'wb')

final = open('./result2.csv', 'wb')



#======================SORT TO MIDDLE FILE

reader = csv.reader(f)
#reader.next()
writer = csv.writer(w)
writer.writerow(reader.next())  #copy the first row into the result file 
reader = sorted(reader, key=operator.itemgetter(4), reverse=False)

data = []
for row in reader:
    #print row[0]
    if row[0] not in data :
    	data.append(row[0])
    	writer.writerow(row)
f.close()
w.close()




#========================SELECT TO RESULT FILE



f = open( './middle2.csv', 'rb')

reader = csv.reader(f)
writer = csv.writer(final)
row0 = reader.next()
row0.append('SwitchOrNot')
writer.writerow(row0)
#print reader[0]
row = reader.next()
#print row

while True:
	#print '1'
	if row[1] == '1':   #routeId is 1
		#here we need to get an array to record consecutive route 1
		#print row[1]
		#print "asdf"
		routes = []
		#print "sdfa"
		routes.append(row)
		#print routes
		while (1) :
			try:
				row = reader.next()
			except:
				break
			if row[1] == '1':
				routes.append(row)
			elif (row[1] == '2' or row[1] == '3'):
				break
		for r in routes:
			if (r[5] < row[5]):  #this means route 1 gets 42th street earlier
				r.append('no')
				writer.writerow(r)
			else :
				r.append('yes')
				writer.writerow(r)
	try:
		row = reader.next()
	except:
		break





