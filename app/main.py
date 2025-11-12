from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import auth,products,batch,brand,category,company,pallet,staging,subcategory
from app.models.batch_pallet import *
from app.models.batch import *
from app.models.brand import *
from app.models.category import *
from app.models.company import *
from app.models.pallet import *
from app.models.products import *
from app.models.role import *
from app.models.staging import *
from app.models.subcategory import *
from app.models.user import *
from app.models.warehouse import *

app = FastAPI(title="FastAPI Backend")
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(batch.router)
app.include_router(brand.router)
app.include_router(category.router)
app.include_router(subcategory.router)
app.include_router(company.router)
app.include_router(pallet.router)  
app.include_router(staging.router)
