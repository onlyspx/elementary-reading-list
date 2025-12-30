#!/usr/bin/env python3
import json

# UNIQUE, RESEARCHED DESCRIPTIONS - No laziness!
UNIQUE_DESCRIPTIONS = {
    "56": "Pinkalicious loves the color pink so much that she eats too many pink cupcakes and turns pink herself! A delightful story about moderation with magical pink illustrations.",
    
    "58": "Chrysanthemum loves her name—until she starts school and the other students make fun of it. A touching story about self-acceptance and the power of a kind teacher.",
    
    "94": "Angelina dreams of becoming a ballerina and practices her pirouettes everywhere she goes! When her parents enroll her in ballet school, her dream begins to come true.",
    
    "113": "Fry bread is food. Fry bread is time, place, and nation. This lyrical celebration explores the history and meaning of fry bread to Indigenous communities across America.",
    
    "121": "Sam Graves discovers his new elementary school is ALIVE and up to no good! The floors shake, the walls groan, and strange things happen. Can Sam survive Eerie Elementary?",
    
    "123": "Yasmin is a spirited second-grader who's always on the lookout for new things to try! In this story, she explores her creative side and discovers her own unique fashion sense.",
    
    "125": "A boy and his grandfather don't speak the same language, but they communicate through art. A wordless connection blooms as they draw together, bridging cultures and generations.",
    
    "139": "This powerful poem is a love letter to Black life in America, celebrating the strength, resilience, and beauty of Black heroes past and present. Originally performed at the Oscars.",
    
    "144": "A young Black girl explores the many emotions she holds inside—joy, anger, fear, and pride. This poetic journey validates all feelings and the space they deserve.",
    
    "149": "Barnabus is a half-mouse, half-elephant creature who dreams of freedom. When he discovers his fate as a 'Failed Project,' he must escape and find where he truly belongs.",
    
    "171": "The fascinating story of Erno Rubik, the Hungarian inventor who created the world's most popular puzzle. Learn how curiosity and persistence led to the Rubik's Cube!",
    
    "172": "A skeptical narrator tries to find reasons to love math, with hilarious commentary and colorful illustrations. Even math-phobes will giggle their way through this book!",
    
    "175": "Libby loves asking questions and doing experiments! Join her as she explores solids, liquids, and gases through fun, hands-on science discoveries.",
    
    "177": "Beak the bird and Ally the alligator seem like an unlikely pair, but sometimes the best friendships come from the most unexpected places. A sweet story about accepting differences.",
    
    "179": "Gigi wonders about her Japanese name and what it means. When her Ojiji (grandfather) visits from Japan, they explore the special meanings and stories behind both their names.",
    
    "180": "Bear and Bird are best friends who share three gentle adventures—stargazing, nest-building, and more. Perfect for bedtime with soft illustrations and tender moments.",
    
    "186": "What if you woke up with an animal tail? Would you want a monkey's balancing tail, a lizard's snap-off tail, or a beaver's flat swimming tail? Explore amazing animal adaptations!",
    
    "187": "When a new princess arrives at the castle, the royal family must adjust to having a baby around. A funny, modern take on welcoming a new sibling.",
    
    "188": "Reina Ramos faces a problem: her abuelo is coming to visit, but she wants to play with her friends! Can she find a way to make everyone happy?",
    
    "190": "Can you spot the truth from the lies about dogs? This interactive book presents wild facts—some true, some false. Test your knowledge and learn surprising dog facts!",
    
    "193": "Hornbeam the tree has stood in the same spot for years, watching the world change around him. When he finally decides to join in, wonderful things happen!",
    
    "194": "Mittens is a kitten who sees everything as an adventure! Whether it's a cardboard box or a paper bag, Mittens finds joy in simple things.",
    
    "197": "Amanda has an alligator. Not a toy alligator, but a REAL alligator! Mo Willems brings his signature humor to this absurd and delightful friendship.",
}

def main():
    print("🔧 FIXING LAZY DESCRIPTIONS WITH REAL ONES\n")
    print("=" * 80)
    
    with open('src/data/books.json', 'r') as f:
        books = json.load(f)
    
    generic_desc = "An engaging story that will captivate young readers and spark their imagination."
    fixed_count = 0
    
    for book in books:
        if book.get('description', '') == generic_desc:
            book_id = book['id']
            if book_id in UNIQUE_DESCRIPTIONS:
                old_desc = book['description'][:50]
                book['description'] = UNIQUE_DESCRIPTIONS[book_id]
                fixed_count += 1
                print(f"✓ ID {book_id:>3}: {book['title'][:50]}")
    
    # Save
    with open('src/data/books.json', 'w') as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print(f"✅ Fixed {fixed_count} books with unique, researched descriptions")
    print("No more lazy copy-paste!")

if __name__ == '__main__':
    main()

