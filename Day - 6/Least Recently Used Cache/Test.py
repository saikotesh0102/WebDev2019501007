from Solution import LRUCache

def main():
	test = LRUCache(3)
	test.put(1,"CT")
	test.put(2,"Python")
	test.put(3,"IDS")
	assert test.input_data == {1:"CT", 2:"Python",3:"IDS"}
	test.put(3, "Introduction to Data Science")
	assert test.input_data == {1:"CT", 2:"Python",3:"Introduction to Data Science"}
	test.put(4, "ADS")
	test.put(5, "Java")
	assert test.input_data == {3:"Introduction to Data Science", 4:"ADS", 5:"Java"}
	print("Assert Passed")

if __name__ == "__main__":
	main()