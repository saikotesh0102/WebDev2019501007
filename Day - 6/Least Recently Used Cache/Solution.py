class LRUCache:
	def __init__(self, capacity):
		super().__init__()
		self.capacity = capacity
		self.input_data = {}
		self.listCache = []
	
	def get(self, key):
		'''
			return value of -1
		'''
		if key in self.input_data:
			self.listCache.remove(key)
			self.listCache.append(key)
			return self.input_data[key]
		else:
			return -1

	def get_cache(self):
		return self.listCache

	def put(self,key,value):
		if len(self.listCache) == self.capacity:
			if key in self.input_data:
				self.listCache.remove(key)
			else:
				x = self.listCache.pop(0)
				del self.input_data[x]
		self.listCache.append(key)
		self.input_data[key] = value

