# poultry-marketplace

A full-stack poultry marketplace web app — the third and final iteration of a marketplace concept, now with proper migrations, custom error handling, and a React storefront.

## Tech stack
- **Backend**: FastAPI (Python)
- **Frontend**: React (JavaScript)
- **Database**: PostgreSQL (via Docker Compose)
- **Container**: Docker / Docker Compose
- **Migrations**: Alembic

## Architecture summary
```
poultry-marketplace/
├── backend/           # FastAPI service
│   └── app/
│       └── modules/   # auth, cart, orders, products (custom domain error responses)
├── frontend-store/    # React customer storefront
├── docs/              # Documentation
├── docker-compose.yml # Services orchestration
└── .gitignore
```
The backend uses a modular structure where each feature (auth, cart, orders, products) is isolated. Custom domain error handling was added in the cart module to improve API clarity.

## Setup / run
1. **Clone the repo**:
```bash
   git clone https://github.com/okureanthonytonny-commits/poultry-marketplace.git
   cd poultry-marketplace
```
2. **Start the database** (PostgreSQL only):
```bash
   cp .env.example .env   # set POSTGRES_PASSWORD
   docker compose up -d
```
3. **Backend**:
```bash
   cd backend
   cp .env.example .env   # fill in DATABASE_URL (password must match POSTGRES_PASSWORD), SECRET_KEY, Google OAuth credentials
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --reload
```
4. **Frontend** (separately):
```bash
   cd frontend-store
   npm install
   npm run dev
```
## What's implemented vs status
- **Implemented**: Full backend API (auth, cart, orders, products) with Alembic migrations and custom error responses; React storefront with cart functionality.
- **Status**: Retired. After repeated business validation, the cost of patching this further outweighs a fresh redesign — this repo is kept as-is, serving as a portfolio artifact for the third iteration of a rebuild lineage (see below) rather than an active project.

## Known limitations
- `backend/requirements.txt` was reconstructed from the code's imports. It is unpinned and has not been verified in a clean environment (the Postgres driver, `psycopg2-binary`, is an assumption).
- `docker-compose.yml` runs only the PostgreSQL database. The backend and frontend run locally (see Setup).

## Project history
This is the **third iteration** of a marketplace concept — earlier versions (`limelight`, `limelight_v2`) explored auth and cart logic before this rebuild added proper migrations, custom exception handling, and a full React frontend.
