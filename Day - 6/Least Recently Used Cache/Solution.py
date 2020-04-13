class LRUCache:
	def __init__(self, capacity):
		super().__init__()
		self.capacity = capacity
		self.cache = deque()
		self.input_data = {}

	
	def get(self, key):
		'''
			return value of -1
		'''
	def set(self, key, value):
		self.input_data[key] = value
