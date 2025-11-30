from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import auth,products,batch_pallet,batch,brand,category,company,consumer,pallet,staging,subcategory,warehouse,price,sales
from app.models.batch_pallet import *
from app.models.batch import *
from app.models.brand import *
from app.models.category import *
from app.models.company import *
from app.models.consumer import *
from app.models.pallet import *
from app.models.price import *
from app.models.products import *
from app.models.role import *
from app.models.sales import *
from app.models.staging import *
from app.models.subcategory import *
from app.models.user import *
from app.models.warehouse import *

app = FastAPI(title="FastAPI Backend")
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(batch_pallet.router)
app.include_router(batch.router)
app.include_router(brand.router)
app.include_router(category.router)
app.include_router(company.router)
app.include_router(consumer.router)
app.include_router(pallet.router)  
app.include_router(price.router) 
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(staging.router)
app.include_router(subcategory.router)
app.include_router(warehouse.router)

# from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="static"), name="static")
