#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import time
import os

def try_openlibrary_search(title, author):
    """Search Open Library API for the book and get cover"""
    try:
        search_url = f"https://openlibrary.org/search.json?title={urllib.parse.quote(title)}&author={urllib.parse.quote(author)}"
        
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            
            if data.get('docs') and len(data['docs']) > 0:
                book = data['docs'][0]
                
                if 'cover_i' in book:
                    cover_id = book['cover_i']
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                    req = urllib.request.Request(cover_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=10) as cover_response:
                        cover_data = cover_response.read()
                        if len(cover_data) > 5000:
                            return cover_data
    except Exception as e:
        pass
    return None

def try_google_books(title, author):
    """Try Google Books API"""
    try:
        query = f"intitle:{title} inauthor:{author}".replace(' ', '+')
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1"
        
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            
            if data.get('items') and len(data['items']) > 0:
                book = data['items'][0]
                if 'volumeInfo' in book and 'imageLinks' in book['volumeInfo']:
                    image_url = book['volumeInfo']['imageLinks'].get('thumbnail', '')
                    if image_url:
                        image_url = image_url.replace('zoom=1', 'zoom=2')
                        image_url = image_url.replace('http:', 'https:')
                        
                        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=10) as img_response:
                            img_data = img_response.read()
                            if len(img_data) > 3000:
                                return img_data
    except Exception as e:
        pass
    return None

# Read books data
with open('src/data/books.json', 'r') as f:
    books = json.load(f)

# Get Mathical books without covers (but SKIP 233 - the bad one!)
mathical_books = [b for b in books if int(b['id']) >= 227 and int(b['id']) <= 265 
                  and 'coverImage' not in b and b['id'] != '233']

print(f"🔍 Re-downloading {len(mathical_books)} Mathical covers (SKIPPING #233)\n")

os.makedirs('public/covers', exist_ok=True)

success_count = 0

for book in mathical_books:
    title = book['title']
    author = book['author']
    book_id = book['id']
    
    print(f"📖 {title[:60]}")
    
    cover_data = None
    
    # Try Open Library search first
    print(f"   → Searching Open Library...")
    cover_data = try_openlibrary_search(title, author)
    if cover_data:
        print(f"   ✅ Found via Open Library!")
    
    # Try Google Books if needed
    if not cover_data:
        print(f"   → Trying Google Books...")
        cover_data = try_google_books(title, author)
        if cover_data:
            print(f"   ✅ Found via Google Books!")
    
    if cover_data:
        filename = f"mathical-{book_id}.jpg"
        filepath = f"public/covers/{filename}"
        with open(filepath, 'wb') as f:
            f.write(cover_data)
        book['coverImage'] = f"/covers/{filename}"
        success_count += 1
        print(f"   💾 Saved ({len(cover_data):,} bytes)\n")
    else:
        print(f"   ❌ No cover\n")
    
    time.sleep(0.8)

print(f"\n{'='*60}")
print(f"✅ Downloaded: {success_count} covers")
print(f"🚫 Skipped #233 (How Many Jelly Beans - bad cover)")
print(f"📚 Total Mathical with covers: {success_count + 6}")
print(f"{'='*60}")

# Save
with open('src/data/books.json', 'w') as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print("✅ Updated books.json")

