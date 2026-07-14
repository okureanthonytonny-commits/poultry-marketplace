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
2. **Start with Docker Compose**:
   ```bash
   docker-compose up
   ```
   This spins up the PostgreSQL database and the FastAPI backend.
3. **Frontend** (separately):
   ```bash
   cd frontend-store
   npm install
   npm start
   ```

## What's implemented vs in-progress
- **Implemented**: Full backend API (auth, cart, orders, products) with Alembic migrations and custom error responses; React storefront with cart functionality.
- **In-progress**: The project is **paused** pending a potential client — core functionality is complete but may lack final polish. This was after business validation, and I confirmed it was best to pause the project until any signal comes across that needs completion of the project.

## Project history
This is the **third iteration** of a marketplace concept — earlier versions (`limelight`, `limelight_v2`) explored auth and cart logic before this rebuild added proper migrations, custom exception handling, and a full React frontend.