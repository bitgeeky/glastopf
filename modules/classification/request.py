# Copyright (C) 2011  Lukas Rist
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re

from xml.dom.minidom import parse

class RequestPattern(object):
	def __init__(self, id, string, description, module):
		self.id = id
		self.string = string
		self.description = description
		self.module = module

class Classifier(object):
	def __init__(self):
		self.tree = parse("requests.xml")
	
	def get_patterns(self):
		patterns = self.tree.getElementsByTagName("request")
		return patterns
	
	def getText(self, nodelist):
		rc = []
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE or node.nodeType == node.CDATA_SECTION_NODE:
				rc.append(node.data)
				break
		return ''.join(rc)
	
	def parse_pattern(self, pattern):
		pattern_id = self.getText(pattern.getElementsByTagName("id")[0].childNodes)
		pattern_string = self.getText(pattern.getElementsByTagName("patternString")[0].childNodes) 
		pattern_description = pattern.getElementsByTagName("patternDescription")[0].childNodes[0].data
		pattern_module = pattern.getElementsByTagName("module")[0].childNodes[0].data
		parsed_pattern = RequestPattern(pattern_id, pattern_string, pattern_description, pattern_module)
		return parsed_pattern
	
	def select_pattern(self, matched_patterns):
		# TODO: add some logic
		matched_pattern = matched_patterns[0]
		if len(matched_patterns) > 1:
			if matched_patterns[0] == "unknown":
				matched_pattern = matched_patterns[1]
		else:
			matched_pattern = matched_patterns[0]
		return matched_pattern
		
	def classify_request(self, parsed_request):
		patterns = self.get_patterns()
		matched_patterns = []
		for pattern in patterns:
			parsed_pattern = self.parse_pattern(pattern)
			re_pattern = re.compile(parsed_pattern.string)
			match = re_pattern.search(parsed_request.url)
			if match != None:
				matched_patterns.append(parsed_pattern.module)
		matched_pattern = self.select_pattern(matched_patterns)
		return matched_pattern