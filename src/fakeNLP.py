import json
import re

class FakeNLP():
	def getKeywordTime(self, words): 
		for word in words: 
			if word[0] == "@":
				return word
		return None

	def getKeywordDate(self, words): 
		regexp = re.compile(r"\d{2}")
		for word in words: 
			if regexp.search(word) and word[0] != "@":
				return word

		return None

	def getKeywordMonth(self, words): 
		with open("src/_months.json", "r") as f: 
			_MONTHS = json.loads(f.read()) 
		for word in words: 
			if word in _MONTHS: 
				return _MONTHS.get(word) 
		return None

	def getKeywordDay(self, words):
		_DAYS_OF_THE_WEEK = None 
		with open("src/_days_of_the_week.json", "r") as f: 
			_DAYS_OF_THE_WEEK = json.loads(f.read()) 
		for word in words: 
			if word in _DAYS_OF_THE_WEEK: 
				return _DAYS_OF_THE_WEEK.get(word) 
		return None 

	def getKeywordWeek(self, words): 
		week = ["this", "next"] 
		for word in words: 
			if word in week: 
				return word 

		return None 