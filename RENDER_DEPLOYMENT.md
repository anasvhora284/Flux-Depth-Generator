# Deploy on $0 (free tiers)

This guide covers the cheapest ways to run Flux Depth Generator. **The frontend and database can stay free reliably; the ML API is the bottleneck** because PyTorch + Depth Anything V2 need more RAM than most free web tiers provide.

## Option A — All on Render (simplest, $0)

Uses the included [`render.yaml`](./render.yaml) with **free** plans for API, frontend, and Postgres.

### Deploy

1. Push `render.yaml` to `main` (merge [PR #2](https://github.com/anasvhora284/Flux-Depth-Generator/pull/2) or equivalent).
2. Open: **https://dashboard.render.com/blueprint/new?repo=https://github.com/anasvhora284/Flux-Depth-Generator**
3. Click **Apply** and connect GitHub.
4. Set secrets when prompted:
   - `MAIL_USERNAME` — e.g. Gmail address
   - `MAIL_PASSWORD` — [Gmail App Password](https://myaccount.google.com/apppasswords)
   - `MAIL_FROM` — sender address
5. Wait for deploys (API Docker build can take **15–30+ minutes**).

### URLs

| Service | URL |
|---------|-----|
| Frontend | `https://flux-depth-frontend.onrender.com` |
| API | `https://flux-depth-api.onrender.com` |
| API docs | `https://flux-depth-api.onrender.com/api/v1/docs` |

### Free-tier limits (Render)

| Resource | Limit | Impact |
|----------|--------|--------|
| Web services | 512 MB RAM, **sleep after ~15 min idle** | Cold start 30s–2min; API may **OOM** during model load |
| Postgres (free) | **Expires after 90 days** | Not for long-term production |
| Build time | Can timeout on slow model download | Retry deploy or upgrade API plan |

**If the API fails health checks or crashes:** Dashboard → `flux-depth-api` → **Upgrade** to **Starter** ($7/mo, 512 MB dedicated — may still be tight) or **Standard** (2 GB, recommended for PyTorch).

---

## Option B — Split stack (often more reliable at $0)

Use the best free product per layer:

| Layer | Free host | Config |
|-------|-----------|--------|
| Frontend | [Vercel](https://vercel.com) or [Netlify](https://netlify.com) | Root: `Flux-Wallpaper-Web/frontend`, build: `npm run build` |
| Database | [Neon](https://neon.tech) or [Supabase](https://supabase.com) | Copy connection string → `DATABASE_URL` on backend |
| API | Render free **or** run locally | See Option C |

**Frontend env:**

```env
NEXT_PUBLIC_API_URL=https://YOUR-API-HOST/api/v1
```

(`resolveApiBaseUrl()` in the frontend appends `/api/v1` if you only pass the host URL.)

**Backend env** (same as `.env.example`):

```env
DATABASE_URL=postgresql+asyncpg://...   # Neon gives postgres:// — app auto-converts
SECRET_KEY=<random>
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_FROM=...
```

---

## Option C — Free UI + local API (100% $0, demo/dev)

Best when Render’s free API keeps OOMing:

1. **Local backend**

   ```bash
   cd Flux-Wallpaper-Web/backend
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   cp .env.example .env   # edit DATABASE_URL, mail, SECRET_KEY
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Expose API** (optional, for a deployed frontend): [ngrok](https://ngrok.com) free tier  
   `ngrok http 8000` → set `NEXT_PUBLIC_API_URL=https://xxxx.ngrok-free.app/api/v1` on Netlify/Vercel.

3. **Deploy frontend only** (Netlify/Vercel/Cloudflare Pages) — see [frontend README](./Flux-Wallpaper-Web/frontend/README.md).

---

## Email on $0

| Provider | Free tier |
|----------|-----------|
| Gmail SMTP | Free with App Password (limits apply) |
| [Resend](https://resend.com) | 3k emails/month |
| [Brevo](https://www.brevo.com) | 300 emails/day |

The backend supports SMTP via `MAIL_*` variables in `.env`.

---

## Quick troubleshooting

| Symptom | Fix |
|---------|-----|
| API deploy fails / unhealthy | Upgrade API instance; check build logs for model download errors |
| `502` / timeout on first request | Free tier woke from sleep — wait and retry |
| Signup email never arrives | Check `MAIL_*` secrets; use App Password for Gmail |
| Frontend can’t reach API | Verify `NEXT_PUBLIC_API_URL`; CORS allows all origins when `BACKEND_CORS_ORIGINS` is unset |
| DB connection errors | Ensure `DATABASE_URL` is set; Neon URL is auto-converted to `asyncpg` |

---

## Cost summary

| Setup | Monthly cost | Best for |
|-------|----------------|----------|
| Render Blueprint (all free) | **$0** | Trying the full app; may need API upgrade |
| Netlify + Neon + local API | **$0** | Demos, development |
| Render API on Starter/Standard | **$7–25+** | Stable depth generation |

For questions about the Blueprint file, see [`render.yaml`](./render.yaml).
