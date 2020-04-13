import collections

class LRUCache:
	def __init__(self, capacity):
		super().__init__()
		self.capacity = capacity
		self.input_data = collections.OrderedDict()
	
	def get(self, key):
		'''
			return value of -1
		'''
		if key in self.input_data.keys():
			return self.input_data[key]

	def get_cache(self):
		return self.input_data

	def put(self,key,value):
		if key not in self.input_data.keys():
			if len(self.input_data) >= self.capacity:
				self.input_data.popitem(last = False)
		self.input_data[key] = value