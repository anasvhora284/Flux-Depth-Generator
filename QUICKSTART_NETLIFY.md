# Quick Start: Deploy on Netlify

**🚀 Deploy the Flux Depth Generator frontend to Netlify in 5 minutes!**

## Prerequisites
- GitHub/GitLab/Bitbucket account with this repository
- A deployed backend API (see [Backend Setup](#backend-setup))

## Frontend Deployment (5 Steps)

### 1. Sign Up for Netlify
Go to [netlify.com](https://netlify.com) and sign up (free tier is fine).

### 2. Import Repository
- Click **"Add new site"** → **"Import an existing project"**
- Authorize Netlify with your Git provider
- Select the `Flux-Depth-Generator` repository

### 3. Configure Build
```
Base directory: Flux-Wallpaper-Web/frontend
Build command: npm run build
Publish directory: .next
```

### 4. Add Environment Variable
Under "Environment variables", add:
```
Variable: NEXT_PUBLIC_API_URL
Value: https://your-backend-url.onrender.com/api/v1
```

Also add:
```
Variable: NODE_VERSION
Value: 20
```

### 5. Deploy
Click **"Deploy site"** and wait 2-3 minutes. Done! 🎉

Your site will be live at: `https://random-name-123.netlify.app`

## Backend Setup

The frontend requires a Python backend API. Quick options:

### Option A: Render (Recommended - Free Tier)
1. Go to [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect repo (Render will use `render.yaml`)
4. Set environment variables:
   - `SECRET_KEY` - Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `MAIL_USERNAME` - Your Gmail
   - `MAIL_PASSWORD` - Gmail App Password
   - `MAIL_FROM` - Your email
5. Deploy → Get backend URL

### Option B: Railway ($5 free credit)
1. Go to [railway.app](https://railway.app)
2. Import from GitHub
3. Add PostgreSQL from marketplace
4. Set environment variables
5. Deploy → Get backend URL

**📖 Full Guide**: See [NETLIFY_DEPLOYMENT.md](./NETLIFY_DEPLOYMENT.md) for detailed instructions.

## Test Your Deployment

1. Visit your Netlify URL
2. Sign up with your email
3. Verify OTP from email
4. Upload an image
5. Generate depth map! ✨

## Troubleshooting

**Issue: CORS errors in browser console**
- ✅ Add your Netlify URL to backend `BACKEND_CORS_ORIGINS`
- ✅ Redeploy backend after changing variables

**Issue: "Failed to fetch"**
- ✅ Check `NEXT_PUBLIC_API_URL` is correct in Netlify
- ✅ Ensure backend is running (check Render/Railway logs)

**Issue: Build fails**
- ✅ Verify `NODE_VERSION=20` is set
- ✅ Check build logs for specific errors
- ✅ Try deploying from `main` branch

**Issue: Pages show 404**
- ✅ Check "Publish directory" is set to `.next`
- ✅ Ensure `netlify.toml` exists in repo
- ✅ Redeploy from Netlify dashboard

## What's Next?

- 🌐 Add a custom domain (Netlify Settings → Domain management)
- 🔒 HTTPS is automatic on Netlify ✅
- 📧 Configure email service (Gmail App Password)
- 🎨 Customize the UI (edit in `Flux-Wallpaper-Web/frontend/`)

## Need Help?

- 📖 [Detailed Deployment Guide](./NETLIFY_DEPLOYMENT.md)
- 📖 [Main README](./README.md)
- 🐛 [Open an Issue](https://github.com/anasvhora284/Flux-Depth-Generator/issues)

---

**Made with ❤️ • Deploy in Minutes • Run for Free**
