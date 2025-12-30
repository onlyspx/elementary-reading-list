import './globals.css';

export const metadata = {
  title: 'Elementary School Reading List - Books for Kids',
  description: 'A curated collection of amazing books for elementary school readers, featuring first grade recommendations from libraries and educators',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 min-h-screen">
        {children}
      </body>
    </html>
  );
}

