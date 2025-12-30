#!/usr/bin/env python3
import json
import os

# Find all 15K files with same hash - they're Google placeholder images
bad_covers = []

# Check all mathical covers
for i in range(227, 266):
    filepath = f"public/covers/mathical-{i}.jpg"
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        # 15567 is the exact size of Google Books "no preview" placeholder
        if size == 15567:
            bad_covers.append(i)
            print(f"Found bad placeholder: mathical-{i}.jpg")
            os.remove(filepath)

print(f"\n🗑️  Deleted {len(bad_covers)} placeholder images")

# Remove from books.json
with open('src/data/books.json', 'r') as f:
    books = json.load(f)

for book in books:
    if int(book['id']) in bad_covers and 'coverImage' in book:
        print(f"Removing cover from: {book['title'][:50]}")
        del book['coverImage']

with open('src/data/books.json', 'w') as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print(f"\n✅ Cleaned up {len(bad_covers)} books")
print("These books will show placeholder cards")

