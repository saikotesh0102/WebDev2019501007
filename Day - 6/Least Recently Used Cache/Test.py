from Solution import LRUCache

def main():
	test = LRUCache(5)
	# print(lru.capacity)
	
	test.put(1,1)
	test.put(2,2)
	test.put(3,3)
	assert test.get_cache() == [1, 2, 3] 
	test.put(4,4)
	test.put(5,5)
	assert test.get_cache() == [1, 2, 3, 4, 5]
	assert test.get(6) == -1
	assert test.get(2) == 2
	assert test.get_cache() == [1, 3, 4, 5, 2]
	test.put(6,6)
	assert test.get_cache() == [3, 4, 5, 2, 6]
	print("put test cases passed successfully")

	assert test.get(3) == 3
	assert test.get_cache() == [4, 5, 2, 6, 3]
	assert test.get(1) == -1
	assert test.get(6) == 6
	assert test.get_cache() == [4, 5, 2, 3, 6]
	assert test.get(3) == 3
	assert test.get_cache() == [4, 5, 2, 6, 3]
	test.put(1, 1)
	assert test.get_cache() == [5, 2, 6, 3, 1]
	print("get test cases passed successfully")
        

if __name__ == "__main__" :
	main()