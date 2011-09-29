﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyGtalkRobot: A simple jabber/xmpp bot framework using Regular Expression Pattern as command controller
# Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Homepage: http://code.google.com/p/pygtalkrobot/
#

import sys, traceback
import xmpp
import urllib
import re
import inspect

"""A simple jabber/xmpp bot framework

This is a simple jabber/xmpp bot framework using Regular Expression Pattern as command controller.
Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>

To use, subclass the "GtalkRobot" class and implement "command_NUM_" methods
(or whatever you set the command_prefix to), like sampleRobot.py.

"""

class GtalkRobot:

	def command(self, func):
		self.commands[func.__name__]=func

	conn = None
	show = "available"
	status = "PyGtalkRobot"
	commands = {}
	command_prefix = 'command_'
	########################################################################################################################
	
	#Pattern Tips:
	# I or IGNORECASE <=> (?i)	  case insensitive matching
	# L or LOCALE <=> (?L)		  make \w, \W, \b, \B dependent on the current locale
	# M or MULTILINE <=> (?m)	   matches every new line and not only start/end of the whole string
	# S or DOTALL <=> (?s)		  '.' matches ALL chars, including newline
	# U or UNICODE <=> (?u)		 Make \w, \W, \b, and \B dependent on the Unicode character properties database.
	# X or VERBOSE <=> (?x)		 Ignores whitespace outside character sets
	
	#This method is the default action for all pattern in lowest priviledge
	def command_999_default(self, user, message, args):
		""".*?(?s)(?m)"""
		self.replyMessage(user, message)

	########################################################################################################################
	#These following methods can be only used after bot has been successfully started

	#show : xa,away---away   dnd---busy   available--online
	def setState(self, show, status_text):
		if show:
			show = show.lower()
		if show == "online" or show == "on" or show == "available":
			show = "available"
		elif show == "busy" or show == "dnd":
			show = "dnd"
		elif show == "away" or show == "idle" or show == "off" or show == "out" or show == "xa":
			show = "xa"
		else:
			show = "available"
		
		self.show = show

		if status_text:
			self.status = status_text
		
		if self.conn:
			pres=xmpp.Presence(priority=5, show=self.show, status=self.status)
			self.conn.send(pres)

	def getState(self):
		return self.show, self.status

	def replyMessage(self, user, message):
		self.conn.send(xmpp.Message(user, message))

	def getRoster(self):
		return self.conn.getRoster()

	def getResources(self, jid):
		roster = self.getRoster()
		if roster:
			return roster.getResources(jid)

	def getShow(self, jid):
		roster = self.getRoster()
		if roster:
			return roster.getShow(jid)

	def getStatus(self, jid):
		roster = self.getRoster()
		if roster:
			return roster.getStatus(jid)

	def authorize(self, jid):
		""" Authorise JID 'jid'. Works only if these JID requested auth previously. """
		self.getRoster().Authorize(jid)
	
	########################################################################################################################

	def controller(self, conn, message):
		text = message.getBody()
		user = message.getFrom()
		if text:
			text = text.encode('utf-8', 'ignore')
			text_s=text.split(" ")
			text_f, text_s=text_s[0], " ".join(text_s[1:])
			try:
				self.commands[text_f](text_s)
			except KeyError:
				self.commands["default"](text)
				

	def presenceHandler(self, conn, presence):
		if presence:
			pass
		#	print "from",presence.getFrom()
		#	print "status",presence.getStatus()
		#	print "show",presence.getShow()

	def StepOn(self):
		try:
			self.conn.Process(1)
		except KeyboardInterrupt: 
			return 0
		return 1

	def GoOn(self):
		while self.StepOn(): pass

		########################################################################################################################
	# "debug" parameter specifies the debug IDs that will go into debug output.
	# You can either specifiy an "include" or "exclude" list. The latter is done via adding "always" pseudo-ID to the list.
	# Full list: ['nodebuilder', 'dispatcher', 'gen_auth', 'SASL_auth', 'bind', 'socket', 'CONNECTproxy', 'TLS', 'roster', 'browser', 'ibb'].
	def defaultCommand(self, message):
		pass
	def __init__(self, server_host="talk.google.com", server_port=5223, debug=[]):
		self.commands["default"] = self.defaultCommand
		self.debug = debug
		self.server_host = server_host
		self.server_port = server_port

	def start(self, gmail_account, password):
		jid=xmpp.JID(gmail_account)
		user, server, password = jid.getNode(), jid.getDomain(), password
		
		self.conn=xmpp.Client(server, debug=self.debug)
		#talk.google.com
		conres=self.conn.connect( server=(self.server_host, self.server_port) )
		if not conres:
			print "Unable to connect to server %s!"%server
			sys.exit(1)
		if conres!='tls' and conres!='ssl':
			print "Warning: unable to estabilish secure connection - TLS failed!"
		
		authres=self.conn.auth(user, password)
		if not authres:
			print "Unable to authorize on %s - Plsese check your name/password."%server
			sys.exit(1)
		if authres<>"sasl":
			print "Warning: unable to perform SASL auth os %s. Old authentication method used!"%server
		
		self.conn.RegisterHandler("message", self.controller)
		self.conn.RegisterHandler('presence',self.presenceHandler)
		
		self.conn.sendInitPresence()
		
		self.setState(self.show, self.status)
		
		#print "Bot started."
		self.GoOn()

	########################################################################################################################


############################################################################################################################
if __name__ == "__main__":
	bot = GtalkRobot()
	bot.setState('available', "PyGtalkRobot")
	bot.start("PyGtalkRobot@gmail.com", "PyGtalkRobotByLdmiao")
