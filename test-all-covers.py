#!/usr/bin/env python3
import json
import os
from PIL import Image

# Read books
with open('src/data/books.json', 'r') as f:
    books = json.load(f)

# Get all Mathical books
mathical_books = [b for b in books if int(b['id']) >= 227 and int(b['id']) <= 265]

print(f"Testing {len(mathical_books)} Mathical book covers...\n")
print("="*70)

good = []
bad = []
missing = []

for book in mathical_books:
    book_id = book['id']
    title = book['title'][:50]
    cover_path = book.get('coverImage', '')
    
    if not cover_path:
        missing.append(f"#{book_id}: {title} - NO coverImage in JSON")
        continue
    
    # Check if file exists
    filepath = f"public{cover_path}"
    
    if not os.path.exists(filepath):
        bad.append(f"#{book_id}: {title} - FILE MISSING: {filepath}")
        continue
    
    # Check file size
    size = os.path.getsize(filepath)
    
    if size < 1000:
        bad.append(f"#{book_id}: {title} - TOO SMALL: {size} bytes")
        continue
    
    # Try to open as image
    try:
        img = Image.open(filepath)
        width, height = img.size
        
        # Check if it's a valid size (not 1x1 placeholder)
        if width < 50 or height < 50:
            bad.append(f"#{book_id}: {title} - TINY IMAGE: {width}x{height}")
        else:
            good.append(f"#{book_id}: {title} - ✅ OK ({width}x{height}, {size:,} bytes)")
            
    except Exception as e:
        bad.append(f"#{book_id}: {title} - CORRUPT: {str(e)}")

print("\n✅ GOOD COVERS:")
print("="*70)
for g in good:
    print(g)

if bad:
    print(f"\n❌ BAD COVERS ({len(bad)}):")
    print("="*70)
    for b in bad:
        print(b)

if missing:
    print(f"\n⚠️  MISSING ({len(missing)}):")
    print("="*70)
    for m in missing:
        print(m)

print(f"\n{'='*70}")
print(f"Summary: {len(good)} good, {len(bad)} bad, {len(missing)} missing")
print(f"{'='*70}")

