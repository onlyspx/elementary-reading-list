# Deployment Guide 🚀

## Quick Deploy to Vercel

### Option 1: Deploy via GitHub (Recommended)

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Elementary School Reading List"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Click "Deploy"
   - Done! ✅

### Option 2: Deploy via Vercel CLI

```bash
npm i -g vercel
vercel
```

## Environment Variables

No environment variables needed! This project works out of the box.

## Custom Domain (Optional)

1. Go to your project in Vercel
2. Settings → Domains
3. Add your custom domain
4. Update DNS records as instructed

## Build Settings

These are automatically configured, but for reference:

- **Framework Preset**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

## Vercel.json Configuration

Already included in the project for optimal deployment.

## Post-Deployment

After deployment, you'll get:
- 🌍 Production URL: `https://your-project.vercel.app`
- 📊 Analytics dashboard
- 🚀 Automatic deployments on git push
- 🔄 Preview deployments for pull requests

## Troubleshooting

**Build fails?**
- Check `npm run build` works locally first
- Ensure all dependencies are in `package.json`
- Check Vercel build logs for specific errors

**Images not loading?**
- Local images in `public/covers/` are automatically deployed
- External APIs (Open Library, Google Books) work from any domain

## Performance

Expected Lighthouse scores:
- ⚡️ Performance: 95+
- ♿️ Accessibility: 100
- 🎯 Best Practices: 95+
- 🔍 SEO: 100

---

Need help? Check [Vercel's Next.js deployment docs](https://vercel.com/docs/frameworks/nextjs)

