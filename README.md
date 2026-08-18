# ZTP Assistant — Zion Prayer Tower Ministry Assistant

ZTP Assistant is an AI-powered ministry assistant designed to support ministry work such as:
* sermon preparation
* Bible study
* Scripture exploration
* verse explanations
* sermon assistance
* ministry content creation
* creative poster generation
* church banners
* announcements
* visual ministry assets
* Bible verse posters
* church/event graphics

## Features

- **AI Chat Assistant**: Conversational AI for ministry support, utilizing Gemini.
- **Creative Studio**: Generates beautiful typographic posters with Bible verses and ministry graphics.
- **Bible Services**: Fetch Scripture accurately and deterministically directly from the application's Bible service without relying on an image model to hallucinate text.

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (React / TypeScript)
- **Database**: PostgreSQL (Neon) using SQLAlchemy & Alembic

## AI / Creative Pipeline

The Creative Studio pipeline operates as follows:
User request → Assistant → Gemini reasoning / content understanding → Creative Studio → Pollinations image generation → Pillow typography/composition → Cloudinary asset storage → Neon PostgreSQL metadata/history → Frontend rendering

*Bible verse text is retrieved from the application’s Bible service and composed deterministically rather than relying on an image model to render Scripture text.*

## Repository Structure

```
MinistryAssisstant/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .env.example
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   └── .env.example
│
├── README.md
└── .gitignore
```

## Environment Variables

This project uses `.env` files for configuration. **Never commit actual `.env` files with real credentials.** 

Reference the `.env.example` files in both the `backend/` and `frontend/` directories to set up your local environment. 

### Backend Variables (`backend/.env`)
- `GEMINI_API_KEY`: API key for Google Gemini.
- `DATABASE_URL`: Connection string for PostgreSQL (e.g., Neon).
- `CLOUDINARY_*`: Credentials for Cloudinary asset storage.
- `JWT_SECRET`: Secret key for authentication.

### Frontend Variables (`frontend/.env.local`)
- `NEXT_PUBLIC_API_URL`: URL pointing to the backend API (e.g., `http://127.0.0.1:8000`).

## Local Development

### Backend Setup

1. **Install uv**: This project uses `uv` for Python package management.
2. **Navigate to Backend**: `cd backend`
3. **Install Dependencies**: `uv pip install -r pyproject.toml` (or standard `uv sync`).
4. **Environment Configuration**: Copy `.env.example` to `.env` and fill in the values.
5. **Database Migrations**: `alembic upgrade head`
6. **Start Server**: `uv run uvicorn app.main:app --reload` (or standard `fastapi dev` depending on your entry point).

### Frontend Setup

1. **Navigate to Frontend**: `cd frontend`
2. **Install Dependencies**: `npm install`
3. **Environment Configuration**: Copy `.env.example` to `.env.local` and set the backend URL.
4. **Start Development Server**: `npm run dev`

## Database Migrations

Alembic is used for managing database schemas. 
Production credentials are supplied through environment variables and are never committed.
- Apply migrations: `alembic upgrade head`
- Create new migration: `alembic revision --autogenerate -m "description"`

## Testing

**Backend Tests:**
Tests are located in `backend/`. Run tests using:
```bash
cd backend
uv run pytest
```

## Creative Studio

The intended architecture for the Creative Studio is:
1. User requests a graphic.
2. ZTP Assistant triggers `CreativeStudioTool`.
3. Gemini generates a visual prompt.
4. Pollinations AI generates raw artwork.
5. Pillow adds Bible verse typography / layout on top of the image.
6. Cloudinary stores the generated image assets.
7. Neon PostgreSQL stores metadata/history (prompt, provider, provider model, Cloudinary URL, generation status, timestamps).
8. The graphic is sent back to the frontend.

## Deployment Notes

- Ensure `DATABASE_URL` is set to the production Neon connection string.
- Provide all valid API keys (Gemini, Cloudinary) to the environment running the backend.
- Build the Next.js frontend using `npm run build` and serve statically or via a Node server.

## Security

- Do not expose `GEMINI_API_KEY`, `CLOUDINARY_API_SECRET`, or `DATABASE_URL`.
- The `.gitignore` is configured to prevent committing `.env` and `.env.local`.

## Contributing & License
(Add specific contribution guidelines and license as needed.)
