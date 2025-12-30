#!/usr/bin/env python3
import json

# Unique descriptions for the remaining 6 duplicates
FIXES = {
    "61": "Splat the Cat is nervous about his first day of school! Will he make friends? Will he like his teacher? Join Splat on his hilarious school adventure filled with mishaps and surprises.",
    
    "104": "The Bad Seed has a bad attitude, bad manners, and a bad temper. But was he always bad? A surprisingly touching story about how it's never too late to change your ways.",
    
    "168": "When a crocodile accidentally swallows a watermelon seed, he's convinced a watermelon will grow in his belly! His friends try to reassure him in this silly story about worrying.",
    
    "170": "Gerald the Elephant has an ice cream cone, but should he share it with Piggie? Mo Willems explores friendship and sharing with humor and heart in this easy reader.",
    
    "59": "A little chameleon is sad that he doesn't have his own color like goldfish, elephants, and parrots do. But being able to change colors turns out to be a special gift all its own!",
    
    "80": "Titch is the smallest in his family. His brother and sister have bigger things than him—until Titch plants a tiny seed that grows bigger than anything! A story about finding your own strengths.",
}

with open('src/data/books.json', 'r') as f:
    books = json.load(f)

fixed = 0
for book in books:
    if book['id'] in FIXES:
        book['description'] = FIXES[book['id']]
        print(f"✓ ID {book['id']:>3}: {book['title'][:50]}")
        fixed += 1

with open('src/data/books.json', 'w') as f:
    json.dump(books, f, indent=2, ensure_ascii=False)

print(f"\n✅ Fixed {fixed} remaining duplicate descriptions")

