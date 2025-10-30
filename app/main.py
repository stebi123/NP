from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import auth,products,batch

app = FastAPI(title="FastAPI Backend")
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(batch.router)  # Include other routers as needed