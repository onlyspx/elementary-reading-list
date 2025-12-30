'use client';

import { useState, useMemo } from 'react';
import { ShoppingCart, Book, Building, Search } from 'lucide-react';
import booksData from '../data/books.json';
import { 
  getAmazonLink, 
  getMountainViewLibraryLink, 
  getLosAltosLibraryLink 
} from '../utils/linkHelpers';

// Helper function to get Lexile level explanation
const getLexileExplanation = (lexile) => {
  if (!lexile) return null;
  
  const level = lexile.replace(/[^0-9]/g, ''); // Extract number
  const numLevel = parseInt(level) || 0;
  
  // Check prefixes
  if (lexile.startsWith('BR')) {
    return {
      title: 'Beginning Reader (BR)',
      description: 'Pre-level books with very simple text. Perfect for kids just starting to read.',
      readingLevel: 'Pre-K to Early Grade 1'
    };
  }
  
  if (lexile.startsWith('AD')) {
    return {
      title: `Adult Directed (AD) - ${level}L`,
      description: 'Picture book meant to be read aloud by an adult. Rich vocabulary and concepts for shared reading.',
      readingLevel: numLevel < 400 ? 'Read-aloud for PreK-Grade 1' : 'Read-aloud for Grade 1-3'
    };
  }
  
  if (lexile.startsWith('GN')) {
    return {
      title: `Graphic Novel (GN) - ${level}L`,
      description: 'Comic book format with pictures and text bubbles. Great for visual learners!',
      readingLevel: numLevel < 400 ? 'Grade 1-2' : 'Grade 2-3'
    };
  }
  
  // Regular Lexile levels
  if (numLevel < 200) {
    return {
      title: `${lexile} Level`,
      description: 'Early reader text. Simple sentences and common words.',
      readingLevel: 'Kindergarten to Early Grade 1'
    };
  } else if (numLevel < 400) {
    return {
      title: `${lexile} Level`,
      description: 'Grade 1 independent reading. Growing vocabulary and sentence complexity.',
      readingLevel: 'Grade 1'
    };
  } else if (numLevel < 600) {
    return {
      title: `${lexile} Level`,
      description: 'Grade 2-3 reading level. More complex stories and vocabulary.',
      readingLevel: 'Grade 2-3 (Advanced for Grade 1)'
    };
  } else {
    return {
      title: `${lexile} Level`,
      description: 'Advanced chapter book. Rich vocabulary and longer narratives.',
      readingLevel: 'Grade 3-4 (Very Advanced for Grade 1)'
    };
  }
};

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [sortBy, setSortBy] = useState('none'); // 'none' or 'lexile'
  const [filtersExpanded, setFiltersExpanded] = useState(true);

  // Get all unique tags for filter buttons
  const allTags = useMemo(() => {
    const tags = new Set();
    booksData.forEach(book => {
      book.tags.forEach(tag => tags.add(tag));
    });
    return Array.from(tags).sort();
  }, []);

  // Popular filters to show as buttons
  const quickFilters = [
    { id: 'all', label: 'All Books', icon: '📚' },
    { id: 'MV Library', label: 'MV Library List', icon: '🏛️', highlight: true },
    { id: 'K-12 Reading List', label: 'K-12 Reading List', icon: '📋', highlight: true },
    { id: 'Mathical', label: 'Mathical Award', icon: '🏆', highlight: true },
    { id: 'Graphic Novel', label: 'Graphic Novels', icon: '💬' },
    { id: 'Modern', label: 'Modern', icon: '✨' },
    { id: 'Chapter Book', label: 'Chapter Books', icon: '📖' },
    { id: 'Funny', label: 'Funny', icon: '😂' },
    { id: 'Classic', label: 'Classics', icon: '🌟' },
    { id: 'Diverse', label: 'Diverse', icon: '🌍' },
    { id: 'STEM', label: 'STEM', icon: '🔬' },
    { id: 'Beginner', label: 'Beginner', icon: '🌱' },
  ];

  // Filter books based on search query and selected filter
  const filteredBooks = useMemo(() => {
    let books = booksData;

    // Apply tag filter
    if (selectedFilter !== 'all') {
      books = books.filter(book => book.tags.includes(selectedFilter));
    }

    // Apply search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      books = books.filter(book => {
        const titleMatch = book.title.toLowerCase().includes(query);
        const authorMatch = book.author.toLowerCase().includes(query);
        const tagMatch = book.tags.some(tag => tag.toLowerCase().includes(query));
        const lexileMatch = book.lexile && book.lexile.toLowerCase().includes(query);
        return titleMatch || authorMatch || tagMatch || lexileMatch;
      });
    }

    // Apply sorting
    if (sortBy === 'lexile') {
      books = [...books].sort((a, b) => {
        const lexileA = a.lexile || '';
        const lexileB = b.lexile || '';
        
        // Helper to extract numeric value from Lexile
        const getLexileValue = (lexile) => {
          if (lexile === 'BR') return -1; // Beginning Reader comes first
          if (lexile === 'NP') return 9999; // Non-Prose at end
          const match = lexile.match(/\d+/);
          return match ? parseInt(match[0]) : 9999;
        };
        
        return getLexileValue(lexileA) - getLexileValue(lexileB);
      });
    }

    return books;
  }, [searchQuery, selectedFilter, sortBy]);

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterClick = (filterId) => {
    setSelectedFilter(filterId);
    setSearchQuery(''); // Clear search when using quick filters
  };

  return (
    <div className="min-h-screen pb-12">
      {/* Header - Compact on Mobile */}
      <header className="bg-white/95 backdrop-blur-sm shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <h1 className="text-2xl sm:text-4xl font-bold text-center bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent mb-1 sm:mb-2">
            📚 Elementary School Reading List
          </h1>
          <p className="text-center text-xs sm:text-sm text-purple-600 font-semibold mb-2 sm:mb-3">
            Currently featuring: First Grade (Ages 6-7)
          </p>
          
          {/* Search Bar - Always Visible */}
          <div className="relative max-w-2xl mx-auto mb-3">
            <div className="absolute inset-y-0 left-0 pl-3 sm:pl-4 flex items-center pointer-events-none">
              <Search className="h-4 w-4 sm:h-5 sm:w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search by title, author, or tag..."
              value={searchQuery}
              onChange={handleSearch}
              className="w-full pl-10 sm:pl-12 pr-4 py-2 sm:py-3 border-2 border-purple-200 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent text-sm sm:text-lg shadow-sm"
            />
          </div>
          
          {/* Filters Toggle Button - Mobile Only */}
          <div className="sm:hidden mb-2">
            <button
              onClick={() => setFiltersExpanded(!filtersExpanded)}
              className="w-full flex items-center justify-between bg-purple-50 hover:bg-purple-100 text-purple-700 font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              <span className="text-sm">
                {selectedFilter !== 'all' ? `Filter: ${quickFilters.find(f => f.id === selectedFilter)?.label}` : 'Filters & Sort'}
              </span>
              <span className="text-lg">{filtersExpanded ? '▲' : '▼'}</span>
            </button>
          </div>

          {/* Expandable Filters Section */}
          <div className={`${filtersExpanded ? 'block' : 'hidden'} sm:block`}>
            {/* Results count and Sort */}
            <div className="flex justify-between items-center mb-3 flex-wrap gap-2">
              <p className="text-xs sm:text-sm text-gray-500">
                {selectedFilter !== 'all' || searchQuery ? (
                  <>Showing {filteredBooks.length} {filteredBooks.length === 1 ? 'book' : 'books'}</>
                ) : (
                  <>{filteredBooks.length} books in collection</>
                )}
              </p>
              
              {/* Sort by Lexile */}
              <div className="flex items-center gap-2">
                <label className="text-xs sm:text-sm text-gray-600 font-medium">Sort:</label>
                <button
                  onClick={() => setSortBy(sortBy === 'lexile' ? 'none' : 'lexile')}
                  className={`px-2 sm:px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                    sortBy === 'lexile'
                      ? 'bg-green-500 text-white shadow-md'
                      : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {sortBy === 'lexile' ? '✓ ' : ''}📊 By Lexile
                </button>
              </div>
            </div>

            {/* Quick Filter Buttons - Scrollable on Mobile */}
            <div className="mt-3 sm:mt-5 flex flex-nowrap sm:flex-wrap overflow-x-auto sm:overflow-x-visible sm:justify-center gap-2 pb-2 sm:pb-0 -mx-4 px-4 sm:mx-0 sm:px-0">
              {quickFilters.map((filter) => (
                <button
                  key={filter.id}
                  onClick={() => handleFilterClick(filter.id)}
                  className={`px-3 sm:px-4 py-2 rounded-full text-xs sm:text-sm font-semibold transition-all duration-200 transform hover:scale-105 whitespace-nowrap flex-shrink-0 ${
                    selectedFilter === filter.id
                      ? filter.highlight
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-md ring-2 ring-blue-300'
                        : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-md'
                      : filter.highlight
                      ? 'bg-blue-50 text-blue-700 hover:bg-blue-100 shadow-sm border-2 border-blue-300 font-bold'
                      : 'bg-white text-gray-700 hover:bg-gray-50 shadow-sm border border-gray-200'
                  }`}
                >
                  <span className="mr-1">{filter.icon}</span>
                  {filter.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Books Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBooks.map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>

        {/* No Results */}
        {filteredBooks.length === 0 && (
          <div className="text-center py-20">
            <p className="text-2xl text-gray-400 mb-2">📖</p>
            <p className="text-xl text-gray-600">No books found</p>
            <p className="text-sm text-gray-500 mt-2">Try a different search term or filter</p>
          </div>
        )}
      </main>
    </div>
  );
}

function BookCard({ book }) {
  const [showTooltip, setShowTooltip] = useState(false);
  const [coverError, setCoverError] = useState(false);
  
  // Multiple cover sources for better reliability
  const getCoverUrl = () => {
    // Priority 1: Local cover image (for MV Library books)
    if (book.coverImage) {
      return book.coverImage;
    }
    
    // Priority 2: External APIs for other books
    if (!book.isbn) return null;
    
    if (!coverError) {
      // Primary: Open Library
      return `https://covers.openlibrary.org/b/isbn/${book.isbn}-M.jpg`;
    } else {
      // Fallback: Google Books
      return `https://books.google.com/books/content?id=&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api&isbn=${book.isbn}`;
    }
  };

  const coverUrl = getCoverUrl();
  const lexileInfo = getLexileExplanation(book.lexile);

  return (
    <div className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 flex flex-col h-full overflow-hidden">
      {/* Book Cover Image */}
      <div className="relative h-48 bg-gradient-to-br from-purple-100 to-pink-100 flex items-center justify-center overflow-hidden">
        {coverUrl ? (
          <img 
            src={coverUrl}
            alt={`Cover of ${book.title}`}
            className="h-full w-auto object-contain"
            onError={(e) => {
              // Don't retry if it's a local image
              if (book.coverImage) {
                e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="120" height="180" viewBox="0 0 120 180"%3E%3Crect fill="%23e2e8f0" width="120" height="180"/%3E%3Ctext x="50%25" y="40%25" font-family="Arial" font-size="40" fill="%239ca3af" text-anchor="middle" dominant-baseline="middle"%3E📚%3C/text%3E%3Ctext x="50%25" y="65%25" font-family="Arial" font-size="10" fill="%236b7280" text-anchor="middle" dominant-baseline="middle" style="word-wrap: break-word"%3E' + encodeURIComponent(book.title.substring(0, 30)) + '%3C/text%3E%3C/svg%3E';
                return;
              }
              
              // Try fallback source for external images
              if (!coverError && book.isbn) {
                setCoverError(true);
                e.target.src = `https://books.google.com/books/content?id=&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api&isbn=${book.isbn}`;
              } else {
                // Final fallback: SVG placeholder
                e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="120" height="180" viewBox="0 0 120 180"%3E%3Crect fill="%23e2e8f0" width="120" height="180"/%3E%3Ctext x="50%25" y="40%25" font-family="Arial" font-size="40" fill="%239ca3af" text-anchor="middle" dominant-baseline="middle"%3E📚%3C/text%3E%3Ctext x="50%25" y="65%25" font-family="Arial" font-size="10" fill="%236b7280" text-anchor="middle" dominant-baseline="middle" style="word-wrap: break-word"%3E' + encodeURIComponent(book.title.substring(0, 30)) + '%3C/text%3E%3C/svg%3E';
              }
            }}
          />
        ) : (
          <div className="text-center p-4">
            <div className="text-4xl mb-2">📚</div>
            <div className="text-xs text-gray-600 font-semibold">{book.title}</div>
          </div>
        )}
      </div>

      {/* Card Content */}
      <div className="p-5 flex-1 flex flex-col">
        {/* Title with Lexile Level */}
        <div className="mb-3">
          <h2 className="text-lg font-bold text-gray-800 mb-1 line-clamp-2">
            {book.title}
          </h2>
          {/* Lexile Level Badge with Tooltip - PROMINENT */}
          {book.lexile && lexileInfo && (
            <div className="inline-block relative">
              <span 
                className="bg-gradient-to-r from-green-500 to-emerald-600 text-white text-sm font-bold px-3 py-1 rounded-full shadow-sm cursor-help inline-flex items-center gap-1"
                onMouseEnter={() => setShowTooltip(true)}
                onMouseLeave={() => setShowTooltip(false)}
                onClick={() => setShowTooltip(!showTooltip)}
              >
                📊 {book.lexile}
              </span>
              
              {/* Tooltip */}
              {showTooltip && (
                <div className="absolute z-50 bottom-full left-0 mb-2 w-64 bg-gray-900 text-white text-xs rounded-lg shadow-xl p-3 pointer-events-none">
                  <div className="font-bold text-sm mb-1 text-green-300">{lexileInfo.title}</div>
                  <div className="mb-2">{lexileInfo.description}</div>
                  <div className="text-gray-300 italic">
                    📚 {lexileInfo.readingLevel}
                  </div>
                  {/* Arrow */}
                  <div className="absolute top-full left-4 -mt-1">
                    <div className="border-4 border-transparent border-t-gray-900"></div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
        
        {/* Author */}
        <p className="text-gray-600 text-sm mb-3">
          <span className="font-medium">by {book.author}</span>
        </p>
        
        {/* Description (if available) */}
        {book.description && (
          <p className="text-gray-600 text-xs mb-3 line-clamp-3 italic">
            "{book.description}"
          </p>
        )}
        
        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-3">
          {book.tags.map((tag, index) => (
            <span
              key={index}
              className="inline-block bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 text-xs font-semibold px-2.5 py-1 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>

        <div className="flex-1"></div>

        {/* Action Buttons - Smaller & Polished */}
        <div className="flex gap-2 mt-3">
          {/* Amazon Link */}
          <a
            href={getAmazonLink(book)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 flex-1 justify-center bg-orange-500 hover:bg-orange-600 text-white rounded-lg py-2 px-3 transition-all duration-200 text-xs font-medium shadow-sm hover:shadow"
            title="Search on Amazon"
          >
            <ShoppingCart className="h-3.5 w-3.5" />
            <span>Amazon</span>
          </a>

          {/* Mountain View Library Link */}
          <a
            href={getMountainViewLibraryLink(book)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 flex-1 justify-center bg-blue-500 hover:bg-blue-600 text-white rounded-lg py-2 px-3 transition-all duration-200 text-xs font-medium shadow-sm hover:shadow"
            title="Search at Mountain View Library"
          >
            <Book className="h-3.5 w-3.5" />
            <span>Mountain View</span>
          </a>

          {/* Los Altos Library Link */}
          <a
            href={getLosAltosLibraryLink(book)}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 flex-1 justify-center bg-green-500 hover:bg-green-600 text-white rounded-lg py-2 px-3 transition-all duration-200 text-xs font-medium shadow-sm hover:shadow"
            title="Search at Los Altos Library"
          >
            <Building className="h-3.5 w-3.5" />
            <span>Los Altos</span>
          </a>
        </div>
      </div>
    </div>
  );
}

