import requests

# result = requests.get("https://www.goodreads.com/book/review_counts.json", params = {"key": "GeJUHhlmNf7PYbzeKEnsuw", "isbns": "9781632168146"})
result = requests.get("http://covers.openlibrary.org/b/isbn/9781632168146.jpg")
print(result)