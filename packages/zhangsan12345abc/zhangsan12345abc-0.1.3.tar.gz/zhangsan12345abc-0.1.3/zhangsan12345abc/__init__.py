import json

class birds():
	DEFAULT_LEGS = 2
	DEFAULT_WINGS = 2
	DEFAULT_HEAD = 1
	def __init__(self,legs = None,wings = None,head = None):
		self.legs = legs or self.__class__.DEFAULT_LEGS
		self.wings = wings or self.__class__.DEFAULT_WINGS
		self.head = head or self.__class__.DEFAULT_HEAD

	def __str__(self):
		strJsonStr = json.dumps(self.__dict__)
		return strJsonStr

