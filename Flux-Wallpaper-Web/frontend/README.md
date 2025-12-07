# Flux Depth Generator - Frontend

This is the Next.js frontend for the Flux Depth Generator application.

## 🚀 Quick Deploy to Netlify

### One-Click Deploy
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)

### Manual Deployment

1. **Sign up for [Netlify](https://netlify.com)** (free tier available)

2. **Import your repository:**
   - Click "Add new site" → "Import an existing project"
   - Select your Git provider and repository

3. **Configure build settings:**
   ```
   Base directory: Flux-Wallpaper-Web/frontend
   Build command: npm run build
   Publish directory: .next
   ```

4. **Add environment variables:**
   ```
   NEXT_PUBLIC_API_URL = https://your-backend-url.onrender.com/api/v1
   NODE_VERSION = 20
   ```

5. **Deploy!** 🚀

📖 **[Full Deployment Guide](../../NETLIFY_DEPLOYMENT.md)** with step-by-step instructions

---

## 🛠️ Local Development

### Prerequisites
- Node.js 18+ 
- Running backend API (see main README)

### Setup

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local and set your backend URL
# For local development:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Run Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

---

## ⚙️ Environment Variables

Create a `.env.local` file in this directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Optional: Disable Next.js telemetry
# NEXT_TELEMETRY_DISABLED=1
```

**For production deployment**, update to your deployed backend URL:
```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1
```

---

## 🏗️ Build for Production

```bash
npm run build
npm start
```

The production build is optimized and ready for deployment.

---

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Authentication pages
│   ├── dashboard/         # Main application pages
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Landing page
├── components/            # React components
│   ├── 3d/               # Three.js components
│   ├── auth/             # Auth-related components
│   ├── depth/            # Depth generation UI
│   └── ui/               # shadcn/ui components
├── lib/                   # Utilities
│   ├── api.ts            # API client
│   └── utils.ts          # Helper functions
├── public/               # Static assets
├── .env.example          # Environment variables template
└── netlify.toml          # Netlify configuration
```

---

## 🚢 Deployment Options

### Netlify (Recommended for Frontend)
- ✅ Easy deployment with Git integration
- ✅ Automatic HTTPS and CDN
- ✅ Preview deployments for PRs
- 📖 [Netlify Deployment Guide](../../NETLIFY_DEPLOYMENT.md)

### Vercel
- ✅ Created by Next.js team
- ✅ Optimized for Next.js apps
- Deploy: https://vercel.com/new

### Cloudflare Pages
- ✅ Fast global CDN
- ✅ Generous free tier
- Deploy: https://pages.cloudflare.com

---

## 🔗 Backend Required

This frontend requires a running FastAPI backend. Deploy options:
- **Render** (recommended) - Uses `render.yaml` from root
- **Railway** - Full-stack deployment
- **Heroku** - Traditional PaaS

See [NETLIFY_DEPLOYMENT.md](../../NETLIFY_DEPLOYMENT.md) for backend deployment instructions.

---

## 📚 Learn More

### Next.js
- [Next.js Documentation](https://nextjs.org/docs)
- [Learn Next.js](https://nextjs.org/learn)
- [Next.js GitHub](https://github.com/vercel/next.js)

### Libraries Used
- [shadcn/ui](https://ui.shadcn.com) - UI components
- [Tailwind CSS](https://tailwindcss.com) - Styling
- [Framer Motion](https://www.framer.com/motion/) - Animations
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber) - 3D graphics

---

## 🐛 Issues & Support

- 📖 [Main README](../../README.md)
- 🐛 [Report Issues](https://github.com/anasvhora284/Flux-Depth-Generator/issues)
- 💬 [Discussions](https://github.com/anasvhora284/Flux-Depth-Generator/discussions)

---

Made with ❤️ using Next.js 15 and AI-powered depth estimation
