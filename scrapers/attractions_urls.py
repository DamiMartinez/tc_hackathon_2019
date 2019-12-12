#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup
import csv
import re
from multiprocessing import Pool
from fake_useragent import UserAgent

def getUrls(row):
	headers = {'User-Agent': ua.random}
	url = 'https://www.tripadvisor.com' + row['category_url']
	# print url
	result = []

	try:
		r = requests.get(url, headers=headers)
		c = r.content
		
		soup = BeautifulSoup(c, 'lxml')
		attractions = soup.find_all(class_="listing_title")
	except:
		print 'Error request'
		attractions = []

	for attraction in attractions:
		try:
			print attraction.a['href'] + ', ' + url
			result.append([attraction.a['href'], row['region']])
		except:
			try:
				print re.findall('/Attraction(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\)]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', attraction.a['onclick'])[0][:-2] + ', ' + url
				result.append([re.findall('/Attraction(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\)]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', attraction.a['onclick'])[0][:-2], row['region']])
			except Exception as e:
				print e, url
				pass

	return result

if __name__ == '__main__':
	ua = UserAgent()
	proxy = 'Damian:berl1n2015@world.proxymesh.com:31280'
	proxies = {'http': 'http://%s' % proxy, 'https': 'http://%s' % proxy}

	file = open('Arival_NORTH_AMERICA_data/attractions_urls_list_north_america.csv', 'w')
	fieldnames = ['attraction_url', 'region']
	writer = csv.DictWriter(file, fieldnames=fieldnames)
	writer.writeheader()
	
	with open(sys.argv[1], 'rb') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',')
		pool = Pool(10)
		for result in pool.map(getUrls, reader):
			for res in result:
				try:
					writer.writerow({'attraction_url':res[0], 'region':res[1]})
					print res[0], res[1]
				except: 
					print 'Error'
					print

	file.close()