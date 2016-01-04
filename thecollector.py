"""
The Collector

Copyright (C) 2015,  Matthew Plummer-Fernandez
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
<http://www.gnu.org/licenses/>

"""

print """

THE COLLECTOR
(A bot that searches and collects things from Thingiverse)
by Matthew Plummer-Fernandez, 2015

^_^ Available on Github:

"""

import time, random, ConfigParser
from selenium import webdriver
from random_words import RandomWords
from bs4 import BeautifulSoup
import urllib, os
from os import listdir
from os.path import isfile, join
import requests

#Provides a random search word
def randWord():
	rw = RandomWords()
	word = rw.random_word()
	return word

# Finds the log-in page in Thingiverse
def getSigninLink(page):
	links = []
	url = ''
	for link in page.find_all('a'):
		role = link.get('class')
		#print role
		if role:
			if role[0] == "login-options":
				url = link.get('href')
				fullurl = "https:" + str(url)
				print fullurl
	return fullurl

#Finds links to Things in Thingiverse
def getThingLinks(page):
	links = []
	for link in page.find_all('a'):
		url = link.get('href')
		if url:
			if '/thing:' in url:
				if '/#comments' in url:
					notinterested = 1
				else:
					if 'edit' in url:
						notinterested = 1
					else:
						fullurl = "http://www.thingiverse.com" + url + "/#files"
						links.append(fullurl)
						print fullurl

	return links

# Finds the url for main image of the Thing
def getImage(page):
	imgdivs = page.findAll("div", {"class":"thing-page-image featured"})
	for imgdiv in imgdivs:
		#print imgdiv
		for img in imgdiv.find_all('img'):
			#print img
			url = img.get('src')
			if url is None:
				ignore = 1
				return "None"
			else:
				print "URL = " + str(url)
				return url

# Finds URLs of all the Things that the search term retrieved
def getSTLs(page):
	urls = []
	thingdivs = page.findAll("div", {"class":"thing-file"})
	for thingdiv in thingdivs:
		for link in thingdiv.find_all('a'):
			#print link
			url = link.get('href')
			fullurl = "http://www.thingiverse.com" + url
			print fullurl
			filename = link.get('data-file-name')
			urls.append([fullurl, filename])
	return urls

# Downloading large files using Requests
# Code adapted from http://stackoverflow.com/a/16696317/3049530
def download_STL(url, folder):
	r = requests.get(url[0], stream=True)
	with open(folder + "/" + url[1], 'w') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)

def getLicense(page):
	licensediv = page.find("div", {"class":"thing-license"})
	return licensediv.get('title')

def getObjectInfo(page):
	thingpage = page.find("div", {"id": "thing-page"})
	object_id = thingpage.get('data-thing-id')

	thingheader = thingpage.find("div", {"class":"thing-header-data"})
	object_title = thingheader.h1.string
	author = thingheader.h2.a.string
	time = thingheader.h2.time['datetime']
	license = getLicense(page)
	
	print object_id, object_title, author, time, license

# Moves files from temp directory to Thing's exclusive directory
def move(src,dst):
	os.system ("mv" + " " + src + "/* " + dst)

# Selenium/ B4S powered search bot on loop
def BrowseBot(browser):
	visited = {}
	pList = []
	count = 0
	word = ""
	while True:
		#sleep to make sure page loads, add random to make it act human.
		time.sleep(random.uniform(1,2))

		if pList: #if there are Things, browse them, if not skip to 'else' routine
			searchPage = pList.pop()
			try:
				browser.get(searchPage)
			except:
				print "[-] could not get page"
			count += 1

			# give time for page to load
			time.sleep(random.uniform(1.5,2))

			#Make a directory for this Thing
			dirname = word + "_" + searchPage[-11:]
			dirname = dirname[:-8]
			print "directory name is = " + str(dirname)
			dirlocation = os.getcwd()+"/downloads/"+dirname
			os.mkdir(dirlocation)
			print "[+] directory made for this thing"

			# get Image of Thing
			print "getting image"
			page = BeautifulSoup(browser.page_source)
			imgurl = getImage(page)
			if imgurl != "None":
				try:
					urllib.urlretrieve(imgurl, dirlocation + "/" + str(word)+ "__" + str(os.path.basename(imgurl)))
					time.sleep(2)
					print "[+] image downloaded"
				except:
					print "[-] failed to download image"
			else:
				print "No image found"

			#get Things
			stlurls = getSTLs(page)

			for url in stlurls:
				#get STLs only, in future will add other file formats
				if url[1][-3:] == "stl":
					# browser.get(url[0]) #They are heading to the temp folder
					download_STL(url, dirlocation)
					print "[+] downloaded file"
			 		#time.sleep(7) #time to download
			 	else:
			 		print "ignoring file = " + str(url[1])

			print "[+] ALL FILES downloaded"
			# Move all the downloaded STLs into the new directory
			# tempdir =  os.getcwd()+"/downloads/temp"
			# move(tempdir,dirlocation+"/")
			getObjectInfo(page)

		else: #otherwise find pages via a new random search
			print "[+] doing new product search"
			word = randWord()
			# Do new search
			print "------------------------------------"
			print "------- SEARCHING FOR THINGS -------"
			print "------------------------------------"
			print "The search term is = " + str(word)
			print "------------------------------------"

			browser.get("http://www.thingiverse.com/search?q="+word)
			time.sleep(random.uniform(0.5,1.4))

			# Beautiful soup helps find urls
			page = BeautifulSoup(browser.page_source)
			searchLinks = getThingLinks(page)
			if searchLinks:
				for searchPage in searchLinks:
						pList.append(searchPage)

				random.shuffle(pList)
				pList = list(set(pList))[:9]  # NUMBER FOR HOW MANY ITEMS TO RETRIEVE



def Main():
	# You need to put your Thingiverse email and password into the settings.cfg file
	config = ConfigParser.ConfigParser()
	try:
		config.read('settings.cfg')
		print "[+] Read settings"
	except:
		print "[-] Could not read settings"

	configEmail = config.get('thingiverse','email')
	configPass = config.get('thingiverse','psswrd')

	## Initiate browser with preferences to download without asking, otherwise human intervention is required
	profile = webdriver.FirefoxProfile()
	profile.set_preference('browser.download.folderList', 2)
	profile.set_preference('browser.download.manager.showWhenStarting', False)
	# profile.set_preference('browser.download.dir', os.getcwd()+"/downloads/temp/") #Make a "/downloads/temp/" folder where you keep your bot
	profile.set_preference("browser.helperApps.alwaysAsk.force", False);
	profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/sla,application/vnd.ms-pki.stl,application/x-navistyle,model/vrml'))
	# Add MIME types in line above for other 3D file formats http://www.sitepoint.com/web-foundations/mime-types-complete-list/

	browser = webdriver.Firefox(profile)
	browser.set_window_size(980,1820)
	browser.set_window_position(650,10)
	aurl = 'http://www.thingiverse.com'
	browser.get(aurl)
	page = BeautifulSoup(browser.page_source)
	signinUrl = getSigninLink(page)
	time.sleep(random.uniform(0.5,1.4))
	browser.get(signinUrl)

	emailElement = browser.find_element_by_id("username")
	configEmail2 = list(configEmail)
	for i in configEmail2:
		emailElement.send_keys(i)
		time.sleep(0.05)

	time.sleep(0.05)
	passElement = browser.find_element_by_id("password")
	configEmail2 = list(configPass)
	for i in configEmail2:
		passElement.send_keys(i)
		time.sleep(0.05)
	time.sleep(random.uniform(0.05,0.1))
	passElement.submit()
	btnElement = browser.find_element_by_id("sso_sign_in")
	btnElement.click()
	print "*click!*"
	print "[+] Logged in to Thingiverse. Commencing automated browsin'"

	#Initiate search/download bot
	BrowseBot(browser)
	# Close browser when done
	browser.close()

if __name__ == '__main__':
	Main()
