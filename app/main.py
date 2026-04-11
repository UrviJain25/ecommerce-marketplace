from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.api.v1.endpoints import auth, categories, products, cart

# Create all tables on startup (use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Marketplace API",
    description="Multi-vendor marketplace — Auth, Products, Cart (Aarushi's module)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")



