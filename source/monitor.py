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


""" Monitors ScT for new torrents of subscribed shows
"""
__author__ = "jared"
__version__ = "1.0"

from subscription import Subscription
from subscription import SubscriptionList
import feedparser
import os
import datetime

class Monitor:
	feed = None			# a feedparser object
	slist = None		# subscription list to monitor
	passkey	= 'error'	# ScT passkey
	url = 'https://www.scenetorrents.org/rss.php?passkey='
	
	def getPasskey(self):
		filename = 'passkey.txt'
		if os.path.exists(filename):
			f = open(filename,'r')
			key = f.readline()
			f.close()
			return key
		return 'error'
	
	def getSubscriptionList(self):
		filename = 'subs'
		slist = SubscriptionList()
		if os.path.exists(filename):
			slist = slist.read(filename)
		return slist
		
	def getFeed(self):
		url = self.url + passkey
		self.feed = feedparser.parse(url)

	def monitorSubscriptions(self):
		# Update subscriptions
		for s in self.slist.values():
			print 'Updating ' + s.title
			s.update()
			
		# Examine subscriptions; if last download is before last episode aired
		for s in self.slist.values():
			lastAir = self.getLastAirTime(s.show['airs_dayofweek'], s.show['airs_time'], s.show['runtime'])
			if s.lastDownload < lastAir:
				print 'yes'
				# Check for it on the rss
				
				# If it isn't in the rss and it is more than an hour (arbitrary) after air, do a search of ScT
		
				# If we have found a torrent; download it, add it to download queue, update subscription object
		
	def getLastAirTime(self, dayOfWeek, time, duration):
		# determine target day from a string like this "Monday"
		days = {'Monday':0,'Tuesday':1,'Wednesday':2,'Thursday':3,'Friday':4,'Saturday':5,'Sunday':6}
		targetDay = days[dayOfWeek]

		# roll date back to that day
		dt = datetime.datetime.now()
		while dt.weekday() != targetDay:
			dt = dt + datetime.timedelta(-1)

		# get target time from a string like "8:00 PM"
		s = time.partition(' ')
		s2 = s[0].partition(':')		
		if s[2] == 'AM':
		 	targetTime = int(s2[0])*60 + int(s2[2]) + int(duration)
		else:
			targetTime = int(s2[0])*60 + 12*60 + int(s2[2]) + int(duration)
		
		# replace the time with targetTime
		dt = dt.replace(hour=int(targetTime/60) ,minute=targetTime%60 , second=0)
		
		return dt