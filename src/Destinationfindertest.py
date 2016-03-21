import DestinationFinder as DST
import urllib2
from datetime import datetime
import peewee
import time
import dataset
import psycopg2
from psycopg2.extensions import AsIs
from playhouse.dataset import DataSet
import sqlalchemy
import json
from pymongo import MongoClient
from porc \
	import Client
#from sqlalchemy import create_engine
#from sqlalchemy.schema import MetaData
from pymongo import MongoClient
conn_string = "host='192.168.1.8' dbname='sabre' user='postgres' password='Lokifish123'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
# psql_db = PostgresqlExtDatabase('sabre', user='pi', password=  'raspberry',host='192.168.1.8')


#db = PostgresqlExtDatabase('sabre', user='pi', password='raspberry', host='192.168.1.8')

#conn_str = 'postgresql://pi:raspberry@192.168.1.8:5432/sabre'
#engine = create_engine(conn_str)

# orchestrate.io connection
#client = Client('dfe9973f-e962-4cde-bf1e-f0bf0fc85384')
#client.ping().raise_for_status()

# mongo
#client = MongoClient("mongodb://localhost:27017")
client = MongoClient("mongodb://192.168.1.8:27017")

# collection = db1.sabre_cpm
Src_airports = [line.strip() for line in open("C:\\Users\\gilby\\PycharmProjects\\PySabre\\src\\origins.txt", 'r')]
# set cpm
cpm = '.05'


pdb = dataset.connect('postgresql://pi:raspberry@192.168.1.8:5432/sabre')





for i in Src_airports:
	try:

		cal = DST.DestinationFinder()

		cal.origin(i)
		cal.pricepermile(cpm)
		cal.lengthofstay([5, 6, 7, 8, 9, 10, 11, 12])
		# cal.pointofsalecountry("US")

		#print(cal.call())
		#print(type(cal.call()))
		print(i)
		print(cal.call())
		var = cal.call()

		#print (cal.call())
		#conn_string = "host='localhost' dbname='sabre' user='postgres' password='Lokifish123'"
		#conn = psycopg2.connect(conn_string)
		#cursor = conn.cursor()
		#cursor.execute("insert into sabre_results (data) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",json.dumps([var],))
		#cursor.execute("INSERT INTO sabre_results(data) VALUES (  %s)", json.dumps(var,))
		#cursor.execute("INSERT INTO sabre_results(data) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", json.dumps(res,))
		#cursor.execute("INSERT INTO product(store_id, url, price, charecteristics, color, dimensions) VALUES (%s, %s, %s, %s, %s, %s)", (55,  'http://www.google.com', '$20', cal.call(), 'red', '8.5x11'))
		#time.sleep(3)
		#conn.commit()
		#cursor.close()
		#pdb = dataset.connect()
		#table = pdb['json_results']
		print type(var)
		with open('data.txt', 'w') as outfile:
			json.dump(cal.call(), outfile, sort_keys = True, indent = 4,
		ensure_ascii=False)
		#table.insert(var)

		db = client.sabre_results
		fare = ({"author": "Bryan Gilbertson",
	    #"fare": var,
	    "origin": var['OriginLocation'],
	    "Destination": var['FareInfo'][0]['DestinationLocation'],
	    "lowfare": var['FareInfo'][0]['LowestFare'],
	    "PricePerMile": var['FareInfo'][0]['PricePerMile'],
		"DepartureDateTime": var['FareInfo'][0]['DepartureDateTime'],
		"ReturnDateTime": var['FareInfo'][0]['ReturnDateTime'],
	    "date": datetime.now()})
		#fares = db.fares
		print var['FareInfo'][0]['LowestFare']
		result = db.sabre_cpm.insert_one(fare).inserted_id
		#db.sabre_cpm.insert({ "created_date": datetime.now() })
		#time.sleep(3)
	except urllib2.HTTPError, e:
		if e.code == 401:
				print 'Unauthorized'
		elif e.code == 404:
				pass
				print 'CPM greater than ' + cpm + " @ " + i

		elif e.code == 503:
				print 'service unavailable'
		else:
				print 'unknown error: '
				print "ERROR: ", e.read()
#conn.close()