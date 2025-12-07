# Deployment Architecture

## Overview

The Flux Depth Generator uses a **split deployment architecture** where different components are hosted on specialized platforms:

```
┌─────────────────────────────────────────────────────────────┐
│                        User's Browser                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTPS
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                  Netlify (Frontend CDN)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │             Next.js 15 Application                    │  │
│  │  • Static pages & assets served from CDN             │  │
│  │  • Server-side rendering & API routes                │  │
│  │  • Automatic HTTPS & global CDN                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ API Requests (HTTPS)
                 │ NEXT_PUBLIC_API_URL
                 ↓
┌─────────────────────────────────────────────────────────────┐
│             Render / Railway (Backend Server)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend                          │  │
│  │  • REST API endpoints                                 │  │
│  │  • Depth Anything V2 ML model                        │  │
│  │  • Image processing pipeline                         │  │
│  │  • Authentication & authorization                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ Database Connection
                 │ DATABASE_URL
                 ↓
┌─────────────────────────────────────────────────────────────┐
│        PostgreSQL Database (Render / Railway)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • User accounts & authentication                     │  │
│  │  • Job queue & processing status                     │  │
│  │  • Application metadata                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                 │
                 │ Email Service
                 │ SMTP (Gmail)
                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    Email Service (Gmail)                     │
│  • OTP verification emails                                   │
│  • Account notifications                                     │
└─────────────────────────────────────────────────────────────┘
```

## Why This Architecture?

### Frontend on Netlify
✅ **Pros:**
- Free tier with generous limits (100GB bandwidth)
- Global CDN for fast page loads worldwide
- Automatic HTTPS and security headers
- Easy Git integration and preview deployments
- Optimized for Next.js applications

❌ **Limitations:**
- Cannot run Python or ML models
- Serverless functions have time/memory limits

### Backend on Render/Railway
✅ **Pros:**
- Full Python runtime for ML models
- Can handle long-running processes
- Persistent storage for models
- PostgreSQL database included
- Docker support for custom environments

❌ **Limitations:**
- Free tier has cold starts (15min inactivity)
- Limited compute resources on free tier

### Database Co-located with Backend
✅ **Pros:**
- Low latency between backend and database
- Simplified configuration (auto-generated DATABASE_URL)
- Backup and restore tools included

## Data Flow

### 1. User Signup Flow
```
Browser → Netlify (Next.js) → Render (FastAPI) → PostgreSQL
                                ↓
                            Gmail (SMTP)
                                ↓
                            User Email (OTP)
```

### 2. Depth Generation Flow
```
Browser → Upload Image → Netlify → Render Backend
                                      ↓
                              Depth Anything V2 Model
                                      ↓
                              Process Image
                                      ↓
                              Store Job Info (PostgreSQL)
                                      ↓
                              Return Depth Map
                                      ↓
                              Browser Download
```

### 3. Authentication Flow
```
Browser → Login → Netlify → Render (Verify Credentials)
                              ↓
                         PostgreSQL (User DB)
                              ↓
                         JWT Token Generated
                              ↓
                         Browser (Store in localStorage)
```

## Environment Configuration

### Frontend (Netlify)
```env
NEXT_PUBLIC_API_URL=https://backend.onrender.com/api/v1
NODE_VERSION=20
```

### Backend (Render/Railway)
```env
DATABASE_URL=postgresql+asyncpg://... (auto-generated)
SECRET_KEY=<random-32-byte-string>
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=<gmail-app-password>
MAIL_FROM=noreply@yourdomain.com
BACKEND_CORS_ORIGINS=["https://your-site.netlify.app"]
```

## File Structure

```
Flux-Depth-Generator/
├── netlify.toml                          # Netlify config (root deploy)
├── NETLIFY_DEPLOYMENT.md                 # Detailed deployment guide
├── QUICKSTART_NETLIFY.md                 # 5-minute quick start
├── render.yaml                           # Render backend config
│
└── Flux-Wallpaper-Web/
    ├── frontend/
    │   ├── netlify.toml                  # Netlify config (frontend only)
    │   ├── .env.example                  # Frontend env template
    │   └── [Next.js app files...]
    │
    └── backend/
        ├── .env.example                  # Backend env template
        ├── requirements.txt              # Python dependencies
        └── [FastAPI app files...]
```

## Security Considerations

### HTTPS Everywhere
- ✅ Netlify provides automatic HTTPS
- ✅ Render/Railway provide HTTPS endpoints
- ✅ Database connections use SSL

### CORS Protection
- Frontend domain must be in `BACKEND_CORS_ORIGINS`
- Prevents unauthorized API access

### Environment Variables
- Secrets stored in platform dashboards (not in code)
- `NEXT_PUBLIC_*` variables are embedded at build time
- Backend secrets never exposed to frontend

### Authentication
- JWT tokens with expiration
- Email OTP verification required
- Optional 2FA support

## Scaling Considerations

### Current Setup (Free Tier)
- **Frontend**: Can handle 1M+ page views/month
- **Backend**: Cold starts after 15min inactivity
- **Database**: 1GB storage limit

### Production Recommendations
1. **Upgrade Render/Railway**: Paid plans eliminate cold starts
2. **CDN Optimization**: Already handled by Netlify
3. **Database**: Upgrade for more storage/connections
4. **Monitoring**: Add error tracking (Sentry, LogRocket)
5. **Caching**: Implement Redis for session storage

## Alternative Deployments

### All-in-One Platforms
- **Vercel**: Frontend + Serverless (but no Python ML models)
- **Railway**: Can host both frontend and backend together
- **Fly.io**: Good for global deployment
- **AWS/GCP/Azure**: Full control but more complex

### Docker Deployment
The app can be containerized:
- Frontend: Node.js container
- Backend: Python + PyTorch container
- Deploy to: Docker Compose, Kubernetes, ECS, etc.

## Monitoring & Debugging

### Frontend (Netlify)
- **Build Logs**: Netlify Dashboard → Deploys → Build log
- **Function Logs**: Netlify Dashboard → Functions
- **Analytics**: Built-in Netlify Analytics

### Backend (Render/Railway)
- **Application Logs**: Platform dashboard
- **Metrics**: CPU, Memory, Network usage
- **Database**: Query logs, connection pool stats

### Browser DevTools
- **Network Tab**: Check API requests/responses
- **Console**: Check for CORS errors
- **Application Tab**: Verify environment variables

## Cost Breakdown (Free Tier)

| Service | Free Tier Limits | Cost if Exceeded |
|---------|------------------|------------------|
| Netlify | 100GB bandwidth, 300 build mins | $19/month for Pro |
| Render | 750 hours/month, cold starts | $7/month for Starter |
| Railway | $5 credit/month | Pay as you go |
| PostgreSQL | 1GB storage (Render) | $7/month for more |
| Gmail SMTP | 500 emails/day | Free |

**Total Free Tier**: Can support small to medium traffic
**Paid Upgrade**: ~$15-25/month for no cold starts + more resources

## Troubleshooting Quick Reference

| Issue | Check |
|-------|-------|
| CORS Error | `BACKEND_CORS_ORIGINS` includes frontend URL |
| Build Failed | Node version = 20, dependencies installed |
| API Failed | Backend is running, `NEXT_PUBLIC_API_URL` correct |
| Email Not Sent | Gmail App Password set, SMTP port = 587 |
| 404 Error | `netlify.toml` present, publish dir = `.next` |
| Cold Start Slow | Upgrade to paid tier or use keep-alive service |

## Next Steps

1. ✅ Follow [QUICKSTART_NETLIFY.md](./QUICKSTART_NETLIFY.md) for deployment
2. 📚 Read [NETLIFY_DEPLOYMENT.md](./NETLIFY_DEPLOYMENT.md) for details
3. 🔧 Configure environment variables
4. 🧪 Test the deployment
5. 🎨 Customize and iterate!

---

**Made with ❤️ • Cloud-Native Architecture • Scales Globally**
