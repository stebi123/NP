# test_env.py
import os
from dotenv import load_dotenv
load_dotenv()
print("JWT_SECRET =", os.getenv("JWT_SECRET"))
print("DATABASE_URL =", os.getenv("DATABASE_URL"))