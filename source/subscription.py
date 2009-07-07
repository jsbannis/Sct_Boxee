#!/usr/bin/env python
# copyright 2009 Jared Bannister

# This file is part of ScT_Boxee.
# 
# ScT_Boxee is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ScT_Boxee is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

""" Manages subscriptions to shows
"""
__author__ = "jared"
__version__ = "1.0"

import tvdb_api
import time
import datetime
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
		self.lastDownload =datetime.datetime(year=1900,month=1,day=1) # some arbitrary date long aga
		
	def update(self):
		"""Updates the show object if it is out of date
		"""
		if time.time() < int(self.show['lastupdated']): # this makes no sense, if it was true, we wouldn't know about it
			t = tvdb_api.Tvdb()
			self.show = t[title]

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
		slist.write('subs')

if __name__ == '__main__':
	main()