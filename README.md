# Flux Depth Generator

A full-stack web application for generating high-quality depth maps from images using the **Depth Anything V2** model. Features include batch processing, multiple visualization modes, and invisible depth embedding using Google Depth XMP metadata.

![Depth Anything V2](https://img.shields.io/badge/AI-Depth%20Anything%20V2-blue)
![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-black)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)

> **🚀 Want to deploy this? [Quick Start: Deploy on Netlify in 5 minutes →](./QUICKSTART_NETLIFY.md)**

---

## ✨ Features

- **🖼️ Depth Map Generation**: Generate accurate depth maps using state-of-the-art Depth Anything V2 models
- **📦 Batch Processing**: Process up to 200 images with async job handling for large batches
- **🎨 Multiple Output Modes**:
  - **Embedded Image**: Original image with depth invisibly embedded as XMP metadata
  - **Depth Map**: Colorized depth visualization with multiple colormap options
- **🔐 Authentication**: User signup with email OTP verification and optional 2FA
- **📱 Responsive Design**: Beautiful UI that works on desktop, tablet, and mobile

---

## 🛠️ Tech Stack

### Backend
| Library | Purpose |
|---------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Modern Python web framework |
| [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) | Monocular depth estimation |
| [PyTorch](https://pytorch.org/) | Deep learning framework |
| [SQLAlchemy](https://www.sqlalchemy.org/) | Async ORM for PostgreSQL |
| [FastAPI-Mail](https://sabuhish.github.io/fastapi-mail/) | Email sending with SMTP |
| [Pydantic](https://docs.pydantic.dev/) | Data validation |
| [Pillow](https://pillow.readthedocs.io/) | Image processing |

### Frontend
| Library | Purpose |
|---------|---------|
| [Next.js 15](https://nextjs.org/) | React framework with App Router |
| [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS |
| [shadcn/ui](https://ui.shadcn.com/) | Beautiful UI components |
| [Framer Motion](https://www.framer.com/motion/) | Animations |
| [Lucide React](https://lucide.dev/) | Icons |

---

## 🚀 Getting Started

### Deployment Options

**Want to deploy to production?** 📦
- 🆓 **[Free ($0) deployment guide](./RENDER_DEPLOYMENT.md)** — Render Blueprint, split stack, or local API + free frontend
- 🌐 **[Netlify Deployment Guide](./NETLIFY_DEPLOYMENT.md)** — Deploy frontend on Netlify + backend on Render/Railway (if present)
- 🔧 **Local Development** - Follow the setup instructions below

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database
- SMTP email service (Gmail recommended)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your credentials

# Run migrations (if using alembic)
# alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local
# Edit .env.local with your backend URL

# Start development server
npm run dev
```

---

## ⚙️ Environment Variables

### Backend (`.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `SECRET_KEY` | ✅ | JWT signing key (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`) |
| `MAIL_USERNAME` | ✅ | SMTP email username |
| `MAIL_PASSWORD` | ✅ | SMTP password (use App Password for Gmail) |
| `MAIL_FROM` | ✅ | From email address |
| `MAIL_SERVER` | ❌ | SMTP server (default: smtp.gmail.com) |
| `MAIL_PORT` | ❌ | SMTP port (default: 587) |

### Frontend (`.env.local`)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API URL (e.g., `http://localhost:8000/api/v1`) |

---

## 📁 Project Structure

```
Flux-Wallpaper-Web/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API routes
│   │   ├── core/                # Config, security, image processing
│   │   │   ├── Depth_Anything_V2/  # Depth model
│   │   │   └── image_processing.py
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   └── services/            # Business logic
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/                     # Next.js App Router
│   ├── components/              # React components
│   ├── lib/                     # Utilities
│   └── .env.example
└── render.yaml                  # Render deployment config
```

---

## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/signup` | Register new user |
| `POST` | `/api/v1/auth/verify-signup` | Verify email OTP |
| `POST` | `/api/v1/auth/login` | Login (returns JWT or 2FA prompt) |
| `POST` | `/api/v1/depth/generate` | Generate depth maps (batch) |
| `GET` | `/api/v1/depth/status/{job_id}` | Check async job status |
| `GET` | `/api/v1/depth/download/{job_id}` | Download completed batch |

---

## 🚢 Deployment

### Netlify + Render/Railway (Recommended)

For production deployment with separate frontend and backend hosting:

👉 **[Complete Netlify Deployment Guide](./NETLIFY_DEPLOYMENT.md)**

This guide covers:
- ✅ Deploying the Next.js frontend on Netlify
- ✅ Deploying the FastAPI backend on Render or Railway
- ✅ Setting up PostgreSQL database
- ✅ Configuring environment variables
- ✅ Setting up CORS and custom domains

### Deployment (Railway) 🚂

Since this is a monorepo, deploying to Railway requires setting up two separate services.

#### 1. Backend Service
1.  Create a **New Project** on Railway.
2.  Add a **GitHub Repo** service -> Select this repository.
3.  Go to **Settings** -> **Root Directory** and set it to `/Flux-Wallpaper-Web/backend`.
4.  Go to **Variables** and add:
    *   `PORT`: `8000`
    *   `PYTHON_VERSION`: `3.11`
    *   `DATABASE_URL`: (Connect a PostgreSQL service in Railway and use its URL)
    *   `SECRET_KEY`: (Generate a secure random string)
    *   `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`: (Your email credentials)
    *   `MAIL_PORT`: `465`
    *   `MAIL_SERVER`: `smtp.gmail.com`
    *   `ACCESS_TOKEN_EXPIRE_MINUTES`: `11520`

#### 2. Frontend Service
1.  Add another **GitHub Repo** service to the same project.
2.  Go to **Settings** -> **Root Directory** and set it to `/Flux-Wallpaper-Web/frontend`.
3.  Go to **Variables** and add:
    *   `NEXT_PUBLIC_API_URL`: The URL of your deployed Backend service (e.g. `https://web-production...up.railway.app/api/v1`)

#### 3. Database
1.  Add a **PostgreSQL** service to your Railway project.
2.  Link it to your Backend service securely using the `DATABASE_URL` variable.

The project includes optimized `Dockerfile` and `railway.toml` configs in each folder to ensure fast builds (handling CPU-only PyTorch automatically).

### Deployment (Render) 🚀

**Quick Start:**
1. Deploy backend on [Render](https://render.com) using `render.yaml` (included)
2. Deploy frontend on [Netlify](https://netlify.com) using `netlify.toml` (included)
3. Configure environment variables on both platforms
4. Test your deployment! 🎉

### Alternative Deployment Options

- **Vercel**: Great for Next.js, but backend needs separate hosting
- **Railway**: Can host both frontend and backend together
- **Heroku**: Traditional PaaS, supports both frontend and backend
- **Docker**: Use provided configurations for containerized deployment

---

## 🙏 Credits & Acknowledgments

### Depth Anything V2
This project uses **Depth Anything V2** for monocular depth estimation.

- **Paper**: [Depth Anything V2](https://arxiv.org/abs/2406.09414)
- **Repository**: [github.com/DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2)
- **Authors**: Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao, Xiaogang Xu, Jiashi Feng, Hengshuang Zhao

If you use this project, please cite:
```bibtex
@article{depth_anything_v2,
  title={Depth Anything V2},
  author={Yang, Lihe and Kang, Bingyi and Huang, Zilong and Zhao, Zhen and Xu, Xiaogang and Feng, Jiashi and Zhao, Hengshuang},
  journal={arXiv preprint arXiv:2406.09414},
  year={2024}
}
```

### Other Libraries
- [FastAPI](https://fastapi.tiangolo.com/) - Sebastián Ramírez
- [Next.js](https://nextjs.org/) - Vercel
- [shadcn/ui](https://ui.shadcn.com/) - shadcn
- [Tailwind CSS](https://tailwindcss.com/) - Tailwind Labs

---

## 📄 License

This project is for educational and personal use. The Depth Anything V2 model has its own license - please refer to their repository for commercial use guidelines.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ using AI-powered depth estimation
