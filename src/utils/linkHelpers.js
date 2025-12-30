/**
 * Generates an Amazon search link.
 * Uses ISBN if available for accuracy, otherwise falls back to Title + Author.
 */
export const getAmazonLink = (book) => {
  const query = book.isbn || `${book.title} ${book.author}`;
  return `https://www.amazon.com/s?k=${encodeURIComponent(query)}`;
};

/**
 * Generates a Mountain View Public Library link.
 * Platform: Mountain View Library Catalog
 */
export const getMountainViewLibraryLink = (book) => {
  const query = `${book.title} ${book.author}`;
  return `https://librarycatalog.mountainview.gov/search?query=${encodeURIComponent(query)}`;
};

/**
 * Generates a Los Altos Library (SCCLD) link.
 * Los Altos is part of Santa Clara County Library District.
 * Platform: Bibliocommons
 */
export const getLosAltosLibraryLink = (book) => {
  const query = `${book.title} ${book.author}`;
  return `https://sccl.bibliocommons.com/v2/search?query=${encodeURIComponent(query)}&searchType=smart`;
};