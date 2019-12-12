#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup
import csv
import re
from multiprocessing import Pool
from fake_useragent import UserAgent
import base64

def getUrls(row):
	headers = {'User-Agent': ua.random}
	url = 'https://www.tripadvisor.com' + row['attraction_url']
	print url
	result = []

	location_id = ''
	attraction_id = ''
	about = ''
	location = ''
	contact = ''
	region = row['region']

	try:
		location_id = re.search(r'[g]\d{1,12}', str(url)).group(0)
		location_id = re.findall(r'\d+', location_id)[0]
	except:
		pass
	try:
		attraction_id = re.search(r'[d]\d{1,14}', str(url)).group(0)
		attraction_id = re.findall(r'\d+', attraction_id)[0]
	except:
		pass
	try:
		about_url = 'https://www.tripadvisor.com/data/1.0/attraction/about/' + attraction_id
		about_r = requests.get(about_url, headers=headers)
		about = about_r.content
	except:
		pass
	try:
		location_url = 'https://www.tripadvisor.com/data/1.0/location/' + attraction_id
		location_r = requests.get(location_url, headers=headers)
		location = location_r.content
	except:
		pass
	try:
		contact_url = 'https://www.tripadvisor.com/data/1.0/attraction/company-supplier/contactcard/' + attraction_id
		contact_r = requests.get(contact_url, headers=headers)
		contact = contact_r.content
	except:
		pass
	result = [url, location_id, attraction_id, about, location, contact, region]
	return result

if __name__ == '__main__':
	ua = UserAgent()
	proxy = 'Damian:berl1n2015@world.proxymesh.com:31280'
	proxies = {'http': 'http://%s' % proxy, 'https': 'http://%s' % proxy}

	file = open('Arival_NORTH_AMERICA_data/details_north_america4.csv', 'w')
	fieldnames = ['url', 'location_id', 'attraction_id', 'about', 'location', 'contact', 'region']
	writer = csv.DictWriter(file, fieldnames=fieldnames)
	writer.writeheader()	
	
	with open(sys.argv[1], 'rb') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		pool = Pool(10)
		for result in pool.map(getUrls, reader):
			try:
				writer.writerow({'url': result[0], 'location_id': result[1], 'attraction_id': result[2], 'about': result[3], 'location': result[4], 'contact': result[5], 'region': result[6]})
				print result[0], result[1], result[2]
			except Exception as e:
				print e				

	file.close()