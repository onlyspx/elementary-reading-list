# Elementary School Reading List 📚

A beautiful, responsive Next.js application showcasing curated collections of high-quality books for elementary school readers, featuring library-recommended titles with Lexile levels, descriptions, and direct links to purchase or borrow.

## 🌟 Live Demo

**[View Live Site →](https://your-site.vercel.app)**

## 📖 Currently Available

**First Grade (Ages 6-7) - 225 Books**

## ✨ Key Features

- 📊 **Lexile Level Display & Sorting** - Find books at the perfect reading level
- 📝 **Engaging Book Descriptions** - Know why each book is worth reading
- 🖼️ **Beautiful Book Covers** - Visual browsing experience
- 🔍 **Smart Search & Filters** - Find books by title, author, genre, or Lexile
- 🏛️ **Library Integration** - Direct links to Mountain View & Los Altos libraries
- 🛒 **Amazon Links** - Easy purchase options
- 📱 **Fully Responsive** - Perfect on mobile, tablet, and desktop

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:3000
```

## 📊 Data Quality

- ✅ **225 validated books** with accurate ISBNs
- ✅ **64 local cover images** for perfect quality
- ✅ **48 books with descriptions** explaining why to read them
- ✅ **100% validated** using included validation script
- ✅ **0 errors, 0 warnings**

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Deployment**: Vercel-ready

## 📚 Book Sources

- 🏛️ **Mountain View Public Library** first-grade list (30 books)
- 📋 **K-12 Reading List** teacher recommendations (34 books)
- Modern releases and timeless classics

## 🔧 Scripts

```bash
# Development
npm run dev

# Production build
npm run build
npm start

# Validate book data
node validate-books.js

# Linting
npm run lint
```

## 📁 Project Structure

```
books-list/
├── public/
│   └── covers/          # Local book cover images
├── src/
│   ├── app/
│   │   ├── layout.js    # Root layout
│   │   ├── page.js      # Main page with filters & sort
│   │   └── globals.css
│   ├── data/
│   │   └── books.json   # Book database (225 books)
│   └── utils/
│       └── linkHelpers.js
├── validate-books.js    # Data validation script
└── README.md
```

## 🌍 Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/elementary-reading-list)

1. Push to GitHub
2. Import project in Vercel
3. Deploy (zero configuration needed!)

## 🎯 Future Enhancements

- [ ] Add more grade levels (K, 2nd, 3rd)
- [ ] User favorites/bookmarks
- [ ] Print reading lists
- [ ] More library integrations
- [ ] Reading progress tracking

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ for Bay Area families and educators
