#!/usr/bin/env node

/**
 * Data Validation Script for Books List
 * Run with: node validate-books.js
 */

const fs = require('fs');
const https = require('https');

const books = JSON.parse(fs.readFileSync('./src/data/books.json', 'utf8'));

console.log('📚 Books Data Validation Report');
console.log('='.repeat(60));
console.log(`Total books: ${books.length}\n`);

let errors = [];
let warnings = [];

// Validation checks
books.forEach((book, index) => {
  const bookRef = `Book #${book.id}: "${book.title}"`;
  
  // Required fields
  if (!book.id) errors.push(`${bookRef} - Missing ID`);
  if (!book.title) errors.push(`${bookRef} - Missing title`);
  if (!book.author) errors.push(`${bookRef} - Missing author`);
  if (!book.isbn) warnings.push(`${bookRef} - Missing ISBN (no cover will show)`);
  if (!book.lexile) warnings.push(`${bookRef} - Missing Lexile level`);
  if (!book.tags || book.tags.length === 0) warnings.push(`${bookRef} - No tags`);
  
  // ISBN format validation
  if (book.isbn && !book.isbn.match(/^97[89]\d{10}$/)) {
    warnings.push(`${bookRef} - Invalid ISBN format: ${book.isbn}`);
  }
  
  // Duplicate ID check
  const duplicateId = books.filter(b => b.id === book.id).length > 1;
  if (duplicateId) errors.push(`${bookRef} - Duplicate ID: ${book.id}`);
});

// Check for duplicate titles
const titleCounts = {};
books.forEach(book => {
  const key = book.title.toLowerCase().trim();
  titleCounts[key] = (titleCounts[key] || 0) + 1;
});
Object.keys(titleCounts).forEach(title => {
  if (titleCounts[title] > 1) {
    warnings.push(`Duplicate title found ${titleCounts[title]} times: "${title}"`);
  }
});

// Report results
console.log('✅ VALIDATION COMPLETE\n');

if (errors.length === 0) {
  console.log('✅ No critical errors found!');
} else {
  console.log(`❌ ERRORS (${errors.length}):`);
  errors.forEach(err => console.log(`  - ${err}`));
}

console.log('');

if (warnings.length === 0) {
  console.log('✅ No warnings!');
} else {
  console.log(`⚠️  WARNINGS (${warnings.length}):`);
  warnings.slice(0, 20).forEach(warn => console.log(`  - ${warn}`));
  if (warnings.length > 20) {
    console.log(`  ... and ${warnings.length - 20} more warnings`);
  }
}

console.log('\n' + '='.repeat(60));

// Tag statistics
const tagStats = {};
books.forEach(book => {
  book.tags.forEach(tag => {
    tagStats[tag] = (tagStats[tag] || 0) + 1;
  });
});

console.log('\n📊 TAG STATISTICS:');
Object.entries(tagStats)
  .sort((a, b) => b[1] - a[1])
  .forEach(([tag, count]) => {
    console.log(`  ${tag}: ${count} books`);
  });

// Exit with error code if there are errors
process.exit(errors.length > 0 ? 1 : 0);

