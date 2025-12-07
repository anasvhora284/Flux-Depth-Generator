# Deploying Flux Depth Generator on Netlify

This guide walks you through deploying the **Flux Depth Generator** application using Netlify for the frontend and a backend hosting service for the Python API.

## Architecture Overview

Since this is a full-stack application:
- **Frontend (Next.js)**: Deploy on Netlify ✅
- **Backend (FastAPI + ML Models)**: Deploy on Render, Railway, or Heroku (Python required)
- **Database (PostgreSQL)**: Use the database service from your backend provider

> **Note**: Netlify is optimized for static sites and serverless functions. The Python backend with ML models requires a traditional server environment, so we deploy it separately.

---

## Part 1: Deploy Backend (FastAPI)

### Option A: Deploy Backend on Render (Recommended)

The repository already includes a `render.yaml` configuration file at the root.

1. **Sign up for Render**: https://render.com
2. **Connect Your Repository**:
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
3. **Configure Environment Variables** in Render Dashboard:
   ```
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-gmail-app-password
   MAIL_FROM=noreply@yourdomain.com
   ```
4. **Deploy**: Render will automatically:
   - Create a PostgreSQL database
   - Deploy the backend service
   - Provide you with a backend URL (e.g., `https://flux-depth-backend.onrender.com`)

5. **Save Your Backend URL** - you'll need it for the frontend deployment.

### Option B: Deploy Backend on Railway

1. **Sign up for Railway**: https://railway.app
2. **Create New Project** → Import from GitHub
3. **Add PostgreSQL Database**: Railway Marketplace → PostgreSQL
4. **Configure Environment Variables**:
   - Railway will auto-fill `DATABASE_URL`
   - Add: `SECRET_KEY`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`
5. **Set Build & Start Commands**:
   - Build: `cd backend && pip install -r requirements.txt`
   - Start: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Deploy** and save the backend URL.

---

## Part 2: Deploy Frontend on Netlify

### Prerequisites
- GitHub/GitLab/Bitbucket account
- Your backend URL from Part 1

### Step-by-Step Deployment

#### 1. Sign Up / Log In to Netlify
Go to https://netlify.com and sign up (free tier is sufficient).

#### 2. Connect Repository
- Click **"Add new site"** → **"Import an existing project"**
- Choose your Git provider and authorize Netlify
- Select the `Flux-Depth-Generator` repository

#### 3. Configure Build Settings

Netlify will auto-detect Next.js. Verify these settings:

**Build Settings:**
```
Base directory: Flux-Wallpaper-Web/frontend
Build command: npm run build
Publish directory: .next
```

**Environment Variables** (click "Show advanced" → "New variable"):
```
NEXT_PUBLIC_API_URL = https://your-backend-url.onrender.com/api/v1
NODE_VERSION = 20
```

> ⚠️ **Important**: Replace `https://your-backend-url.onrender.com/api/v1` with your actual backend URL from Part 1.

#### 4. Deploy
- Click **"Deploy site"**
- Netlify will:
  1. Install dependencies (`npm install`)
  2. Build the Next.js app (`npm run build`)
  3. Deploy to a unique URL (e.g., `https://random-name-123.netlify.app`)

#### 5. Custom Domain (Optional)
- Go to **Site settings** → **Domain management**
- Click **"Add custom domain"**
- Follow instructions to configure DNS

---

## Part 3: Configure Backend CORS

After deploying the frontend, you need to allow it to communicate with the backend.

1. **Get Your Netlify URL** (e.g., `https://your-site.netlify.app`)
2. **Update Backend Environment Variables** on Render/Railway:
   ```
   BACKEND_CORS_ORIGINS=["https://your-site.netlify.app","https://www.your-custom-domain.com"]
   ```
3. **Redeploy Backend** if necessary.

---

## Part 4: Testing Your Deployment

1. **Visit Your Netlify URL**: `https://your-site.netlify.app`
2. **Test Signup/Login**: Verify email OTP works
3. **Upload Test Image**: Ensure depth generation works
4. **Check Browser Console**: Look for CORS errors (should be none)

---

## Troubleshooting

### Issue: "Failed to fetch" or CORS errors
**Solution**: 
- Verify `NEXT_PUBLIC_API_URL` in Netlify environment variables
- Check `BACKEND_CORS_ORIGINS` includes your Netlify URL
- Ensure backend is running (check Render/Railway logs)

### Issue: Build fails on Netlify
**Solution**:
- Check Node version is set to 20: `NODE_VERSION=20`
- Verify `npm install` succeeds locally
- Review Netlify build logs for specific errors

### Issue: Pages return 404
**Solution**:
- Ensure `netlify.toml` is present in `Flux-Wallpaper-Web/frontend/`
- Check "Publish directory" is set to `.next`
- Verify Next.js build completed successfully

### Issue: Environment variables not working
**Solution**:
- Redeploy after adding/changing environment variables
- Variables starting with `NEXT_PUBLIC_` are embedded at build time
- Check environment variables are set in Netlify UI (Site settings → Environment variables)

---

## Alternative: Deploy Frontend Elsewhere

If you prefer not to use Netlify:

### Vercel (Next.js Creator)
1. Go to https://vercel.com
2. Import repository
3. Set base directory: `Flux-Wallpaper-Web/frontend`
4. Add environment variable: `NEXT_PUBLIC_API_URL`
5. Deploy

### Cloudflare Pages
1. Go to https://pages.cloudflare.com
2. Connect repository
3. Build command: `cd Flux-Wallpaper-Web/frontend && npm run build`
4. Output directory: `Flux-Wallpaper-Web/frontend/.next`
5. Add environment variable and deploy

---

## Environment Variables Reference

### Frontend (Netlify)
| Variable | Required | Example |
|----------|----------|---------|
| `NEXT_PUBLIC_API_URL` | ✅ | `https://backend.onrender.com/api/v1` |
| `NODE_VERSION` | ✅ | `20` |

### Backend (Render/Railway)
| Variable | Required | Example |
|----------|----------|---------|
| `DATABASE_URL` | ✅ | Auto-filled by Render/Railway |
| `SECRET_KEY` | ✅ | `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `MAIL_USERNAME` | ✅ | `your-email@gmail.com` |
| `MAIL_PASSWORD` | ✅ | Gmail App Password |
| `MAIL_FROM` | ✅ | `noreply@yourdomain.com` |
| `BACKEND_CORS_ORIGINS` | ✅ | `["https://your-site.netlify.app"]` |

---

## Cost Estimate (Free Tier)

- **Netlify**: Free (100GB bandwidth, 300 build minutes/month)
- **Render**: Free (750 hours/month, but services spin down after 15min inactivity)
- **Railway**: $5/month free trial credit
- **Database**: Free tier with 1GB storage (Render) or limited (Railway)

**For Production**: Consider upgrading to paid tiers for:
- No cold starts (Render free tier sleeps)
- More build minutes (Netlify)
- Better database performance

---

## Next Steps

1. ✅ Deploy backend on Render/Railway
2. ✅ Deploy frontend on Netlify
3. ✅ Configure CORS
4. 🎨 Set up custom domain (optional)
5. 📧 Configure email service (Gmail recommended)
6. 🔒 Enable HTTPS (automatic on Netlify)
7. 📊 Set up monitoring (optional)

---

## Support

- **Netlify Docs**: https://docs.netlify.com
- **Render Docs**: https://render.com/docs
- **Next.js Deployment**: https://nextjs.org/docs/deployment

For issues specific to this project, please open an issue on GitHub.

---

Made with ❤️ • Deployed globally with Netlify & Render
