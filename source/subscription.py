#!/usr/bin/env python
#encoding:utf-8
#author:jared
#project:ScT_Boxee
#repository:
#license:

""" Manages subscriptions to shows
"""
__author__ = "jared"
__version__ = "1.0"

import tvdb_api
import time
import pickle

class Subscription:
	"""Represents a subscription to a certain show
	"""
	title = 'Show Title'	# Redundant from show object but easier access
	show = None				# This is a 'show' object from the tvdb_api
	lastDownload = None		# Date of the last show downloaded; used to see if we need to download
	active = True			# When a subscription is 'unsubscribed' it is simply deactivated
	
	def __init__(self, the_show):
		self.title = the_show['seriesname']
		self.show = the_show
		self.lastDowload = time.time()
		
	def update(self):
		"""Updates the show object if it is out of date
		"""
		if time.time() < int(show['lastupdated']):
			t = tvdb_api.Tvdb()
			show = t[title]

class SubscriptionList(dict):
	"""A dictionary of subscriptions with utilities to read and write to file
	"""
	def __init__(self):
		dict.__init__(self)
	
	def write(self, filename):
		f = open(filename, 'w')
		# for sub in self.values():
		# 			pickle.dump(sub, f)
		pickle.dump(self, f)
		f.close()
	
	def read(self, filename):
		f = open(filename, 'r')
		loaded = pickle.load(f)
		f.close()
		return loaded

def main():
	import os
	t = tvdb_api.Tvdb()
	slist = SubscriptionList()
	if os.path.exists('subs'):
		slist = slist.read('subs')
	
	while True:
		p = raw_input("Enter show name to subscribe: ")
		slist[p] = Subscription(t[p])
		print "Your subscriptions\n"
		for s in slist.values():
			print s.title + "\t\t" + s.show['network'] + "\t" + s.show['airs_dayofweek'] + " " + s.show['airs_time']
		print "\n"

if __name__ == '__main__':
	main()