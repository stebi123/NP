# # test_env.py
# # import os
# # from dotenv import load_dotenv
# # load_dotenv()
# # print("JWT_SECRET =", os.getenv("JWT_SECRET"))
# # print("DATABASE_URL =", os.getenv("DATABASE_URL"))

# from app.core.database import SessionLocal
# from app.models.product import Product
# from app.schemas.product import ProductResponse

# # Create a DB session
# db = SessionLocal()

# # ✅ 1. Create a product
# new_product = Product(
#     prod_id="PROD001",
#     name="Sample Widget",
#     brand_id=1,
#     category_id=1,
#     subcategory_id=1,
#     unit_of_measure="kg",
#     weight=1.2,
#     sku="WIDG123"
# )

# # Add to DB
# db.add(new_product)
# db.commit()
# db.refresh(new_product)

# print("Inserted product ID:", new_product.id)

# # ✅ 2. Test schema mapping
# product_schema = ProductResponse.from_orm(new_product)
# print(product_schema)
