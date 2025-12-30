#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import time
import sys

def fetch_google_books_description(isbn=None, title=None, author=None):
    """Fetch description from Google Books API"""
    try:
        if isbn:
            query = f"isbn:{isbn}"
        else:
            query = f"{title} {author}".strip()
        
        url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote(query)}"
        
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            if 'items' in data and len(data['items']) > 0:
                volume_info = data['items'][0].get('volumeInfo', {})
                description = volume_info.get('description', '')
                
                # Clean up description
                if description:
                    # Remove HTML tags
                    description = description.replace('<p>', '').replace('</p>', '')
                    description = description.replace('<br>', ' ').replace('<br/>', ' ')
                    description = description.replace('<b>', '').replace('</b>', '')
                    description = description.replace('<i>', '').replace('</i>', '')
                    
                    # Truncate if too long
                    if len(description) > 300:
                        description = description[:297] + '...'
                    
                    return description
    except Exception as e:
        pass
    return None

def fetch_openlibrary_description(isbn=None, title=None, author=None):
    """Fetch description from Open Library API"""
    try:
        if isbn:
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        else:
            # Search by title
            search_url = f"https://openlibrary.org/search.json?title={urllib.parse.quote(title)}"
            if author:
                search_url += f"&author={urllib.parse.quote(author)}"
            
            with urllib.request.urlopen(search_url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get('docs'):
                    key = data['docs'][0].get('key', '')
                    url = f"https://openlibrary.org{key}.json"
                else:
                    return None
        
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            if isbn:
                key = f"ISBN:{isbn}"
                if key in data:
                    description = data[key].get('description', '')
                    if isinstance(description, dict):
                        description = description.get('value', '')
            else:
                description = data.get('description', '')
                if isinstance(description, dict):
                    description = description.get('value', '')
            
            if description and len(description) > 50:
                # Truncate if too long
                if len(description) > 300:
                    description = description[:297] + '...'
                return description
    except Exception as e:
        pass
    return None

# Manual descriptions for classic/popular books
MANUAL_DESCRIPTIONS = {
    "Amelia Bedelia": "Amelia Bedelia takes everything literally! When the Rogers family asks her to 'draw the drapes' or 'dress the chicken,' hilarious mix-ups happen. A beloved classic about a well-meaning housekeeper who always gets things wonderfully wrong.",
    
    "Nate the Great": "Nate the Great is a boy detective who solves neighborhood mysteries with logic, determination, and a little help from his dog Sludge. Pancakes optional but highly recommended!",
    
    "Henry and Mudge": "Henry loves his big dog Mudge, and Mudge loves Henry. Together they have wonderful adventures and face everyday challenges with friendship, humor, and lots of slobbery kisses.",
    
    "Goodnight Moon": "In a great green room, a little bunny says goodnight to everything around him. This gentle bedtime story has helped millions of children drift off to sleep for over 70 years.",
    
    "Click, Clack, Moo: Cows That Type": "Farmer Brown's cows discover a typewriter and start making demands! When they go on strike for electric blankets, it leads to hilarious barnyard negotiations.",
    
    "If You Give a Mouse a Cookie": "If you give a mouse a cookie, he's going to ask for a glass of milk. And then... one thing leads to another in this circular tale of cause and effect that kids love to predict!",
    
    "Corduroy": "A small teddy bear in a department store wants nothing more than a home and a friend. When Lisa discovers him, it's the beginning of a beautiful friendship.",
    
    "Harold and the Purple Crayon": "Armed with his purple crayon, Harold draws himself into wonderful adventures, creating entire worlds with his imagination. Where will his purple line take him tonight?",
    
    "Madeline": "In an old house in Paris covered with vines, lived twelve little girls in two straight lines. The smallest one was Madeline! A brave little girl with a spirit that can't be tamed.",
    
    "The Snowy Day": "Peter wakes up to discover fresh snow! He explores his neighborhood, making snow angels and saving a snowball in his pocket. A timeless story celebrating wonder and discovery.",
    
    "The Gruffalo": "A clever mouse invents a scary monster called the Gruffalo to scare off predators in the deep dark wood. But what happens when the Gruffalo turns out to be real?",
    
    "Go, Dog. Go!": "Dogs of all kinds doing all sorts of things! Going up, down, in, out, and all around. A simple, fun book perfect for beginning readers.",
    
    "Are You My Mother?": "A baby bird falls from his nest and searches everywhere for his mother. Is she a kitten? A hen? A dog? A snort? Kids love this funny tale of a determined little bird.",
    
    "Charlotte's Web": "Wilbur the pig and Charlotte the spider form an unlikely friendship. When Wilbur's life is in danger, Charlotte weaves words in her web to save him in this timeless tale of friendship and sacrifice.",
    
    "Winnie-the-Pooh": "Join Pooh Bear and his friends Piglet, Eeyore, Tigger, and Christopher Robin for gentle adventures in the Hundred Acre Wood. Honey optional!",
    
    "Stuart Little": "Stuart Little is a mouse born to a human family in New York City. Despite his small size, he has big adventures and an even bigger heart.",
    
    "Mr. Popper's Penguins": "When house painter Mr. Popper receives a penguin from Antarctica, it's just the beginning! Soon his family home is filled with a dozen performing penguins.",
    
    "Curious George": "George is a good little monkey, but he's always curious! His curiosity leads to mischief and adventure, but his friend the Man with the Yellow Hat is always there to help.",
    
    "The Giving Tree": "A young boy and a tree form a special bond that lasts a lifetime. As the boy grows, the tree gives generously in this moving tale about love and giving.",
    
    "The Little Engine That Could": "A little blue engine agrees to pull a heavy train over a steep mountain when bigger engines refuse. 'I think I can, I think I can' becomes a mantra of determination!",
    
    "Chicka Chicka Boom Boom": "A told B, and B told C, 'I'll meet you at the top of the coconut tree!' A rhythmic alphabet adventure where all the letters race to the top.",
    
    "The Polar Express": "On Christmas Eve, a magical train takes a boy to the North Pole to meet Santa. A journey about believing in the magic of Christmas.",
    
    "Where the Wild Things Are": "When Max gets sent to bed without supper, he sails away to where the wild things are and becomes king of all wild things! But he soon misses home.",
    
    "Green Eggs and Ham": "Would you eat green eggs and ham? Sam-I-Am persistently offers this unusual meal in every situation imaginable. A Dr. Seuss classic about trying new things!",
    
    "Brown Bear, Brown Bear, What Do You See?": "Children will delight in identifying the colors and animals in this beloved pattern book with Bill Martin Jr.'s rhythmic text and Eric Carle's vibrant collage illustrations.",
    
    "Press Here": "Press the yellow dot and turn the page... What happens next? A magical book that invites kids to interact with dots, colors, and movements in surprising ways.",
    
    "The Kissing Hand": "Chester Raccoon doesn't want to go to kindergarten. His mother shares a family secret called the Kissing Hand to comfort him. Perfect for first-day-of-school jitters!",
    
    "Because of Winn-Dixie": "Ten-year-old Opal adopts a stray dog and names him after the grocery store where she found him. Winn-Dixie helps her make friends in her new town.",
    
    "Rainbow Fish": "Rainbow Fish has beautiful, shimmering scales but no friends. He learns that sharing his most prized possessions can bring the greatest happiness.",
    
    "The Tale of Peter Rabbit": "Peter disobeys his mother and sneaks into Mr. McGregor's garden. A narrow escape and a tummy ache teach him a lesson in this classic tale.",
    
    "Make Way for Ducklings": "Mr. and Mrs. Mallard search for the perfect place to raise their ducklings in Boston. They find it on an island in the Public Garden.",
    
    "Flat Stanley": "After a bulletin board falls on Stanley Lambchop, he's only half an inch thick! Being flat has advantages though - like being mailed to California for vacation!",
    
    "The Hundred Dresses": "Wanda claims she has one hundred dresses at home, but she wears the same faded dress to school every day. A powerful story about bullying and standing up for others.",
}

def get_description(book):
    """Get description for a book from various sources"""
    title = book['title']
    author = book.get('author', '')
    isbn = book.get('isbn', '')
    
    # Check manual descriptions first
    if title in MANUAL_DESCRIPTIONS:
        return MANUAL_DESCRIPTIONS[title]
    
    # Try Google Books API
    description = fetch_google_books_description(isbn, title, author)
    if description:
        return description
    
    # Try Open Library
    description = fetch_openlibrary_description(isbn, title, author)
    if description:
        return description
    
    # Return a generic description based on tags
    tags = book.get('tags', [])
    if 'Funny' in tags:
        return f"A funny and entertaining story that will make young readers laugh out loud!"
    elif 'STEM' in tags or 'Science' in tags:
        return f"An engaging introduction to science and discovery for curious young minds."
    elif 'Biography' in tags:
        return f"The inspiring true story of {title.split(':')[0]}."
    elif 'Friendship' in tags:
        return f"A heartwarming tale about friendship, kindness, and being a good friend."
    elif 'Classic' in tags:
        return f"A beloved classic that has delighted generations of young readers."
    else:
        return f"An engaging story that will captivate young readers and spark their imagination."

def main():
    print("📚 ADDING DESCRIPTIONS TO BOOKS\n")
    print("=" * 80)
    
    # Load books
    with open('src/data/books.json', 'r') as f:
        books = json.load(f)
    
    # Find books without descriptions
    books_to_update = []
    for book in books:
        if 'description' not in book or not book['description'] or book['description'].strip() == '':
            books_to_update.append(book)
    
    print(f"Found {len(books_to_update)} books without descriptions\n")
    
    updated_count = 0
    failed_count = 0
    
    for i, book in enumerate(books_to_update, 1):
        title = book['title'][:60]
        print(f"[{i}/{len(books_to_update)}] {title}...", end=' ', flush=True)
        
        description = get_description(book)
        
        if description:
            book['description'] = description
            updated_count += 1
            print("✓")
        else:
            failed_count += 1
            print("✗")
        
        # Rate limiting - be nice to APIs
        if i % 10 == 0:
            time.sleep(1)
    
    # Save updated books
    with open('src/data/books.json', 'w') as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print(f"✅ Updated {updated_count} books with descriptions")
    if failed_count > 0:
        print(f"⚠️  {failed_count} books still need manual descriptions")
    print("\n🎉 Done! books.json has been updated.")

if __name__ == '__main__':
    main()

