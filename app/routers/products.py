from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.models import products as models
from app.schemas import products as schemas
from app.core.config import settings
from app.core.security import get_current_user  #  assuming you already have JWT auth here
from app.core.database import get_db
from typing import List
import os
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

#  Create a new product
@router.post("/", response_model=List[schemas.ProductResponse])
def create_products(
    products: List[schemas.ProductCreate],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_products = []
    for product in products:
        
        # Validate brand
        brand = db.query(models.Brand).filter(models.Brand.id == product.brand_id).first()
        if not brand:
            raise HTTPException(400, "Brand does not exist")

        # Ensure uniqueness
        exists = db.query(models.Product).filter(
            (models.Product.prod_id == product.prod_id) |
            (models.Product.sku == product.sku) |
            (models.Product.upc == product.upc)
        ).first()

        if exists:
            raise HTTPException(400, "Product with same prod_id/sku/upc exists")

        new_prod = models.Product(**product.dict())
        db.add(new_prod)
        new_products.append(new_prod)
        
    db.commit()
    for prod in new_products:
        db.refresh(prod)
    return new_products

#  Get all products
@router.get("/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

#  Get single product or filtered search
@router.get("/filter", response_model=List[schemas.ProductResponse])
def get_products(
    prod_id: str = None,
    brand_id: int = None,
    name: str = None,
    category_id: int = None,
    subcategory_id: int = None,
    sku: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve products with flexible filters.
    You can query by product_id, prod_id, brand_id, name, category_id, subcategory_id, or sku.
    Example: /products/filter?brand_id=1&category_id=2
    """

    query = db.query(models.Product)

    if prod_id:
        query = query.filter(models.Product.prod_id == prod_id)
    if brand_id:
        query = query.filter(models.Product.brand_id == brand_id)
    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if subcategory_id:
        query = query.filter(models.Product.subcategory_id == subcategory_id)
    if sku:
        query = query.filter(models.Product.sku == sku)

    products = query.all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found matching criteria")

    return products

#  Update product by ID
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, updated_data: schemas.ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for key, value in updated_data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


#  Delete product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

# Upload product image
@router.post("/{product_id}/upload-image")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Find product
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    # Extract file extension
    ext = file.filename.split(".")[-1]
    filename = f"product_{product_id}.{ext}"

    # Correct upload folder from config
    file_path = settings.UPLOAD_FOLDER / filename

    # Save the file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Store relative URL path in DB (best practice)
    product.image_path = f"products/{filename}"
    db.commit()

    return {
        "message": "Image uploaded successfully",
        "image_url": f"/products/{product_id}/image"
    }

#retrieve product image
@router.get("/{product_id}/image")
def get_product_image(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product or not product.image_path:
        raise HTTPException(404, "Image not found")

    # Build full absolute path
    file_path = settings.BASE_DIR / "uploads" / product.image_path

    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found on server")

    return FileResponse(file_path)
