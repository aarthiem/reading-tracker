import requests
import json

# Sample book data
books = [
    {
        'title': 'The Midnight Library',
        'author': 'Matt Haig',
        'total_pages': 288,
        'status': 'To be read'
    },
    {
        'title': 'Atomic Habits',
        'author': 'James Clear',
        'total_pages': 320,
        'status': 'Reading'
    },
    {
        'title': 'The Alchemist',
        'author': 'Paulo Coelho',
        'total_pages': 163,
        'status': 'Read Done'
    }
]

print('Adding sample books to the database...')
for i, book in enumerate(books, 1):
    try:
        response = requests.post('http://localhost:5000/api/books', json=book)
        if response.status_code == 201:
            book_id = response.json()['id']
            print(f'SUCCESS Book {i}: "{book["title"]}" by {book["author"]} added successfully (ID: {book_id})')
        else:
            print(f'FAILED to add book {i}: {response.text}')
    except Exception as e:
        print(f'ERROR adding book {i}: {e}')

print('\nDone! You can now view these books in your reading tracker app.')